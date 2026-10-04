# AGENTS.md — Contrato para agentes (CEREBRO)

Este repositorio implementa el patrón **LLM Wiki de Karpathy** adaptado a CEREBRO.
La memoria es Markdown; el LLM escribe y mantiene la Wiki, el humano cura fuentes y pregunta.

Antes de operar, **lee y sigue**:

- `_SISTEMA/SCHEMA.md` — esquema, tipos de página, convenciones y operaciones INGEST/QUERY/LINT/ACT.
- `_SISTEMA/plantillas/` — plantillas exactas de cada tipo de página.
- `_SISTEMA/REGLAS.md` — reglas del sistema.

## Reglas rápidas

- Memoria = Markdown. **Nunca edites `raw/`** (fuentes inmutables).
- Cada operación de escritura actualiza `index.md` y añade una entrada a `log.md`.
- Cada página (excepto `index.md` y `log.md`) lleva frontmatter `type:`
  (`summary` | `entity` | `concept` | `comparison` | `synthesis` | `archive`).
- Cada entrada de log: `## [YYYY-MM-DD] <op> | <título>`.
- Enlaces relativos dentro de `01_WIKI/`; los nombres de archivo siguen
  `summary-*`, `entity-*`, `concept-*`, `comparison-*`, `synthesis-*`, `archive-*`.
- Sé económico en tokens: no cargues toda la Wiki; usa el índice para localizar páginas.
