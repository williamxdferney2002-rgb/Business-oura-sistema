# Oura · Un emprendimiento gestionado desde Telegram, construido con un equipo de agentes de IA

> Registro público y anonimizado de cómo una sola persona, sin equipo de desarrollo, reemplazó el Excel de su negocio por un sistema propio (app interna + bot de Telegram) usando tres agentes de IA con roles separados: uno que **planea**, otro que **implementa** y otro, independiente, que **audita**.

**Oura** es un pequeño negocio de reventa en Colombia, con dos socios al 50 %: compran productos (sobre todo en Shein) y los venden a clientes que pagan de contado o por abonos. Durante años todo se llevó en un Excel con macros: compras, inventario, ventas, abonos, deudas, gastos y reparto de ganancias. Este repositorio cuenta cómo se construyó el sistema que lo reemplazó y deja las piezas para que otro emprendimiento lo replique.

> Este repo no contiene el código de producción ni ningún dato real. Contiene la **metodología**, la **arquitectura**, la **bitácora** del proyecto y las **plantillas** del sistema multiagente, listas para copiar. Ver [PRIVACIDAD.md](PRIVACIDAD.md).

## Qué hace hoy el sistema

| Pieza | Qué hace | Estado (nov-2026) |
|---|---|---|
| **App interna** (Google Apps Script sobre Google Sheets) | Compras, inventario en vivo, ventas, abonos repartidos entre ventas, cobros, salidas de inventario, anulaciones con historial, estado de cuenta y factura en PDF/imagen para el cliente | En producción |
| **Bot de Telegram** (n8n) en el grupo de los socios | Registra **compras de Shein con un pantallazo**, **abonos con la foto del comprobante o una nota de voz**, **ventas y gastos por texto o voz**, consultas de deuda, seguimiento de pedidos y deshacer. Siempre con vista previa y botón **Confirmar** | En producción |
| **Web de catálogo con stock en vivo** | Mostrar lo disponible ahora, nuevos ingresos y "por encargo", con carrito que termina en WhatsApp | Planeada (Fase 7) · [ver diseño](docs/06-web-y-stock.md) |
| **WhatsApp con clientes** | Recibir pedidos y pasarlos al grupo para que un socio confirme | Planeada (Fase 8) |
| **Dashboard** (Looker Studio) | Ventas, deudores, ganancia por socio, lo no vendido | Planeada (Fase 9) |

## Cifras del proyecto

- **Duración:** del 4-oct-2026 (primer commit) al 4-nov-2026 (app y bot completos en producción el 2-nov) · 25 días con trabajo.
- **~360 commits** y **31 tareas** especificadas, cada una con su especificación, informe de implementación y auditoría en un solo archivo.
- **~1.050 comprobaciones automáticas** que corren fuera de Google (reglas de negocio, sincronizador, pantallas en Chromium a 390 y 1366 px).
- **Infraestructura: $0/mes.** Capas gratuitas de Google Cloud, Google Workspace personal, n8n autoalojado e IA con cuotas gratuitas. El único gasto son las suscripciones de los asistentes de IA usados para construir.

## La idea central en una imagen

```
                  ┌──────────── el dueño (aprueba especificaciones, instala y prueba en el celular)
                  ▼
   ARQUITECTO (Claude Code) ── especificación ──► EJECUTOR (Codex) ── commit + informe ──► AUDITOR (conversación NUEVA)
          ▲                                                                                   │
          └───────────────────────── APPROVED / REJECTED + incidencias ───────────────────────┘

   Memoria compartida = archivos Markdown del repo (plan, decisiones, una tarea = un archivo).
   El prompt solo señala qué leer: PROMPT = ÍNDICE · REPOSITORIO = MEMORIA.
```

## Documentación

| # | Documento | Para qué |
|---|---|---|
| 1 | [Arquitectura](docs/01-arquitectura.md) | Cómo está construido: Sheets como base de datos, un solo escritor, IA que propone y código que calcula, seguridad |
| 2 | [Sistema multiagente](docs/02-sistema-multiagente.md) | Roles, protocolo, estados de una tarea, handoff, niveles de auditoría y cómo evolucionó |
| 3 | [Herramientas](docs/03-herramientas.md) | Todo lo que se usó y para qué: Claude Code, Codex, skills, n8n, Apps Script, Gemini, Groq, Playwright… |
| 4 | [Bitácora](docs/04-bitacora.md) | Qué se hizo, en qué orden y qué se aprendió (se sigue actualizando) |
| 5 | [Cómo replicarlo](docs/05-replicar.md) | Guía paso a paso para montar lo mismo en otro emprendimiento que registre desde Telegram |
| 6 | [Web con stock en vivo](docs/06-web-y-stock.md) | La ambición de la web, el problema de los tiempos de respuesta y cómo se piensa resolver |
| — | [Plantillas](plantillas/) | Reglas, roles y formatos (TASK, HANDOFF, informes) del sistema multiagente, listos para copiar |

## Cómo se mantiene este repo

Esta carpeta es la **versión pública** del proyecto, separada del repositorio privado. Cada vez que se cierra una tarea o una fase:

1. Se agrega una entrada a [docs/04-bitacora.md](docs/04-bitacora.md) (qué se hizo y qué se aprendió, sin datos).
2. Se corre el verificador de privacidad: `python verificar_privacidad.py` debe terminar en `Resultado: 0 hallazgos.`
3. Solo entonces se hace commit y push.

## Licencia

Documentación y plantillas bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es): úsalas, adáptalas y cita la fuente.
