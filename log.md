# log.md — Cronología de CEREBRO

> Log **append-only** (nunca se edita el pasado; solo se añade al final).
> Cada entrada empieza con `## [YYYY-MM-DD] <op> | <título>`.
> `<op>` = ingest · query · lint · act · project · task · decision · rule · workflow · state · event.
> Parseable: `grep "^## \[" log.md | tail -5`.

## [2026-10-04] ingest | Summary: LLM Wiki (Karpathy Gist)

<!-- Step 0 — takeaways surfaced antes de escribir:
  1. Claim central: la wiki mantenida por LLM supera a RAG porque el conocimiento
     se compila una vez y se mantiene vigente, en vez de re-derivarse en cada consulta.
  2. Entidades clave: Andrej Karpathy (autor), Obsidian (visor), qmd (búsqueda opcional).
  3. Páginas existentes afectadas: ninguna — primer ingest.
  Páginas a crear: summary, entity (Karpathy), 2x concept, 1x synthesis.
-->

- Created: Summary: LLM Wiki (Karpathy Gist)
- Created: Andrej Karpathy (entity)
- Created: Patrón LLM Wiki (concept)
- Created: Base de Conocimiento Compuesta (concept)
- Created: LLM Wiki supera a RAG para conocimiento de largo plazo (synthesis)

## [2026-10-04] project | Producción de Eva (ejemplo)
- Creado `02_OPERACIONES/proyectos/project-eva-produccion.md`; usa el workflow de música.

## [2026-10-04] decision | Workflow de música para proyectos nuevos (ejemplo)
- Creada la decisión; enlaza el workflow de producción de música.

## [2026-10-04] rule | Usar el workflow de música en proyectos nuevos (ejemplo)
- Creada la regla derivada de la decisión.

## [2026-10-04] event | Se acabó el café (ejemplo)
- EVENTO: se registra **solo aquí**. Los eventos no tienen página ni carpeta.
