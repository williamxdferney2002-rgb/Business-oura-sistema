# TASK-XXX · <título corto>

<!--
Plantilla del arquitecto. Copiar a tareas/activas/TASK-XXX-<slug>.md.
Un archivo por tarea. Cada agente AGREGA su sección al final (nunca reescribe las anteriores);
lo único que se edita en el lugar es la línea STATUS y la sección ESPECIFICACIÓN VIGENTE (D41).
El arquitecto llena APPROVAL antes de entregar la tarea.
ESPECIFICACIÓN VIGENTE (D41): con el primer SPEC_AMENDMENT aprobado, el arquitecto agrega debajo de STATUS
la sección "## ESPECIFICACIÓN VIGENTE", que consolida la especificación y todos los amendments, y la
actualiza en el mismo commit de cada amendment nuevo. Empieza con: "Para trabajo operativo, leer esta
sección. El historial inferior no es lectura obligatoria salvo referencia expresa." Es la fuente operativa
de ejecutor y auditor; lo de abajo queda como historial.
El STATUS de este archivo es la única fuente del estado de la tarea (CURRENT_STATE.md solo dice cuál es la activa).

| STATUS          | Lo pone    | Siguiente que actúa | Qué hace                                                    |
|-----------------|------------|---------------------|-------------------------------------------------------------|
| DRAFT           | arquitecto | el dueño             | Revisa la especificación; con su "dale" el arquitecto llena APPROVAL y pone SPEC_READY |
| SPEC_READY      | arquitecto | ejecutor            | Implementa (exige APPROVAL lleno)                           |
| IN_PROGRESS     | ejecutor   | ejecutor            | Trabajando                                                  |
| AWAITING_AUDIT  | ejecutor   | auditor             | Audita el COMMIT del último informe                         |
| REJECTED        | auditor    | arquitecto → ejecutor | Claude clasifica las incidencias (D39); el ejecutor corrige con su prompt → CORRECTION_REPORT |
| APPROVED        | auditor    | arquitecto          | Sin pruebas humanas: FINAL_STATUS. Con pruebas humanas: AWAITING_HUMAN |
| AWAITING_HUMAN  | arquitecto | el dueño             | Hace las HUMAN_TESTS y reporta PASSED/FAILED + autoriza el cierre |
| BLOCKED         | cualquiera | arquitecto          | Responde con SPEC_AMENDMENT (y el dueño si cambia alcance)   |
| DONE            | arquitecto | —                   | Cerrada. Exige APPROVED y, si hay HUMAN_TESTS, PASSED + autorización del dueño |

BLOCKED lo pone: el ejecutor (ARCHITECTURE_CONFLICT, informe PARTIAL/BLOCKED, o alguna incidencia DISPUTED);
el auditor (tercer rechazo, o el problema está en la especificación: ESCALATE_TO_ARCHITECT en su AUDIT_REPORT).
El SPEC_AMENDMENT dice en NEXT_STATUS cómo sigue: SPEC_READY, REJECTED o AWAITING_AUDIT.
Si una HUMAN_TEST falla (FAILED), el arquitecto agrega un SPEC_AMENDMENT con la corrección y NEXT_STATUS: REJECTED.
Cada etapa termina con el HANDOFF compacto (agentes/plantillas/HANDOFF.md, RULES §12): quién sigue, qué leer, qué hacer.
-->


STATUS: SPEC_READY

## TASK SPECIFICATION
```
TASK_ID: TASK-XXX
OBJECTIVE: <una o dos frases: qué queda funcionando al terminar>
SOURCE_PLAN_SECTION: <plan §x · Fase n · R## · D##>
APPROVAL: <el dueño, "dale", AAAA-MM-DD>   ← sin esto el ejecutor no arranca
BASE_COMMIT: <hash corto de HEAD al especificar>
AUDIT_LEVEL: <QUICK | STANDARD | DEEP> (D41) — <por qué>
CURRENT_STATE: <qué hay hoy en el código y en Google, con rutas; qué falla o falta>
SCOPE:
  - <qué entra, concreto>
OUT_OF_SCOPE:
  - <qué NO se toca aunque parezca relacionado>
FILES_TO_INSPECT:
  - <ruta> — <por qué>
FILES_EXPECTED_TO_CHANGE:
  - <ruta> — <qué cambia>
DEPENDENCIES:
  - <tareas previas, datos o acciones del dueño, servicios>
IMPLEMENTATION_STEPS:
  1. <paso verificable: archivo, función, comportamiento>
  2. …
CONSTRAINTS:
  - <contratos api_* / columnas / IDs de flujos que no cambian; velocidad; estilo; seguridad>
ACCEPTANCE_CRITERIA:
  AC1. <comprobable por el auditor sin preguntar a nadie>
  AC2. …
REQUIRED_TESTS:            (las que corren los agentes)
  - <comando exacto> → esperado <X/Y>
  - casos válidos: …
  - casos inválidos: …
  - duplicados / doble toque: …
HUMAN_TESTS:               (las que solo puede hacer el dueño: Google, celular, Telegram…; "ninguna" si no hay)
  - H1. <qué hacer> → <qué debe pasar>
CLOSURE_CONDITIONS:
  - <qué debe existir para pasar a DONE>
RISKS:
  - <riesgo> → <mitigación>
NOTES_FOR_EXECUTOR:
  - <suposiciones del arquitecto, trampas aplicables de ARCHITECTURE.md, skills a leer>
```

<!--
Debajo se agregan, en orden, según ocurran (formatos en agentes/plantillas/REPORTS.md):
## SPEC_AMENDMENT N          (arquitecto)
## ARCHITECTURE_CONFLICT     (ejecutor)
## IMPLEMENTATION_REPORT     (ejecutor)
## AUDIT_REPORT · ronda 1    (auditor)
## CORRECTION_REPORT · ronda 2 (ejecutor)
## AUDIT_REPORT · ronda 2    (auditor)
## HUMAN_TEST_RESULT         (arquitecto, con lo que reporte el dueño)
## FINAL_STATUS              (arquitecto)
-->
