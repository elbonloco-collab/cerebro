---
type: archive
---
# CEREBRO OS — MASTER AUDIT

> Sources: [MVP operativo](../../CEREBRO_MVP_MARKDOWN_OPERATIVO.md); inspección de solo lectura de `/srv/cerebro` y del runtime del servidor.
> Archived: 2026-10-08

## Overview

Al 2026-10-08, CEREBRO tiene una Wiki Markdown con ejemplos operativos y un bot de Telegram en ejecución que captura y clasifica mensajes en `00_INBOX`. No está completo el flujo del MVP: no hay herramienta Python que procese aprobaciones hacia `02_OPERACIONES`, ni implementación de QUERY o ACT. La evidencia siguiente distingue documentación, código y observación del sistema. La inspección no modificó archivos del servidor y no reproduce contenido personal ni secretos.

## 1. REAL CURRENT STATE

- **Documentación:** `/srv/cerebro/CEREBRO_MVP_MARKDOWN_OPERATIVO.md` es la fuente rectora. Su contenido coincide por SHA256 con la copia del workspace. Enumera doce pasos; el Paso 12 es probar proyectos, tareas, decisiones y workflows.
- **Código:** `/srv/cerebro/_AUTOMATIZACIONES/telegram/bot.py` implementa recepción Telegram, captura en Inbox, clasificación y respuestas. No implementa el puente de aprobación a Operaciones.
- **Sistema real:** se observó un proceso `python3` cuyo comando apunta al bot; Ollama está activo y hay sockets locales en 11434 y 49374. Los logs contienen actividad anterior de clasificación y respuestas.
- **Conclusión:** el canal de captura está operativo, pero la memoria operativa aún depende de edición manual. No se verificó una sesión nueva con Telegram durante esta auditoría.

## 2. MVP 12-STEP STATUS

| Paso | Requisito del MVP | Estado | Evidencia |
|---|---|---|---|
| 1 | Crear estructura física | IMPLEMENTADO | Directorios de Wiki, Operaciones, Inbox, sistema y proyectos presentes en `/srv/cerebro`. |
| 2 | Crear `SCHEMA.md` | IMPLEMENTADO | `/srv/cerebro/_SISTEMA/SCHEMA.md` y plantillas presentes. |
| 3 | Crear `REGLAS.md` | IMPLEMENTADO | `/srv/cerebro/_SISTEMA/REGLAS.md` presente. |
| 4 | Crear Markdown reales de prueba | IMPLEMENTADO | Proyecto Eva, decisión, regla y workflow con `ejemplo: true`. |
| 5 | Configurar Obsidian | IMPLEMENTADO | `.obsidian/` y configuración del vault presentes; no se observó un proceso Obsidian activo. |
| 6 | Conectar Telegram | IMPLEMENTADO | Unidad configurada, proceso Python activo, bot usa `getUpdates` y `ia.log` conserva actividad Telegram. Conectividad en el instante de la auditoría: NO CONFIRMADO. |
| 7 | Conectar Donna/Gemma | IMPLEMENTADO | Código consulta Ollama; servicio activo, modelo disponible y modelo anotado en logs. |
| 8 | Crear herramientas Python mínimas | PENDIENTE | No existe `ingest_inbox.py` ni herramienta equivalente de crear/validar/buscar Operaciones. Ver sección 3. |
| 9 | Probar captura → clasificación → Markdown | PARCIAL | Captura y clasificación escriben Markdown en Inbox; no se completa la escritura operativa requerida. |
| 10 | Probar QUERY | PENDIENTE | Está descrito en schema, pero no hay consulta implementada por el bot. |
| 11 | Probar ACT | PENDIENTE | No hay código que aplique cambios a estados, reglas o compras. |
| 12 | Probar proyectos, tareas, decisiones y workflows | PARCIAL | Hay ejemplos Markdown; no hay flujo integrado Donna → Python → Operaciones que cumpla el criterio de aceptación. |

La lista oficial de pasos está en el MVP, sección 28. Los criterios de implementación y pendientes adicionales están en `/srv/cerebro/_SISTEMA/ESTADO.md`, líneas 26–46.

## 3. STEP 8 STATUS

