# Formatos de informe

Cada bloque se **agrega** al final del archivo de la tarea, con un título `## <NOMBRE> · ronda N`. Los campos van siempre, aunque sea con "ninguno". Toda afirmación lleva evidencia (comando + resultado, o `ruta:línea`).

**Breve (D41):** una línea por campo cuando basta. Pruebas en verde: "probar.js 140/140 PASSED", sin logs. Con fallos, solo el error relevante. No se repiten la especificación, archivos sin cambios, decisiones conocidas ni la historia de la tarea. En el chat va solo el veredicto o un resumen corto; el informe vive aquí.

---

## IMPLEMENTATION_REPORT (ejecutor)
`STATUS: COMPLETED` → la tarea pasa a `AWAITING_AUDIT`. `PARTIAL` o `BLOCKED` → la tarea pasa a `BLOCKED` (decide el arquitecto).
```
IMPLEMENTATION_REPORT

TASK_ID:
ROUND: 1
STATUS: COMPLETED | PARTIAL | BLOCKED
COMMIT: el commit que contiene este informe (código + informe juntos, D41)

FILES_CHANGED:
  - <ruta> — <qué y por qué (paso o AC que cumple)>
FILES_CREATED:
FILES_DELETED:

CHANGES_IMPLEMENTED:
  - <por función / nodo, no "mejoras varias">

DECISIONS_MADE:
  - <decisión menor tomada dentro del alcance y por qué>

DEVIATIONS_FROM_PLAN:
  - ninguna
  (o cada desviación: qué, por qué, impacto)

ACCEPTANCE_CRITERIA_STATUS:
  AC1: cumplido — evidencia: <prueba / ruta:línea>
  AC2: …

TESTS_EXECUTED:
  - <comando exacto>
TEST_RESULTS:
  - <salida resumida: X/Y, avisos>; línea base antes: X/Y, después: X/Y

SELF_AUDIT: <resultado de auditar-entrega: ✅ / ⚠️ / ❌ corregidos>

INSTALL_STEPS:          (paral dueño, orden exacto; "no aplica" si no hay nada que instalar)
WHAT_TO_REVIEW:         (qué nodos/archivos revisar al importar o pegar)
SUGGESTED_TESTS:        (pruebas del dueño en PRUEBA / Telegram, con un caso inválido y un doble toque)
NOT_EXECUTED:           (lo que no corrió: Google, n8n, Telegram, IA real…)

KNOWN_LIMITATIONS:
RISKS_OR_PENDING_ITEMS:
INSTRUCTIONS_FOR_AUDITOR:
  - <qué mirar primero, cómo reproducir, datos de prueba>
```

---

## CORRECTION_REPORT (ejecutor, después de un REJECTED)
Sin incidencias `DISPUTED` → `STATUS: AWAITING_AUDIT`. Con alguna `DISPUTED` → corrige las demás y pone `STATUS: BLOCKED` (el arquitecto arbitra con `SPEC_AMENDMENT`).
```
CORRECTION_REPORT

TASK_ID:
ROUND: <n>
RESPONDS_TO: AUDIT_REPORT · ronda <n-1>
STATUS: COMPLETED | PARTIAL | BLOCKED
COMMIT: el commit que contiene este informe (D41)
PREVIOUS_COMMIT: <hash auditado antes>

FIXES:
  ISSUE_001: FIXED | NOT_FIXED | DISPUTED
    CHANGE: <ruta:línea, qué cambió>
    EVIDENCE: <prueba que lo demuestra>
    (DISPUTED: por qué la incidencia es incorrecta, con evidencia; decide el arquitecto)
  ISSUE_002: …

OPTIONAL_IMPROVEMENTS_APPLIED:
  - ninguna (o cuáles, solo si estaban en el alcance)

FILES_CHANGED:
DEVIATIONS_FROM_PLAN:
TESTS_EXECUTED:
TEST_RESULTS:
SELF_AUDIT:
NEW_RISKS:
INSTRUCTIONS_FOR_AUDITOR:
```

---

