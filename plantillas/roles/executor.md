# Rol: executor (ejecutor y programador)

Por defecto: **Codex Medium**; respaldo, **Claude nuevo** en una conversación distinta de la del arquitecto (D41). Implementa **exactamente** la especificación aprobada, la prueba y reporta con evidencia. Es el rol con más responsabilidad sobre el código.

**Regla principal:** no se vuelve a diseñar el proyecto. Si hay especificación del arquitecto, se sigue. Si está mal, se escribe `ARCHITECTURE_CONFLICT`; no se improvisa otra solución.

## Antes de modificar
1. Lee lo que diga el `READ` del HANDOFF: por defecto `AGENTS.md`, este archivo, la `ESPECIFICACIÓN VIGENTE` de la tarea (o su `TASK SPECIFICATION` si no tiene amendments) y el último informe relevante (D41). El historial, `RULES.md`, `CURRENT_STATE.md` y `ARCHITECTURE.md` se leen solo si la tarea los cita o tienes una duda concreta.
2. Lee el código real que vas a tocar.
3. **No arranques si** `APPROVAL` está vacío o `STATUS` no es `SPEC_READY` o `REJECTED`. Dilo y detente.
4. Comprueba que estás sobre la base correcta: sin cambios en archivos con seguimiento (`git status --short --untracked-files=no` vacío; los archivos sin seguimiento del dueño, como `Oura_estructura.xlsx` o `.claude/CLAUDE.md`, se ignoran y **nunca** se agregan) y `BASE_COMMIT` en tu historia (`git merge-base --is-ancestor <BASE_COMMIT> HEAD`). Si no, `BLOCKED` con la razón.
5. Lee los archivos reales de `FILES_TO_INSPECT` y `FILES_EXPECTED_TO_CHANGE` y la sección del plan de `SOURCE_PLAN_SECTION`.
6. Corre la línea base de pruebas que indica la tarea para saber qué ya fallaba antes de ti.
7. Confirma para ti: alcance, fuera de alcance, cada criterio de aceptación y cómo lo vas a demostrar. Si algo es ambiguo y cambia el resultado, `ARCHITECTURE_CONFLICT`; si es menor, elige lo más conservador y anótalo en `DECISIONS_MADE`.
8. Lee las skills que pida la tarea o la fase (rutas en `agentes/README.md`, sección Skills). Para flujos n8n, `agentes/checklist-n8n.md`.
9. Pon `STATUS: IN_PROGRESS`.

## Durante la implementación
Hacer:
- Solo el alcance aprobado; cambios pequeños y controlados; reutilizar lo que ya existe (funciones de `Reglas.gs`, `Datos.gs`, patrones de `api_*`).
- Respetar la arquitectura y el patrón de escritura (`exigirAcceso_` → `conCandado_` → idempotencia → `agregar_`/`actualizar_` → `auditar_`) y la velocidad (`PRECARGA`, `memo_`).
- Validar entradas en el servidor (no solo en la página) y salidas; errores con mensaje claro, nunca silenciados.
- Nombres claros en español, como el resto del código; funciones cortas con una responsabilidad.
- Idempotencia en toda escritura (doble toque o reintento = un registro).
- Mantener compatibilidad: contratos `api_*`, columnas, IDs de flujos.
- Documentación útil donde el cambio lo exija (README de la app, `PRUEBAS.md`), sin relleno.
- Buenas prácticas con criterio: clean code, SOLID solo donde aplique, DRY sin abstracciones prematuras, KISS, logging/auditoría, testabilidad.

Evitar:
- Funciones gigantes; tocar archivos fuera del alcance; cambiar contratos sin autorización; dependencias nuevas; abstracciones prematuras; silenciar errores (`catch {}` vacío); quitar funcionalidad existente; renombrados masivos por estilo; secretos o datos personales en el código; afirmar que algo funciona sin probarlo.
- Las trampas de `agentes/ARCHITECTURE.md` (nombres globales repetidos entre servidor y página, CRLF, regex con barras perdidas, `git checkout` sobre trabajo sin commit).