El MVP pide “Crear herramientas Python mínimas”. El estado del sistema detalla el criterio: `ingest_inbox.py` debe leer `00_INBOX/`, clasificar y escribir Markdown en `02_OPERACIONES/` o `01_WIKI/`, actualizando `index.md` y `log.md` (`/srv/cerebro/_SISTEMA/ESTADO.md`, líneas 35–36).

Inventario de `/srv/cerebro/_AUTOMATIZACIONES/`:

- Existe `telegram/bot.py`.
- `scripts/` y `tools/` solo tienen `.gitkeep`.
- No existen `ingest.py`, `ingest_inbox.py`, `query.py`, `lint.py` ni `act.py`.
- La unidad `cerebro-bot.service` ejecuta solamente `telegram/bot.py`.
- No se encontraron otros scripts Python del MVP ni tests asociados en el árbol del servidor.

**Conclusión: Paso 8 PENDIENTE.** El bot sí automatiza captura y clasificación, pero no satisface el criterio de procesar datos aprobados ni de mantener la Wiki/Operaciones.

## 4. TELEGRAM/DONNA STATUS

| Etapa | Estado | Evidencia y límite |
|---|---|---|
| Telegram → bot | IMPLEMENTADA | La unidad apunta a `/srv/cerebro/_AUTOMATIZACIONES/telegram/bot.py`; proceso activo y llamadas registradas. Conectividad en vivo al momento de la auditoría: NO CONFIRMADO. |
| Bot → `00_INBOX` | IMPLEMENTADA | `guardar()` crea Markdown con metadatos; Inbox contiene capturas. |
| Clasificación | IMPLEMENTADA | `clasificar()` llama al endpoint local de Ollama con `gemma4:e2b-it-qat`; log contiene eventos `clasificar`. |
| Respuesta de charla | IMPLEMENTADA | El código usa OpenCode y, como respaldo, Gemma; log registra ambas vías. |
| Aprobación con botones | NO IMPLEMENTADA | No hay `reply_markup`, teclado inline ni `callback_query`; el bot recibe solo updates `message`. |
| Escritura en `02_OPERACIONES` | NO IMPLEMENTADA | El bot actualiza frontmatter en Inbox, pero no escribe páginas operativas. |
| Adjuntos | PARCIAL | Fotos/documentos/voz/video se descargan a `00_INBOX/adjuntos`; no se encontró pipeline de transcripción o clasificación del contenido del adjunto. |
| Logging | IMPLEMENTADO | `/srv/cerebro/_SISTEMA/logs/ia.log` existe y contiene eventos de clasificación, respuesta y adjuntos. |

Flujo reconstruido: `Telegram → bot.py → Inbox Markdown → Ollama clasifica → respuesta Telegram`. La salida hacia Markdown de Operaciones **no existe**.

La unidad referencia `/home/bismarck/.config/cerebro/bot.env`; el archivo existe. El bot lee variables como `TELEGRAM_BOT_TOKEN`, `CEREBRO_OWNER_ID`, `CEREBRO_MODELO`, `CEREBRO_OLLAMA` y `CEREBRO_OPENCODE_MODELO`. No se inspeccionaron sus valores.

## 5. WIKI STATUS

- `index.md` y `log.md` están en la raíz de `/srv/cerebro`; `index.md` lista páginas de Wiki y ejemplos de Operaciones.
- `01_WIKI/` contiene `raw/`, conocimiento, personas, conceptos, herramientas y referencias. Hay además archivos sin título y `.trash/`.
- Existe una fuente raw de Karpathy y páginas de summary/entity/concept/synthesis.
- `_SISTEMA/plantillas/`, `SCHEMA.md`, `REGLAS.md` y `DONNA.md` existen.
- **Documentación:** schema define INGEST, QUERY, LINT y ACT.
- **Código:** el bot no consulta el índice ni implementa esas cuatro herramientas de Wiki.
- El índice y log del servidor están modificados respecto a Git; además, el diff muestra cambios en el archivo raw. Esto contradice las reglas de inmutabilidad de `raw/` y de log append-only. No se alteró ni corrigió nada durante la auditoría.

## 6. OPERATIONS STATUS

Presentes: `tareas.md`, `estados.md`, `compras.md`, carpetas `proyectos/`, `decisiones/`, `reglas/` y `workflows/`, con ejemplos reales de estructura.

Capacidad automatizada de Python para `02_OPERACIONES`:

