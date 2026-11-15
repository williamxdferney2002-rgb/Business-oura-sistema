# 5 · Cómo replicarlo en otro emprendimiento

Esta guía sirve para cualquier negocio pequeño que hoy lleva su operación en un Excel o en un cuaderno y conversa por Telegram: ropa, cosméticos, repostería por encargo, repuestos, papelería, venta por catálogo. Lo que cambia es el modelo de datos; el método y la arquitectura se mantienen.

## Qué necesitas
| Cosa | Costo |
|---|---|
| Una cuenta de Google **solo para el negocio** (con 2FA) | $0 |
| Proyecto de Google Cloud con alerta de presupuesto y una VM e2-micro (pide tarjeta, no cobra dentro del límite) — o n8n en la nube si prefieres no administrar un servidor | $0 (o el plan de n8n) |
| Un bot de Telegram (@BotFather) y un grupo con los socios | $0 |
| Llave de Gemini en un proyecto **sin facturación**; cuenta de Groq para audio | $0 |
| Claude Code y Codex (o cualquier par de asistentes que trabajen sobre un repositorio) | Tus suscripciones |
| Git y un repositorio **privado** para el código | $0 |

## Paso 1 · Plan maestro antes que código (1 sesión)
1. Reúne lo que existe: el Excel, reportes, la web, capturas de pedidos y comprobantes.
2. Pide al arquitecto una **entrevista por rondas** (skill `grilling`) hasta cerrar: qué se registra, quién lo registra, qué cálculos hay (saldos, reparto, inventario PEPS), qué NO hará el sistema.
3. Que la escriba en `docs/plan-maestro.md` con requisitos numerados, fases, seguridad y decisiones. Marca el origen de cada requisito (lo dijiste tú / sale del Excel / propuesta de la IA) y **aprueba** las propuestas una por una.
4. Ordena las fases para **dejar el Excel primero** (app manual) y automatizar después.

## Paso 2 · Monta el sistema multiagente (media sesión)
1. Copia [plantillas/](../plantillas/) a tu repo: `RULES.md` y `roles/` a `agentes/`, `TASK.md`, `HANDOFF.md` y `REPORTS.md` a `agentes/plantillas/`.
2. Crea `AGENTS.md` (entrada común): qué es el negocio en 3 líneas, jerarquía de autoridad, tabla de roles con el modelo de cada uno, qué leer al empezar y los no negociables (sin secretos en el repo, sin "probado" sin evidencia, sin push, los agentes no tocan producción).
3. Crea `CLAUDE.md` con `@AGENTS.md` y el rol por defecto (arquitecto). Codex lee `AGENTS.md` directo.
4. Crea `agentes/CURRENT_STATE.md` (tarea activa, línea base de pruebas) y `agentes/DECISIONS.md`.
5. Carpetas `tareas/activas/`, `tareas/completadas/`.

Desde aquí, cada petición sigue el ciclo: tú pides → el arquitecto especifica → tú apruebas → ejecutor → auditor nuevo → arquitecto → pruebas en tu celular.

## Paso 3 · Base de datos y app (Fases 1–2)
1. **Modelo de datos en un script** que genere el Sheet (pestañas y encabezados). Así se puede regenerar y versionar.
2. Pestañas mínimas: `productos`, `variantes`, `compras`, `ventas`, `abonos`, `clientes`, `socios` (Gmail de cada uno), `config`, `auditoria`. Columnas: se agregan, nunca se renombran.
3. Apps Script con el patrón de toda escritura: acceso por Gmail → `LockService` único → clave de idempotencia → una fila de una vez → auditoría → devolver la vista. Ver [arquitectura](01-arquitectura.md).
4. Reglas de negocio (saldos, reparto, PEPS) en un archivo de **funciones puras** que se prueba en Node.
5. Un *mock* de Apps Script para correr pruebas fuera de Google y **contar las idas al Sheet**.
6. Dos Sheets: **PRUEBA** (datos inventados) y **REAL**. El código de demo solo corre si el nombre contiene "PRUEBA".
7. Copia nocturna del Sheet a una carpeta de Drive con retención.

## Paso 4 · Migración (Fase 3)
1. Extrae el Excel a JSON **fuera del repo** (tiene datos reales).
2. Una función pura `planMigracion` que devuelve qué filas crear, y un ensayo que solo corre en PRUEBA.
3. **Concilia antes de pasar:** deuda total, unidades en stock y número de salidas deben dar igual en el Excel y en el sistema.
4. Corre en paralelo una semana con el Excel antes de soltarlo.

## Paso 5 · El bot (Fases 4–5)
1. n8n con un flujo de entrada (webhook de Telegram con `secret_token`), uno de errores (avisa por Telegram) y uno de salud (recordatorios).
2. **Lista blanca** de IDs de Telegram de los socios. Todo lo demás se ignora.
3. n8n **no escribe al Sheet**: llama las mismas funciones `api_*` del Apps Script con un secreto compartido.
4. Para cada entrada (texto, voz, foto):
   - la IA **extrae** campos con un esquema cerrado (y el texto de la imagen es dato, no instrucción);
   - el código **valida y calcula** (suma contra el total, cliente existe, no hay sobrepago, ¿ya se registró?);
   - el bot muestra **vista previa** con Confirmar / Cancelar;
   - al confirmar, una sola llamada atómica; después, botón **Deshacer**.
5. Cadena de modelos de respaldo y reintentos para los 503 de las capas gratuitas.
6. Entrega los flujos con `active: false` y una guía de instalación paso a paso.

## Paso 6 · Producción
- Una **guía única** de paso al real con un comando de lista de verificación (qué archivos, en qué orden, qué revisar).
- Pruebas humanas una por una: qué hacer, qué debe pasar, qué responder.
- Si algo falla después de cerrado, se abre una tarea nueva que cite la anterior.

## Cuánto tiempo
Con este método, una persona llevó app + migración + bot completo (texto, voz, fotos, compras, ventas, abonos, gastos) a producción en **unas 4 semanas** de trabajo de tarde/noche. Lo que más tiempo consumió no fue programar, sino las **pruebas humanas en el celular** y las rondas por casos reales que la IA no anticipó (nombres de productos con "para", transcripciones raras, modelos saturados).

## Adaptarlo a tu negocio
| Si tu negocio… | Cambia… |
|---|---|
| Fabrica (repostería, artesanías) | `compras` pasa a insumos; agrega `recetas` o `ordenes` y descuenta insumos al producir |
| Vende de contado siempre | Quita `abonos`; los cobros se vuelven una columna de la venta |
| Tiene más de 2 socios | `socios` con porcentaje; el reparto es una función pura más |
| Recibe pedidos por WhatsApp | Fase 8: el mensaje del cliente llega al grupo como propuesta y un socio confirma |
| No usa Shein | El lector de pantallazos se adapta a facturas de tu proveedor: cambia el prompt y el esquema, no la arquitectura |