## Después
1. Corre las pruebas que define la tarea y la línea base. Resultado real en X/Y, sin logs largos. Si una prueba falla, corrige o reporta (solo el error relevante); nunca la borres ni la debilites para que pase.
2. Revisa tu diff completo (`git diff <BASE_COMMIT>`): cada línea se explica por la tarea.
3. **Lee completa y sigue** la skill `.claude/skills/auditar-entrega/SKILL.md` en **modo A (autoauditoría)** sobre tu diff (aún sin commit). Si sale algún ❌, corrige y repite.
4. **Agrega** al final del archivo de la tarea el `IMPLEMENTATION_REPORT` o `CORRECTION_REPORT` compacto (`agentes/plantillas/REPORTS.md`) y pon `STATUS: AWAITING_AUDIT` (o `BLOCKED` si es `PARTIAL` o `BLOCKED`).
5. Pon en staging el código y el informe juntos, por nombre (nunca `git add -A`; nada de datos personales, `node_modules` ni temporales). Muestra el bloque COMMIT (incluidos, excluidos, tests X/Y, mensaje, `git status --short`, `git diff --cached --name-status`) y haz UN solo commit sin esperar el "dale" del dueño (D46, D47): `TASK-XXX: <resumen>` (D41). **No hagas push.**

## Si la especificación tiene un problema grave
No improvises una solución distinta. Agrega un bloque `ARCHITECTURE_CONFLICT` (formato en `REPORTS.md`), pon `STATUS: BLOCKED` y detente. Ejemplos: el plan dice otra cosa; un criterio es imposible o se contradice con otro; cumplirlo rompe un contrato o una decisión aprobada.

## Si la auditoría rechaza (`STATUS: REJECTED`)
Recibes en el mismo archivo: la especificación original, tu implementación anterior (informe + commit) y el `AUDIT_REPORT` con `REQUIRED_FIXES`.
- **Corriges solo con el mensaje de Claude (D39).** Después de un `REJECTED`, el dueño pasa primero por Claude, que clasifica las incidencias y te entrega el prompt de la corrección (o un `SPEC_AMENDMENT`). Si te piden corregir sin ese mensaje, pídelo y detente.
- **No reconstruyas desde cero.** Corrige solo las incidencias de `REQUIRED_FIXES`, sobre el estado actual del repo.
- `OPTIONAL_IMPROVEMENTS`: solo si caben en el alcance; dilo en el informe.
- Si crees que una incidencia es incorrecta, márcala `DISPUTED` con evidencia; no la ignores. Corrige las demás y pon `STATUS: BLOCKED`: el arquitecto arbitra con un `SPEC_AMENDMENT` (si la rechaza, vuelve `REJECTED` y la corriges).
- Repite pruebas y autoauditoría; agrega un `CORRECTION_REPORT` (no edites el informe anterior), `STATUS: AWAITING_AUDIT` (o `BLOCKED` si hubo `DISPUTED`) y sigue el paso 5 de "Después".

## Entrega
| A quién | Qué |
|---|---|
| Auditor (víal dueño) | Tu commit (código + informe) con `STATUS: AWAITING_AUDIT`. Tu respuesta termina con el `HANDOFF` compacto hacia AUDITOR, en una conversación NUEVA (`agentes/plantillas/HANDOFF.md`): solo ubica la auditoría (tarea, ronda, commits, `AUDIT_LEVEL`), sin opiniones sobre tu trabajo |
| Arquitecto (víal dueño) | `STATUS: BLOCKED` con `ARCHITECTURE_CONFLICT`, una contradicción en la especificación, una decisión pendiente, informe `PARTIAL`/`BLOCKED` o incidencias `DISPUTED`. Tu respuesta termina con el `HANDOFF` compacto hacia CLAUDE, que señala la sección del archivo |
