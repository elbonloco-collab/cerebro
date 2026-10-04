---
type: synthesis
---
# LLM Wiki supera a RAG para conocimiento de largo plazo

> Sources: Andrej Karpathy (gist), 2026-04-04
> Wiki pages: [Patrón LLM Wiki](concept-llm-wiki-pattern.md); [Base de Conocimiento Compuesta](concept-compounding-knowledge-base.md); [Andrej Karpathy](../personas/entity-andrej-karpathy.md)
> Updated: 2026-10-04

<!-- Nota: se usa "Wiki pages:" (no "Raw:") porque las síntesis razonan sobre la wiki misma. -->

## Claim

Para conocimiento que se acumula a lo largo del tiempo, una wiki persistente mantenida por un LLM
**supera a RAG**, porque compila el conocimiento una vez y lo mantiene vigente en lugar de re-derivarlo
en cada consulta.

## Supporting Evidence

- [Patrón LLM Wiki](concept-llm-wiki-pattern.md) — la arquitectura de capas raw/wiki/schema y las operaciones INGEST/QUERY/LINT producen memoria compilada, no recuperación repetida.
- [Base de Conocimiento Compuesta](concept-compounding-knowledge-base.md) — el valor crece con cada fuente porque el *bookkeeping* es casi gratis para el LLM.
- [Andrej Karpathy](../personas/entity-andrej-karpathy.md) — autor del gist que articula el patrón.

## Caveats & Counterarguments

- RAG sigue siendo más simple de arrancar cuando las fuentes son muchas, heterogéneas y desechables.
- El patrón depende de la calidad del **schema** y de la disciplina del LLM; un schema pobre produce una wiki inconsistente.
- A gran escala (miles de fuentes) el `index.md` puede no bastar y se necesita búsqueda dedicada (p. ej. **qmd**, híbrida BM25/vectorial).
- Las afirmaciones de la wiki deben poder auditarse contra `raw/`; el **LINT** es la salvaguarda.

## See Also

- [Patrón LLM Wiki](concept-llm-wiki-pattern.md)
- [Base de Conocimiento Compuesta](concept-compounding-knowledge-base.md)
