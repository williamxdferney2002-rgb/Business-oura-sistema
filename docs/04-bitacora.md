# 4 · Bitácora

Registro de avances, sin datos del negocio. Se agrega una entrada al cerrar cada tarea o fase (formato al final).

## Fases del plan
| # | Fase | Estado (14-nov-2026) |
|---|---|---|
| 0 | Cierre del diseño | Hecha |
| 1 | Base y seguridad | Hecha |
| 2 | App interna (registro manual completo) | En producción |
| 3 | Migración del historial y salida del Excel | Hecha; revisión de inventario en curso |
| 4 | Bot de Telegram: ventas, abonos, consultas | En producción |
| 5 | Pantallazos de Shein y seguimiento de pedidos | En producción |
| 6 | Dinero, reparto y estados de cuenta | Parcial (gastos y estados de cuenta listos; reparto pendiente) |
| 7 | Web con stock en vivo y fotos | Por empezar · [diseño](06-web-y-stock.md) |
| 8 | WhatsApp con clientes | Por empezar |
| 9 | Looker Studio y reportes | Por empezar |

Estimación inicial: 36–53 sesiones de 2–4 horas. Para dejar el Excel (Fases 1–3): 10–15 sesiones.

## Línea de tiempo

### 4-oct-2026 · Día 0: el plan
- Sesión de preguntas por rondas (22 preguntas) para sacar requisitos del Excel, el Power BI, la web y el catálogo existentes.
- **Plan maestro v0.1 → v0.3** el mismo día: 62 requisitos, 9 fases, seguridad, modelo de datos y 36 decisiones.
- Cambio grande: **Google Sheets reemplaza a Supabase** y se agrega una app en Apps Script para dejar el Excel antes de automatizar nada.
- 32 skills instaladas.

### 4–5 oct · Fase 1: base
- Cuenta de Google separada para el negocio, con 2FA y alerta de presupuesto.
- VM gratuita, n8n con HTTPS (Caddy) y dominio dinámico gratuito; swap de 2 GB.
- Sheet generado por script (20 pestañas), copia nocturna con 30 días de retención.
- Bot y grupo de Telegram; flujos de errores, entrada y salud.

### 5 oct · Fase 2: app interna (versiones 2a → 2c-2)
- Compras con número PED###, pendientes por asignar, inventario con costo promedio y margen.
- Ventas V0001…, rebajas, obsequios, venta a socio al costo; clientes con alias.
- Abonos repartidos automáticamente entre ventas, con vista previa y sobrepago bloqueado.
- Salidas de inventario (regalo, inversión del negocio, faltante), anulaciones e historial.
- Lectura en una sola llamada: guardar pasó de 8–11 s a ~3 s.

### 5 oct (noche) · Nace el sistema multiagente (D37)
- Tres roles, un archivo por tarea, plantillas. La tarea piloto (TASK-001) valida una versión y descubre riesgos altos en el PDF, que corrige la siguiente.

### 6–10 oct · App 2c-3 → 2c-7
- **TASK-002:** sincronizador seguro del código hacia la copia de PRUEBA (3 rondas).
- **TASK-003:** orquestador automático de agentes → **aplazado**: el sandbox no demostró la frontera de lectura exigida.
- **TASK-004:** estado de cuenta 2.0, PDF armado en el servidor, trazabilidad de abonos (6 rondas).
- **TASK-005:** factura simple (pantalla, PDF, imagen) y nuevo inicio (5 rondas).
- **TASK-006:** preparar y pasar al Sheet real; migración del historial con conciliación de deuda total y stock contra el Excel.
- **TASK-008:** rediseño visual "Rosa Oura" con guía de estilo propia.

### 15–18 oct · Fases 4 y 5: el bot
- **TASK-009:** puerta n8n → Apps Script, consultas, abonos por texto, deshacer.
- **TASK-010:** compras de Shein **por pantallazo**: Gemini lee, el código suma y compara contra el total del pedido, el socio confirma (5 rondas).
- **TASK-011:** bot listo para producción (sin aviso falso con doble toque, alerta si falla Confirmar).
- **TASK-012:** las capturas de cada pedido se guardan en Drive.

### 18–27 oct · Bot por foto y por voz
- **TASK-013:** abonos con la **foto del comprobante**. Decisión: el bot lee solo capturas, sin PDF (más simple y confiable).
- **TASK-014:** abonos por **nota de voz**: Whisper transcribe, la IA de texto propone con la lista de clientes, el código convierte números en palabras; reintentos y cadena de modelos de respaldo ante errores 503 (6 rondas).
- **TASK-015:** **ventas** por texto y voz: varios productos, cliente nuevo, abono inicial, deshacer (4 rondas).
- **TASK-016 a 019:** ajustes de la prueba en vivo; pedir el enlace de la app al bot; capturas guardadas aunque haya alerta.
- **TASK-007:** velocidad de la app (pantallas al instante con precarga) y precio por tono.
- **27-oct (D46):** Claude lanza a Codex y hace de puente; el dueño deja de copiar handoffs.

### 28-oct – 2-nov · Al real
- **TASK-022:** seguimiento de compras de Shein (recordatorio diario y llegada con avisos).
- **TASK-023:** **gastos** por texto y voz con vista previa, egreso atómico y anti-duplicados (4 rondas).
- **TASK-024:** voz tolerante a errores de transcripción.
- **TASK-020:** una sola guía paso a paso y un comando de lista de verificación para pasar app y bot a producción.
- **2-nov-2026: app 2c-8 y bot completo en producción**; el flujo de prueba queda apagado.

### 3–4 nov · Mejoras de uso real
- **TASK-025 a 028:** precio al asignar a stock, "ya pagó" al vender, categoría por nombre en el bot, elegir producto al vender.
- **TASK-029:** el valor en pesos se ve mientras se teclea; correcciones legibles en el historial.
- **TASK-030:** medios de pago al pie de la factura y del estado de cuenta.
- **TASK-031:** editar una venta (precios, fecha, cliente) sin anularla, recalculando total, saldo y estado.
- **4-nov (D47):** sin aprobación por commit; la aprobación de la especificación basta.

## Lecciones
1. **Primero reemplazar, después automatizar.** Una app manual que deja el Excel vale más que un bot brillante sobre una hoja vieja.
2. **La IA nunca escribe sola en dinero.** Vista previa + botón Confirmar + cálculo determinista. Cero descuadres por "alucinación".
3. **Las cuotas gratuitas fallan en horas pico.** Cadena de modelos de respaldo y reintentos desde el diseño, no después.
4. **Una copia de PRUEBA con datos inventados** permite probar en el celular sin miedo; el sincronizador con candados evita enviar a la copia equivocada.
5. **Medir la velocidad en las pruebas** (idas al Sheet) en vez de "sentirla" en el celular.
6. **Si no se puede demostrar una frontera de seguridad, no existe** (el orquestador quedó aplazado por eso).
7. **El prompt es un índice.** Copiar contexto en los prompts hace que los agentes trabajen sobre versiones viejas; señalar el archivo, no.
8. **Las rondas de corrección son normales.** Varias tareas necesitaron 4–6 rondas; el costo de una ronda es mucho menor que el de un error en producción.
9. **Pruebas humanas una por una**, con qué ver y qué responder. El dueño no necesita leer código.

## Formato de una entrada nueva
```
### <fecha> · <TASK-XXX o fase>: <título>
- Qué quedó funcionando (en palabras del usuario).
- Rondas de auditoría y qué se corrigió (sin datos).
- Decisión tomada, si la hubo, y por qué.
- Lección, si la hubo.
```
