---
type: concept
---
# Patrón LLM Wiki

> Sources: Andrej Karpathy (gist), 2026-04-04
> Raw: [2026-04-04-llm-wiki-karpathy-gist.md](../raw/llm-wiki/2026-04-04-llm-wiki-karpathy-gist.md)
> Updated: 2026-10-04

## Overview

El **Patrón LLM Wiki** es una forma de construir bases de conocimiento personales en la que un LLM
construye y mantiene incrementalmente una wiki persistente —una colección estructurada e
interconectada de archivos Markdown— que se sitúa entre el usuario y las fuentes crudas. Sustituye la
recuperación en tiempo de consulta (RAG) por **memoria compilada y mantenida**.

## Las tres capas

1. **Fuentes crudas (`raw/`)** — colección curada de documentos fuente (artículos, papers, imágenes, datos). Son **inmutables**: el LLM las lee pero nunca las modifica. Es la fuente de verdad.
2. **La wiki (`wiki/`)** — archivos Markdown generados por el LLM: resúmenes, páginas de entidad y concepto, comparaciones, una visión general y síntesis. El LLM posee esta capa por completo: crea y actualiza páginas, mantiene cross-references y consistencia. **El humano la lee; el LLM la escribe.**
3. **El schema** — un documento (p. ej. `AGENTS.md`/`CLAUDE.md`) que dice al LLM cómo está estructurada la wiki, cuáles son las convenciones y qué workflows seguir. Es el archivo de configuración clave: convierte al LLM en un mantenedor disciplinado en vez de un chatbot genérico. Humano y LLM lo co-evolucionan.

## Las tres operaciones

- **INGEST** — se añade una fuente a `raw/` y se pide al LLM procesarla: lee, discute takeaways, escribe un resumen, actualiza el índice y las páginas de entidad/concepto, y añade una entrada al log. Una sola fuente puede tocar **10–15 páginas**.
- **QUERY** — se pregunta contra la wiki; el LLM busca páginas relevantes, las lee y sintetiza una respuesta con citas. Las buenas respuestas pueden **archivarse de vuelta** como páginas nuevas.
- **LINT** — health-check periódico: contradicciones entre páginas, afirmaciones obsoletas, páginas huérfanas, conceptos importantes sin página propia, cross-references faltantes y vacíos de datos.

## Los dos archivos especiales

- **`index.md`** — orientado a **contenido**: catálogo de la wiki; cada página con enlace, resumen de una línea y metadatos. Se actualiza en cada ingest. Funciona bien a escala moderada (~100 fuentes) y evita infraestructura RAG con embeddings.
- **`log.md`** — **cronológico**: registro append-only de qué ocurrió y cuándo (ingests, queries, lints). Con un prefijo consistente es parseable con herramientas unix: `grep "^## \[" log.md | tail -5`.

## División humano / LLM

- **Humano:** curar fuentes, dirigir el análisis, preguntar, pensar el significado.
- **LLM:** resumir, cross-referenciar, archivar, *bookkeeping*, mantener consistencia.

## See Also

- [Base de Conocimiento Compuesta](concept-compounding-knowledge-base.md)
- [LLM Wiki supera a RAG para conocimiento de largo plazo](synthesis-llm-wiki-beats-rag.md)
- [Andrej Karpathy](../personas/entity-andrej-karpathy.md)