| Acción | Estado | Motivo |
|---|---|---|
| Crear | NO IMPLEMENTADA | No hay herramienta que genere una página operativa. |
| Validar | NO IMPLEMENTADA | No hay validador de frontmatter, esquema ni enlaces. |
| Buscar | NO IMPLEMENTADA | No hay buscador/QUERY implementado para las notas operativas. |
| Actualizar | NO IMPLEMENTADA | No hay escritor que cambie listas/notas y mantenga índice/log. |

El bot sí crea y actualiza archivos de **Inbox**, pero esto no equivale a operar sobre `02_OPERACIONES`.

## 7. PYTHON STATUS

No se ejecutaron scripts. Entradas y salidas se deducen del código; fuera del proceso activo del bot, su funcionamiento actual es NO CONFIRMADO.

| Archivo | Propósito | Entrada → salida | Quién lo usa / estado |
|---|---|---|---|
| `/srv/cerebro/_AUTOMATIZACIONES/telegram/bot.py` | Bot Donna: captura, clasifica, responde y guarda adjuntos | Telegram → Inbox, logs y respuestas | Unidad `cerebro-bot.service`; proceso activo. |
| `/home/bismarck/cerebro-bot/bot.py` | Copia anterior del bot, con rutas y configuración diferentes | Telegram → Inbox/log según variables | No es la ruta lanzada por la unidad del servidor; caller actual NO CONFIRMADO. Hash distinto del bot activo. |
| `/home/bismarck/respaldo-estructura-vieja/_sistema/scripts/nueva_sesion.py` | Preparar estructura de canciones, versiones y lanzamientos | Argumentos CLI + plantillas DAW → carpetas y notas musicales | Utilidad del respaldo antiguo; no se encontró caller actual y no se ejecutó. |
| `/home/bismarck/probar2.py` | Prueba manual de clasificación vía Ollama | Modelo + archivo → clasificación impresa y métricas | No se encontró integración con el bot ni caller; estado operativo NO CONFIRMADO. |

Scripts inexistentes en `/srv/cerebro`: `ingest.py`, `query.py`, `lint.py`, `act.py` e `ingest_inbox.py`. No se encontraron tests del MVP en ese árbol.

## 8. DOCKER/SERVICES STATUS

- Docker: cero contenedores en ejecución y cero detenidos; una imagen `hello-world`; no se encontraron archivos Compose.
- `cerebro-bot.service`: unidad de usuario presente y enlazada desde `default.target.wants`; `ExecStart` apunta al bot de `/srv/cerebro`.
- Proceso: `python3` activo, con comando apuntando a `telegram/bot.py`.
- `systemctl --user` no pudo conectar al bus DBus de usuario. Estado reportado por systemd user: **NO CONFIRMADO**.
- `ollama.service`: `active`; puerto local 11434. OpenCode escucha localmente en 49374.
- Obsidian no apareció como proceso en ejecución durante la consulta.

## 9. GIT STATUS

Servidor `/srv/cerebro`: rama `main`, HEAD `bab2c54` (`2026-10-05`, revert de ejemplo de log), sin remotes reportados. El worktree tiene 24 archivos tracked modificados y 53 untracked. El diff indica cambios en raw y en `log.md`, incluyendo líneas eliminadas.

Workspace `/home/bismarck/cerebro-prueba`: rama `main`, un commit local por delante de `origin/main` (`d2b69d5`, proyecto OpenCode de ejemplo), sin cambios tracked y con un directorio untracked. Las URLs de remote no se mostraron.

## 10. DUPLICATES

- `/srv/cerebro`: instalación activa inspeccionada.
- `/home/bismarck/cerebro-prueba`: workspace abierto; MVP idéntico por hash, pero varios documentos del estado/sistema difieren.
- `/home/bismarck/cerebro-bot`: copia distinta de `bot.py`, no es worktree Git.
- `/home/bismarck/respaldo-estructura-vieja`: árbol antiguo no Git con script musical, plantillas y datos de prueba.
- `/srv/cerebro/srv/cerebro/_SISTEMA/`: carpeta anidada con contenido de sistema; no es una copia completa del vault.

No se borró ni cambió ninguna copia.

## 11. INTERFACE STATUS

