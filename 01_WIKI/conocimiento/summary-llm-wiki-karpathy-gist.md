---
type: summary
---
# Summary: LLM Wiki (Karpathy Gist)

> Sources: Andrej Karpathy (gist), 2026-04-04
> Raw: [2026-04-04-llm-wiki-karpathy-gist.md](../raw/llm-wiki/2026-04-04-llm-wiki-karpathy-gist.md)
> Updated: 2026-10-04

## Overview

El gist propone un patrón para construir bases de conocimiento personales con LLMs: en lugar de
recuperar fragmentos de documentos crudos en el momento de la consulta (RAG), el LLM **construye y
mantiene de forma incremental una wiki persistente** —una colección estructurada e interconectada de
archivos Markdown que se sitúa entre el usuario y las fuentes crudas—. El conocimiento se compila
una vez y **se mantiene vigente**, en vez de re-derivarse en cada pregunta. Es el documento
fundacional que CEREBRO adopta como modelo de conocimiento.

## Key Points

- RAG re-descubre el conocimiento desde cero en cada consulta; no hay acumulación.
- La wiki es un **artefacto persistente y compuesto**: cross-references ya presentes, contradicciones ya marcadas, síntesis ya incorporada.
- Tres capas: (1) fuentes crudas **inmutables**, (2) la wiki Markdown que el LLM posee y escribe, (3) el **schema** (documento de configuración que guía al LLM).
- Tres operaciones: **Ingest** (procesar una fuente → summary + entidades + conceptos + síntesis + índice + log; ~10-15 páginas), **Query** (responder con citas; las buenas respuestas se archivan), **Lint** (health-check).
- Dos archivos especiales: `index.md` (catálogo orientado a contenido) y `log.md` (cronológico, append-only y parseable).
- El humano cura fuentes, dirige el análisis y pregunta; el LLM hace el *bookkeeping*.
- Obsidian como visor; la wiki "es solo un repo git de archivos markdown".
- En espíritu se relaciona con el **Memex** de Vannevar Bush (1945): lo no resuelto era quién hace el mantenimiento.

## Entities Mentioned

- [Andrej Karpathy](../personas/entity-andrej-karpathy.md) — autor del gist que articula el patrón.
- (Mencionados sin página aún: **Obsidian** — visor recomendado; **qmd** — buscador local opcional.)

## Concepts Discussed

- [Patrón LLM Wiki](../conceptos/concept-llm-wiki-pattern.md) — las 3 capas y las 3 operaciones.
- [Base de Conocimiento Compuesta](../conceptos/concept-compounding-knowledge-base.md) — por qué la wiki compone valor frente a RAG.

## See Also

- [LLM Wiki supera a RAG para conocimiento de largo plazo](../conceptos/synthesis-llm-wiki-beats-rag.md)
