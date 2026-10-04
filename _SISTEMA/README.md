# _SISTEMA — Capa de control de CEREBRO

Esta carpeta contiene la **capa schema** del patrón LLM Wiki de Karpathy: los documentos que definen
cómo está estructurado CEREBRO, cuáles son sus reglas y cuál es su estado.

| Archivo | Rol |
|---------|-----|
| `SCHEMA.md` | **Contrato del sistema.** Estructura, tipos, operaciones (INGEST/QUERY/LINT/ACT) y convenciones. |
| `DONNA.md` | **Contrato corto (runtime)** para Donna; derivado de `SCHEMA.md`. |
| `REGLAS.md` | Reglas operativas del sistema. |
| `ESTADO.md` | Estado actual de construcción. |
| `plantillas/` | Plantillas de Wiki (raw, summary, entity, concept, comparison, synthesis, archive, index). |
| `plantillas/operaciones/` | Plantillas de operaciones (project, decision, rule, workflow, task). |

La raíz del repositorio tiene además `AGENTS.md`, un puntero corto que envía a los agentes aquí.

## Mapa de CEREBRO

### Primer nivel

| Ruta | Rol |
|------|-----|
| `README.md` | Presentación del vault |
| `AGENTS.md` | Contrato corto para agentes |
| `index.md` | Catálogo único (conocimiento + operaciones) |
| `log.md` | Cronología única (append-only) |
| `01_WIKI/` | Conocimiento (raw + páginas) |
| `02_OPERACIONES/` | Operaciones (notas + archivos-lista) |
| `_SISTEMA/` | Capa schema |
| `00_INBOX/` | Capturas sin clasificar |
| `_AUTOMATIZACIONES/`, `03_PROYECTOS/` … `06_ARCHIVOS/` | fase 3 |

### Conocimiento `01_WIKI`

| Ruta | Contenido |
|------|-----------|
| `01_WIKI/raw/` | Fuentes inmutables |
| `01_WIKI/conocimiento/` | summaries |
| `01_WIKI/personas/` | entities (personas) |
| `01_WIKI/conceptos/` | concepts + syntheses |
| `01_WIKI/herramientas/` | entities (tools) |
| `01_WIKI/referencias/` | referencias |

### Operaciones `02_OPERACIONES`

| Ruta | Contenido |
|------|-----------|
| `02_OPERACIONES/proyectos/` | `type: project` |
| `02_OPERACIONES/decisiones/` | `type: decision` |
| `02_OPERACIONES/reglas/` | `type: rule` |
| `02_OPERACIONES/workflows/` | `type: workflow` |
| `02_OPERACIONES/tareas.md` | tareas sin proyecto (casillas) |
| `02_OPERACIONES/estados.md` | tabla de estados |
| `02_OPERACIONES/compras.md` | lista de compras |