# _SISTEMA — Capa de control de CEREBRO

Esta carpeta contiene la **capa schema** del patrón LLM Wiki de Karpathy: los documentos que definen
cómo está estructurado CEREBRO, cuáles son sus reglas y cuál es su estado.

| Archivo | Rol |
|---------|-----|
| `SCHEMA.md` | **Contrato del sistema.** Estructura, tipos de página, operaciones (INGEST/QUERY/LINT/ACT) y convenciones. Es el archivo que el LLM lee primero. |
| `REGLAS.md` | Reglas operativas del sistema (qué se puede y qué no). |
| `ESTADO.md` | Estado actual de construcción de CEREBRO. |
| `INDICE.md` | Mapa de `_SISTEMA` y de la estructura de primer nivel. |
| `plantillas/` | Plantillas exactas de cada tipo de página (raw, summary, entity, concept, comparison, synthesis, archive, index). |

La raíz del repositorio tiene además `AGENTS.md`, un puntero corto que envía a los agentes aquí.
