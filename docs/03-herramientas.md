# 3 · Herramientas

## Para construir (agentes)
| Herramienta | Uso en el proyecto |
|---|---|
| **Claude Code** (app de escritorio y terminal) | Arquitecto: plan maestro, especificaciones, revisión de auditorías, guías de instalación. Lee `CLAUDE.md`, que importa `AGENTS.md` y fija su rol. Usa *skills*, *hooks* (al iniciar sesión instala dependencias de prueba) y memoria persistente de preferencias del dueño |
| **Codex CLI** (OpenAI) | Ejecutor y auditor. Lee `AGENTS.md` solo. Claude lo lanza con `codex exec` en conversaciones separadas |
| **Skills** (`.claude/skills/<nombre>/SKILL.md`) | Instrucciones empaquetadas que cualquier modelo puede leer por ruta. 32 instaladas el día 1, registradas con versión en un `skills-lock.json` |
| **Git** | Cada etapa de cada tarea es un commit (`TASK-XXX: especificación | entrega | auditoría N | cierre`). Es la evidencia de qué revisó cada auditor |

### Skills usadas
| Skill | Origen | Para qué |
|---|---|---|
| n8n oficiales (14: ciclo de vida, nodos, expresiones, nodos Code, errores, agentes, binarios, subflujos, credenciales…) | `n8n-io/skills` | Construir y revisar flujos con criterio del fabricante |
| Complementos de n8n (patrones, JavaScript, autoalojado…) | `czlonkowski/n8n-skills` | Cuando la oficial no alcanza |
| `google-apps-script` | `jezweb/claude-skills` | Patrones de Apps Script |
| `frontend-design`, `webapp-testing`, `theme-factory` | `anthropics/skills` | Interfaz y pruebas en navegador |
| `grilling` / `grill-me` | `mattpocock/skills` | Entrevista por rondas para cerrar decisiones antes de especificar |
| `auditar-entrega` | Propia | Modo A (autoauditoría del ejecutor) y modo B (auditoría independiente) |
| `auditoria-proyecto` | Propia | Auditoría completa del proyecto, solo a pedido |
| `n8n-workflow-check` | Propia | Revisión estática de flujos exportados + simulador de nodos Code sin n8n |

## Para el sistema
| Herramienta | Uso |
|---|---|
| **Google Sheets** | Base de datos: unas 20 pestañas generadas por un script de Python (productos, variantes, compras, ventas, abonos, clientes, socios, config, auditoría…) |
| **Google Apps Script** | App interna (HTML + `google.script.run`), funciones `api_*` que también llama el bot, PDF armado en el servidor con `Utilities`, copia nocturna |
| **clasp** + sincronizador propio | El código llega a la copia de PRUEBA con un comando que exige: identidad del proyecto aprobada, árbol limpio, lista cerrada de archivos, confirmación escrita "PRUEBA" y verificación después del envío. No existe comando para el Sheet real: ese se actualiza a mano |
| **n8n** (autoalojado, Docker) | Flujos: entrada del bot, errores, salud (recordatorio diario). Se generan con un script de Python y se entregan con `active: false` |
| **Google Cloud** e2-micro + **Caddy** | Servidor gratuito con HTTPS automático y swap de 2 GB para que n8n quepa en 1 GB de RAM |
| **Telegram Bot API** | Grupo de los socios; botones Confirmar / Cancelar / Deshacer; mensajes en HTML |
| **Gemini** (Google AI Studio, nivel gratuito) | Lee pantallazos de pedidos de Shein y comprobantes de pago; interpreta texto libre |
| **Groq** (Whisper) | Transcribe notas de voz; números dichos en palabras ("cincuenta mil") los convierte el código |
| **Gemma** | Respaldo cuando Gemini responde 503 por alta demanda |
| **Google Drive** | Capturas de cada pedido ("PED### parte N") y comprobantes |
| **Looker Studio** | Dashboard (pendiente) |

## Para probar fuera de Google
| Herramienta | Uso |
|---|---|
| **Node.js** + un *mock* de Apps Script | Corre las funciones del servidor en el computador; cuenta las idas al Sheet como medida de velocidad |
| **Playwright + Chromium** | Abre la app a 390 px (celular) y 1366 px, prueba doble toque y que cargue la letra |
| **Python** | Revisión estática de flujos n8n (zona horaria, `parse_mode`, versiones de nodo, una sola lectura de la hoja) |
| Simulador de nodos Code | Ejecuta el JavaScript de un nodo con casos válidos, inválidos y duplicados sin abrir n8n |

## Para planear y documentar
- **Plan maestro** en Markdown con requisitos numerados (R01–R62) marcados por origen: lo dijo el dueño, sale del Excel, o propuesta de la IA (requiere aprobación).
- **Excalidraw** para el diagrama del sistema (hecho / en prueba / falta).
- **Registro de decisiones** (D1…D47) con fecha, motivo, alternativas y quién aprobó.
