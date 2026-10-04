# _SISTEMA — Capa de control de CEREBRO

Esta carpeta contiene la **capa schema** del patrón LLM Wiki de Karpathy: los documentos que definen
cómo está estructurado CEREBRO, cuáles son sus reglas y cuál es su estado.

| Archivo | Rol |
|---------|-----|
| `SCHEMA.md` | **Contrato del sistema.** Estructura, tipos de página, operaciones (INGEST/QUERY/LINT/ACT) y convenciones. Es el archivo que el LLM lee primero. |
| `REGLAS.md` | Reglas operativas del sistema (qué se puede y qué no). |
| `ESTADO.md` | Estado actual de construcción de CEREBRO. |
| `plantillas/` | Plantillas exactas de cada tipo de página (raw, summary, entity, concept, comparison, synthesis, archive, index). |
| `plantillas/operaciones/` | Plantillas de la capa operativa (project, task, decision, rule, workflow, state, purchase). |

La raíz del repositorio tiene además `AGENTS.md`, un puntero corto que envía a los agentes aquí.

## Mapa de CEREBRO

### Primer nivel

| Ruta | Rol | Estado |
|------|-----|--------|
| `README.md` | Presentación del vault | Fase 1 |
| `AGENTS.md` | Contrato corto para agentes | Fase 1 |
| `01_WIKI/` | **Dominio** de conocimiento (raw + wiki) | Fase 1 |
| `_SISTEMA/` | Capa schema | Fase 1 |
| `_AUTOMATIZACIONES/` | scripts / telegram / tools | Fase 2 (esqueleto) |
| `00_INBOX/` | Entrada sin clasificar | Fase 2 (esqueleto) |
| `02_OPERACIONES/` | Capa operativa de CEREBRO (index.md, log.md + tipos) | Fase 2 — activo |
| `03_PROYECTOS/` | Proyectos | Fase 2 (esqueleto) |
| `04_CLIENTES/` | Clientes | Fase 2 (esqueleto) |
| `05_RECURSOS/` | Recursos | Fase 2 (esqueleto) |
| `06_ARCHIVOS/` | Archivos / adjuntos | Fase 2 (esqueleto) |

### Dominio `01_WIKI`

| Ruta | Contenido |
|------|-----------|
| `01_WIKI/raw/` | Fuentes inmutables |
| `01_WIKI/index.md` | Índice del dominio (único índice) |
| `01_WIKI/log.md` | Log append-only ⭐ |
| `01_WIKI/conocimiento/` | summaries |
| `01_WIKI/personas/` | entities (personas) |
| `01_WIKI/conceptos/` | concepts + syntheses |
| `01_WIKI/herramientas/` | entities (tools) |
| `01_WIKI/referencias/` | referencias |

### Capa `02_OPERACIONES`

| Ruta | Contenido |
|------|-----------|
| `02_OPERACIONES/index.md` | Índice de operaciones |
| `02_OPERACIONES/log.md` | Log operativo (append-only) |
| `02_OPERACIONES/proyectos/` | `type: project` |
| `02_OPERACIONES/tareas/` | `type: task` |
| `02_OPERACIONES/decisiones/` | `type: decision` |
| `02_OPERACIONES/reglas/` | `type: rule` |
| `02_OPERACIONES/workflows/` | `type: workflow` |
| `02_OPERACIONES/estados/` | `type: state` |
| `02_OPERACIONES/compras/` | `type: purchase` |
| evento · contexto · acción | entradas en `index.md`/`log.md` (sin carpeta) |