## AUDIT_REPORT (auditor, compacto, D41)
`VERDICT` reemplaza a `AUDIT_RESULT` (equivalentes). STATUS de la tarea: `APPROVED` → `APPROVED`; `REJECTED` → `REJECTED`; `ARCHITECTURE_CONFLICT` (incluye tercer rechazo o fallo de la especificación) → `BLOCKED`. `APPROVED` solo con 0 CRITICAL, 0 HIGH y todos los criterios verificados.
```
AUDIT_REPORT

TASK_ID:
ROUND: <n>
AUDITED_COMMIT: <hash> · BASE: <hash> · AUDIT_LEVEL: <QUICK | STANDARD | DEEP>
VERDICT: APPROVED | REJECTED | ARCHITECTURE_CONFLICT

FINDINGS:              (ninguno, o uno por línea; detalle en 1–3 frases)
  CRITICAL:
  HIGH:   H1 — <ruta:línea o zona> — <criterio incumplido (AC#, R##, D##, regla)>: <qué pasa y evidencia corta>
  MEDIUM:
  LOW:
REQUIRED_FIXES: <IDs que bloquean> | ninguno
CRITERIA: <todos verificados | cuáles no y por qué>
TESTS: <comando corto → X/Y, solo los que corrió el auditor>
NOT_VERIFIED: <lo que no pudo ejecutar (Google, n8n, Telegram…)> | nada
NEXT: CLAUDE
```

---

## ARCHITECTURE_CONFLICT (ejecutor; pone STATUS: BLOCKED)
```
ARCHITECTURE_CONFLICT

TASK_ID:
WHERE: <paso / AC / constraint de la especificación>
CONFLICTS_WITH: <plan §x, R##, D##, código existente ruta:línea, otro AC>
PROBLEM:
EVIDENCE:
OPTIONS:
  A. <opción> — consecuencias
  B. …
EXECUTOR_RECOMMENDATION:
WORK_DONE_SO_FAR: <nada / commit hash>
```

## SPEC_AMENDMENT (arquitecto; responde a todo BLOCKED)
```
SPEC_AMENDMENT N
TASK_ID:
RESPONDS_TO: ARCHITECTURE_CONFLICT | DISPUTED en CORRECTION_REPORT · ronda n | informe PARTIAL/BLOCKED | escalamiento del auditor (ronda n)
RULINGS:
  - <ISSUE_00x DISPUTED>: ACEPTADA (la incidencia queda anulada) | RECHAZADA (el ejecutor debe corregirla) — por qué
  - <conflicto>: opción elegida — por qué
CHANGES: <qué campos de la especificación cambian y cómo; "ninguno" si solo se arbitra>
APPROVAL: <el dueño, fecha> (obligatorio si cambia SCOPE, OUT_OF_SCOPE o ACCEPTANCE_CRITERIA)
NEXT_STATUS: SPEC_READY (no había implementación) | REJECTED (el ejecutor corrige) | AWAITING_AUDIT (solo faltaba arbitrar; el auditor reaudita con este fallo)
```

## HUMAN_TEST_RESULT (arquitecto, transcribe lo que reportal dueño)
```
HUMAN_TEST_RESULT
TASK_ID:
REPORTED_BY: el dueño, AAAA-MM-DD
RESULTS:
  H1: PASSED | FAILED — <lo que vio el dueño>
  H2: …
OVERALL: PASSED | FAILED
CLOSURE_AUTHORIZED: sí (el dueño, fecha) | no
```

## FINAL_STATUS (arquitecto)
```
FINAL_STATUS
TASK_ID:
RESULT: DONE | CANCELLED
APPROVED_IN: AUDIT_REPORT · ronda <n> (commit <hash>)
HUMAN_TESTS: PASSED (HUMAN_TEST_RESULT del AAAA-MM-DD) | no aplica
CLOSURE_AUTHORIZED_BY: el dueño, AAAA-MM-DD | no aplica
ROUNDS: <n>
OWNER_ACTIONS_PENDING: <instalación en Google / importar en n8n / ninguna>
STATE_UPDATED: CURRENT_STATE.md (sí/no), DECISIONS.md (D## o no), plan §0 (propuesto / no aplica)
FOLLOW_UP_TASKS: <TASK-YYY o ninguna>
```
