# 2 · Sistema multiagente

## El problema
Un solo asistente de IA que planea, programa y se revisa a sí mismo tiende a darse la razón: declara "probado" lo que no corrió, cambia el alcance sin avisar y olvida decisiones de sesiones anteriores. Con 30 tareas en un mes, eso no escala.

## La solución: tres roles, una memoria en archivos

| Rol | Herramienta | Hace | No hace |
|---|---|---|---|
| **Arquitecto** | Claude Code | Lee el plan y el código, entrevista al dueño, escribe la especificación de cada tarea, clasifica las incidencias de la auditoría, mantiene el estado y las decisiones | No escribe código de producción |
| **Ejecutor** | Codex (nivel Medium; High solo en escalaciones justificadas). Respaldo: una instancia nueva de Claude | Implementa **solo** la especificación vigente, corre las pruebas, se autoaudita, hace un commit con código e informe | No rediseña ni cambia alcance: si la especificación choca con algo, escribe `ARCHITECTURE_CONFLICT` |
| **Auditor** | Una conversación **nueva** e independiente (modelo según el nivel de auditoría) | Revisa el commit real contra la especificación, corre las pruebas, busca regresiones y problemas de seguridad | No corrige código: devuelve las incidencias |

Y por encima, **el dueño**: aprueba cada especificación, decide cuando hay conflicto, instala en Google/n8n y hace las pruebas humanas en el celular.

**Ejecutor y auditor nunca son la misma conversación** y, de preferencia, tampoco el mismo modelo. Esa es la defensa contra el sesgo de autoaprobación.

## Jerarquía de autoridad
```
PLAN MADRE      requisitos R01–R62, fases, seguridad, decisiones fundacionales
   ↓
DECISIONES      D37 en adelante, cada una con fecha, motivo y quién la aprobó
   ↓
TAREA           una especificación por archivo
   ↓
IMPLEMENTACIÓN  código + IMPLEMENTATION_REPORT
   ↓
AUDITORÍA       AUDIT_REPORT
```
Ningún agente contradice un nivel superior en silencio: lo escribe y lo escala.

## Ciclo de vida de una tarea

```
DRAFT ──(aprobación del dueño)──► SPEC_READY ──► IN_PROGRESS ──► AWAITING_AUDIT
                                                                   │
                       ┌───────────── REJECTED ◄───────────────────┤
                       ▼                                           ▼
          arquitecto clasifica:                                 APPROVED
          · corrección → ejecutor → CORRECTION_REPORT              │
          · cambio de especificación → SPEC_AMENDMENT              ▼
                                                          AWAITING_HUMAN (pruebas en el celular)
                                                                   │ PASSED
                                                                   ▼
                                                                 DONE
BLOCKED: conflicto de arquitectura, informe parcial, incidencia disputada o tercer rechazo.
```

Cada tarea vive en **un solo archivo** (`tareas/activas/TASK-XXX-*.md`). Arriba, la `ESPECIFICACIÓN VIGENTE` (la única que se edita); debajo, el historial que cada rol **agrega** y nunca reescribe: especificación original, amendments, informes y auditorías. El que llega después encuentra todo en un lugar.

Campos clave de la especificación ([plantilla](../plantillas/TASK.md)): objetivo, alcance y fuera de alcance, archivos a inspeccionar y a cambiar, pasos, restricciones (contratos que no cambian, velocidad), **criterios de aceptación comprobables sin preguntar a nadie**, pruebas automáticas con el resultado esperado `X/Y`, pruebas humanas y riesgos.

## Handoff: el prompt es un índice
**PROMPT = ÍNDICE · REPOSITORIO = MEMORIA · ESPECIFICACIÓN VIGENTE = FUENTE OPERATIVA.**

Cada agente termina su etapa con un bloque de 100–200 palabras que dice quién sigue, qué leer, qué hacer y qué devolver. No copia la tarea: la señala.

```
HANDOFF
TASK: TASK-XXX
STATUS: AWAITING_AUDIT · ronda 2
NEXT: AUDITOR (conversación NUEVA)
BASE: <commit base> · auditar: <commit del ejecutor>
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agentes/roles/auditor.md
- tareas/activas/TASK-XXX-<slug>.md → ESPECIFICACIÓN VIGENTE y último informe
DO: Audita el diff real contra la especificación vigente. No implementes.
RETURN: AUDIT_REPORT en la tarea + commit. NEXT: CLAUDE.
```

Efecto: cada agente nuevo arranca leyendo 4 archivos, no todo el repositorio. Menos tokens, menos confusión.

## Niveles de auditoría
| Nivel | Cuándo | Auditor |
|---|---|---|
| `QUICK` | Cambios pequeños y de bajo riesgo (un texto, un formato) | Modelo económico |
| `STANDARD` | Lo normal | Claude o Codex en conversación nueva |
| `DEEP` | Dinero, escritura atómica, seguridad, migración | Modelo fuerte |

## Reglas que más pesaron
- **Sin falsos positivos:** prohibido decir "funciona" o "probado" sin evidencia ejecutada en esa sesión (comando y resultado `X/Y`). Lo que no se pudo correr (dentro de Google, Telegram real) se declara en `NOT_EXECUTED`.
- **Cambios mínimos:** solo los archivos que la tarea lista; nada de "mejorar" código vecino.
- **No destruir:** nada se borra sin justificación escrita; nada de `git reset --hard` sobre trabajo sin commit.
- **Un commit por entrega** con código e informe juntos; el auditor revisa exactamente ese hash.
- **Los agentes no tocan producción:** ni Google, ni el sincronizador, ni el Sheet real. Eso lo hace el dueño con una guía paso a paso.
- **Sin push:** el dueño decide cuándo sube la rama.

Texto completo: [plantillas/RULES.md](../plantillas/RULES.md) y [plantillas/roles/](../plantillas/roles/).

## Cómo evolucionó la coordinación
1. **Manual (oct-2026).** El dueño copiaba el handoff de una herramienta a otra: Claude → Codex → Codex nuevo → Claude. Funcionaba, pero cada tarea eran 4–8 copias y pegas.
2. **Orquestador automático (intentado y aplazado).** Se construyó un script en Node que lanzaba procesos efímeros de Codex con permisos de solo lectura y red bloqueada. La prueba inicial demostró que el sandbox nativo de Windows de esa versión no garantizaba la frontera de lectura exigida. Decisión: **no usarlo** hasta que la herramienta lo garantice. Lección: si una frontera de seguridad no se puede demostrar, no existe.
3. **Claude como puente (27-oct-2026).** Claude lanza al ejecutor con `codex exec` y, para cada auditoría, una conversación nueva de Codex. Tras un `REJECTED` relanza la corrección sin esperar al dueño, salvo que cambie el alcance. Máximo 3 rondas por tarea. El dueño solo aprueba especificaciones, instala y prueba.
4. **Sin aprobación por commit (4-nov-2026).** La aprobación de la especificación cubre todos los commits de la tarea. Se muestra un bloque COMMIT como registro (archivos, pruebas, mensaje) y se hace.

## Qué ganó el dueño
- Revisar **especificaciones** en lenguaje claro, no diffs.
- Cada entrega trae: qué cambió, cómo instalarlo en orden exacto, qué revisar y qué pruebas hacer en el celular.
- La separación de roles atrapó problemas antes de llegar al celular: riesgos altos en la generación del PDF del estado de cuenta (la tarea piloto), avisos falsos con doble toque en el bot, un color de texto sin contraste suficiente en los documentos para clientes y funciones que habrían hecho más idas al Sheet de las permitidas.
