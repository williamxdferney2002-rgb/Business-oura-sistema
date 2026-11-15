# Plantilla: HANDOFF compacto (D39, D41)

**PROMPT = ÍNDICE · REPOSITORIO = MEMORIA · ESPECIFICACIÓN VIGENTE = FUENTE OPERATIVA.**

Cada agente termina cada etapa importante con este bloque, como lo último de su respuesta en el chat. No se escribe en el archivo de la tarea. Señala dónde está el contexto; no lo copia. Objetivo: 100–200 palabras. Solo se alarga por seguridad, migración, incidente o ambigüedad de arquitectura.

Etapas importantes: especificación lista, informe del ejecutor, auditoría, revisión del arquitecto, `SPEC_AMENDMENT`, `ARCHITECTURE_CONFLICT`, pruebas humanas, cierre y cualquier parada que necesite al dueño.

## Hacia un agente
```
HANDOFF
TASK: <TASK_ID>
STATUS: <STATUS (y ronda)>
NEXT: <EXECUTOR | AUDITOR | CLAUDE> (<modelo>, conversación nueva si aplica)
BASE: <commit base> · <commit a auditar o último auditado, si aplica>
AUDIT_LEVEL: <QUICK | STANDARD | DEEP>
READ:
- AGENTS.md · agentes/roles/<rol>.md
- tareas/activas/<archivo>.md → ESPECIFICACIÓN VIGENTE
- <último informe relevante, si aplica>
DO:
<1–3 frases>
RETURN:
<qué entrega y dónde>
```
Lo que va en READ no se resume en DO. No se manda a leer un `SPEC_AMENDMENT` ya incorporado a la ESPECIFICACIÓN VIGENTE salvo por una razón explícita.

## Hacial dueño
Sin prompt para pegar.
```
HANDOFF
TASK: <TASK_ID>
STATUS: <STATUS>
NEXT: OWNER
DO:
1. <dónde entrar, qué tocar>
2. …
EXPECTED: <qué debe ver; qué es PASSED y qué es FAILED>
REPORT: <qué responder>
```
Las pruebas humanas complejas van una por una. Si el dueño debe abrir otro agente, DO dice cuál y en qué conversación, y el bloque "Hacia un agente" va debajo para que lo pegue.

## Quién sigue (RULES §12)
| Quién termina | Caso | NEXT |
|---|---|---|
| Claude | Tarea `SPEC_READY`, corrección decidida tras un `REJECTED` o `SPEC_AMENDMENT` aprobado | EXECUTOR |
| Claude | Falta un "dale", una decisión o pruebas humanas | OWNER |
| Ejecutor | Commit hecho con su informe, `STATUS: AWAITING_AUDIT` | AUDITOR (conversación nueva) |
| Ejecutor | `ARCHITECTURE_CONFLICT`, contradicción, decisión necesaria, `PARTIAL`/`BLOCKED`, `DISPUTED` | CLAUDE |
| Auditor | Cualquier veredicto: **siempre** | CLAUDE (nunca directo al ejecutor) |

## Ejemplos
Claude → ejecutor:
```
HANDOFF
TASK: TASK-XXX
STATUS: SPEC_READY
NEXT: EXECUTOR (Codex Medium)
BASE: <hash>
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agentes/roles/executor.md
- tareas/activas/TASK-XXX-<slug>.md → ESPECIFICACIÓN VIGENTE
DO:
Implementa solo la especificación vigente y corre las pruebas que define. Sin push ni REAL.
RETURN:
Informe en la tarea + commit hecho (sin "dale", D47); hash en el HANDOFF.
```

Ejecutor → auditor (solo datos para ubicar la auditoría; nada de opiniones sobre el propio trabajo):
```
HANDOFF
TASK: TASK-XXX
STATUS: AWAITING_AUDIT · ronda N
NEXT: AUDITOR (<modelo según AUDIT_LEVEL>, conversación NUEVA)
BASE: <base> · auditar: <commit del ejecutor> · auditado antes: <hash o "ninguno">
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agentes/roles/auditor.md
- tareas/activas/TASK-XXX-<slug>.md → ESPECIFICACIÓN VIGENTE y el último informe del ejecutor
DO:
Audita el diff real contra la especificación vigente. No implementes.
RETURN:
AUDIT_REPORT compacto en la tarea + commit hecho (sin "dale", D47). NEXT: CLAUDE.
```

Auditor → Claude:
```
HANDOFF
TASK: TASK-XXX · ronda N
NEXT: CLAUDE
VERDICT: APPROVED | REJECTED | ARCHITECTURE_CONFLICT
FINDINGS: <solo los IDs y severidades; el detalle está en el AUDIT_REPORT>
READ: tareas/activas/TASK-XXX-<slug>.md → AUDIT_REPORT · ronda N
```

Ningún bloque lleva tokens, llaves, correos, IDs personales ni datos de clientes.
