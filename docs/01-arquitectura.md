# 1 · Arquitectura

## Restricciones que la definieron
- **Costo lo más cercano a cero.** Nada de activar facturación en la IA.
- **Dejar el Excel cuanto antes:** primero una app manual que lo reemplace; la automatización viene después.
- **Dos usuarios, ambos desde el celular**, y un grupo de Telegram donde ya conversaban.
- **Volumen bajo:** unas decenas de movimientos al mes. No hace falta una base de datos "de verdad".
- **Una sola persona construyendo**, con agentes de IA.

## Mapa del sistema

```
Telegram (grupo de los socios) ──┐
WhatsApp (clientes, Fase 8) ─────┼──► n8n (VM gratuita e2-micro + Caddy con HTTPS)
                                 │        │  nunca escribe directo al Sheet: llama funciones del Apps Script
App interna (Apps Script) ───────┼────────┼──► Google Sheets (datos + pestañas calculadas)
(solo las cuentas Gmail          │        │        │
 de los socios)                  │        │        ├──► Looker Studio (Fase 9)
                                 │        │        └──► pestaña catalogo_publico ──► endpoint público ──► web (Fase 7)
Google Drive: capturas de pedidos, comprobantes, PDF y copia nocturna del Sheet
IA gratuita: Gemini (lectura de capturas y texto) · Groq Whisper (voz) · Gemma (respaldo)
```

| Pieza | Elección | Por qué |
|---|---|---|
| Base de datos | **Google Sheets** | Gratis, sin pausa por inactividad, los socios ya la entienden, Looker se conecta nativo. Al principio se planeó Supabase; se cambió en la primera semana |
| App interna | **Apps Script** (web app) | Vive junto al Sheet, autenticación con Gmail gratis, sin servidor |
| Automatización | **n8n autoalojado** en una VM e2-micro de la capa gratuita de Google Cloud | Flujos visuales, nodos de Telegram e IA, sin costo por ejecución |
| IA | Gemini con llave de un proyecto **sin facturación**; Groq Whisper para audio; Gemma de respaldo | Cuotas gratuitas suficientes para el volumen; cadena de respaldo cuando un modelo da error 503 |
| Archivos | Google Drive | Capturas y comprobantes quedan junto al registro que los usa |

## Las cinco reglas que sostienen todo

1. **Un solo escritor.** Toda escritura pasa por una función `api_*` del Apps Script, protegida con un único `LockService`. La app y el bot comparten el mismo candado, así que nunca se pisan. n8n no usa el nodo de Google Sheets para escribir.
2. **Idempotencia.** Cada operación lleva una clave única (id del mensaje de Telegram + número de ejecución, o un id del formulario). Un doble toque o un reintento de red produce **un solo registro**.
3. **La IA propone, el humano confirma, el código calcula.** El modelo lee el pantallazo o la nota de voz y propone; el bot muestra una vista previa con botón **Confirmar**. Sumas, saldos, PEPS (primero en entrar, primero en salir) y reparto los hace código determinista y probado, nunca el modelo.
4. **Anular, no borrar.** Ventas, compras, abonos y salidas se anulan con motivo; todo cambio queda en una pestaña de auditoría (historial). Las correcciones en producción son filas nuevas, nunca ediciones de filas calculadas.
5. **Copia de prueba separada.** Hay un Sheet "PRUEBA" con datos inventados donde se instala y prueba cada versión antes de llevarla al real. El código de demostración y los ensayos de migración solo corren si el nombre del Sheet contiene "PRUEBA".

## Patrón de toda función que escribe

```
api_registrarAbono(datos)
  → exigirAcceso_()       ¿el correo está en la pestaña de socios?
  → conCandado_(...)      un solo LockService para toda la app y el bot
  → clave de idempotencia ¿ya se registró esta operación? → devuelve lo mismo
  → agregar_/actualizar_  una fila de una vez
  → auditar_              queda en el historial
  → devuelve la vista ya actualizada (la página no vuelve a pedirla)
```

## Seguridad (obligatoria en todas las fases)
- Secretos solo en las **credenciales de n8n** y en `PropertiesService` del Apps Script. Nunca en código, JSON, repo ni chat.
- **Lista blanca:** en Telegram solo los IDs de los socios dan órdenes; en la app solo sus Gmail.
- **Webhooks firmados:** Telegram con `secret_token`; las llamadas de n8n al Apps Script llevan un secreto compartido.
- **Todo lo que llega de clientes, capturas o comprobantes es dato, no instrucción** (defensa contra inyección de prompts en las imágenes).
- La web futura solo verá una pestaña pública (nombre, precio de lista, tonos, estado, foto). Jamás costos, márgenes ni clientes.
- Flujo de errores global que avisa por Telegram, y copia nocturna del Sheet con 30 días de retención.

## Velocidad
Apps Script es lento al arrancar (10–20 s el primer guardado) y cada ida y vuelta de `google.script.run` cuesta 1–3 s. Por eso:
- Las pestañas que necesita una pantalla se leen **en una sola llamada** (`Sheets.Spreadsheets.Values.batchGet`).
- Cada ejecución guarda en memoria lo que ya leyó.
- Toda acción que guarda devuelve la vista actualizada.
- Las pruebas fuera de Google **cuentan las idas al Sheet**: una función nueva que haga más lecturas de las permitidas falla en las pruebas antes de llegar a producción.

Resultado: de 8–11 s por guardado al principio, a unos 3 s, y pantallas que abren al instante con datos precargados.