- **Diseño/configuración:** `.obsidian/` existe y hay configuración de vault.
- **Código Life OS/Dashboard:** no se encontró código frontend (HTML/JS/React/Vue) en los árboles relevantes examinados.
- **Funcionalidad:** Obsidian es la interfaz documental prevista; no se observó el proceso activo. Dashboard propio: NO IMPLEMENTADO según la búsqueda de archivos.

## 12. PRODUCTION ASSISTANT STATUS

Hay una utilidad musical heredada en `respaldo-estructura-vieja/_sistema/scripts/nueva_sesion.py`, con plantillas FL Studio/Ableton y datos de prueba. Es externa al repo actual y usa una estructura antigua (`proyectos/musica`), no el modelo vigente de `02_OPERACIONES`.

Una nota archivada en `/srv/cerebro/01_WIKI/.trash/Auditoria_Production_Assistant.md` describe Producer Pal, Ableton y un asistente TypeScript. Sin embargo, no se encontraron en las rutas examinadas fuentes como `producer-pal-client.ts`, `session-adapter.ts` ni un proyecto TypeScript asociado. Que ese asistente exista actualmente en el servidor, esté ejecutándose o esté integrado con CEREBRO: **NO CONFIRMADO**. La utilidad heredada de sesiones sí está separada del repo CEREBRO actual.

## 13. CONTRADICTIONS

1. **Estructura de índice/log:** el diagrama inicial del MVP coloca `index.md`/`log.md` bajo `01_WIKI`; SCHEMA y ESTADO fijan índices únicos en la raíz. La instalación actual sigue la decisión de índice/log únicos, pero el diagrama no está armonizado.
2. **Ruta raw:** el MVP sitúa `raw/` bajo `01_WIKI`; algunas rutas genéricas del SCHEMA hablan de `<dominio>/raw/`. El árbol real usa `01_WIKI/raw/`.
3. **Nombre Inbox:** `DONNA.md` pide `AAAA-MM-DD-HHMMSS-<id>.md`; el código genera `YYYYMMDD-HHMMSS-<id>.md`.
4. **Mensajes charla:** `DONNA.md` dice que charla no se escribe; el bot guarda primero el mensaje en Inbox y después lo marca como `charla`.
5. **Aprobación:** `ESTADO.md` afirma captura/clasificación aprobada y Donna exige aprobación para Operaciones; el código no contiene botones ni escritura de Operaciones. Una captura con `estado: aprobado` no demuestra que exista ese flujo.
6. **Inmutabilidad:** REGLAS define raw inmutable y log append-only; el estado Git del servidor muestra cambios en raw y modificaciones/eliminaciones en log.

No hay discrepancia en el número de pasos: la fuente rectora contiene 1–12; la lectura inicial de esta auditoría había quedado truncada antes del paso 12 y fue corregida.

## 14. WHAT IS ACTUALLY WORKING

El bot Python está en ejecución; existe su unidad configurada; Ollama está activo; el modelo Gemma requerido está disponible. Logs e Inbox acreditan capturas y clasificaciones previas. La estructura Wiki y los ejemplos de Operaciones están presentes.

Esto verifica captura y clasificación hasta Inbox. No verifica procesamiento en Operaciones ni el éxito de una interacción Telegram nueva durante la auditoría.

## 15. WHAT IS ACTUALLY BROKEN

No se observó un crash del bot ni un fallo de servicio de Ollama. El bloqueo verificable es funcional: el código no implementa aprobación, puente hacia Operaciones, QUERY ni ACT. El estado del bus systemd de usuario y la conectividad Telegram en el instante de la auditoría son **NO CONFIRMADO**.

## 16. WHAT IS NOT IMPLEMENTED

`ingest_inbox.py`/herramientas del Paso 8; aprobación con botones; creación, validación, búsqueda y actualización automática de `02_OPERACIONES`; actualización programática de índice/log; QUERY; LINT; ACT; y el flujo integrado del Paso 12. No se localizó código de Life OS/Dashboard.

## 17. SINGLE NEXT TASK

Implementar **`ingest_inbox.py`**, el criterio explícito del Paso 8: procesar solo capturas aprobadas, crear una nota operativa válida y actualizar el índice y el log. Verificación concreta: una captura aprobada genera una nota enlazada y una captura no aprobada permanece intacta. Esta auditoría no implementa ni ejecuta ese cambio.