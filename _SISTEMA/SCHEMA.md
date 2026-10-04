# SCHEMA.md — Contrato del sistema CEREBRO

> Capa **schema** del patrón LLM Wiki de Karpathy. Este archivo dice al LLM cómo está estructurada la
> Wiki, cuáles son las convenciones y qué workflows seguir. **Humano y LLM lo co-evolucionan.**
> Fuente del patrón: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
> Implementación de referencia: https://github.com/wpzero/karpathy-llm-wiki

---

## 1. Propósito

CEREBRO es un sistema local **file-first**: Markdown es la memoria persistente; **Obsidian** es la
interfaz visual; **Donna** (IA vía Telegram) y la IA de terminal (**Cline**) construyen y mantienen la
Wiki; **Python** ejecuta las automatizaciones. El LLM escribe y mantiene la Wiki; el humano cura
fuentes, dirige el análisis y pregunta.

## 2. Las tres capas

| Capa | Dónde vive | Regla |
|------|-----------|-------|
| **Fuentes crudas** | `<dominio>/raw/<topic>/` | **Inmutable.** El LLM lee, nunca edita. Fuente de verdad. |
| **Wiki** | `<dominio>/<topic>/` | El LLM la posee por completo: crea, actualiza, cross-referencia. |
| **Schema** | `_SISTEMA/SCHEMA.md` (este archivo) | Define estructura, tipos y workflows. |

Plantillas exactas de cada tipo de página: `_SISTEMA/plantillas/`.

## 3. Dominios

Un **dominio** es una carpeta de primer nivel con su propio `raw/`, `index.md` y `log.md`.
En CEREBRO, `01_WIKI` es el dominio de conocimiento inicial.

**Resolución de dominio** (en este orden):
1. El usuario lo nombra explícitamente.
2. Inferido del contexto de la conversación.
3. Si es ambiguo: **preguntar**. Nunca elegir un dominio en silencio cuando hay varios.

## 4. Inicialización

Se dispara solo en el **primer INGEST** de un dominio. Crear únicamente lo que falte; **nunca sobrescribir**:
- `<dominio>/raw/` (+ `.gitkeep`)
- `<dominio>/index.md` — título `# <Dominio> — Base de Conocimiento`, cuerpo vacío
- `<dominio>/log.md` — título `# <Dominio> — Wiki Log`, cuerpo vacío
- `wiki/index.md` — título `# Índice de la Base de Conocimiento — CEREBRO`, si no existe

Si QUERY o LINT no encuentran el dominio: pedir un ingest primero para inicializarlo.

## 5. Tipos de página

Cada archivo de la Wiki **excepto `index.md` y `log.md`** lleva `type:` en su frontmatter:

| `type` | Qué es | Plantilla |
|--------|--------|-----------|
| `summary` | Uno por fuente cruda — destila lo que dice la fuente | `summary-template.md` |
| `entity` | Una por cosa nombrada: persona, org, tool, model, paper, dataset, algorithm, project, event, product, framework, place, ... | `entity-template.md` |
| `concept` | Idea temática sintetizada a través de varias fuentes | `concept-template.md` |
| `comparison` | Evaluación lado a lado de dos o más entidades/conceptos | `comparison-template.md` |
| `synthesis` | Conclusión de orden superior razonada sobre varias páginas | `synthesis-template.md` |
| `archive` | Instantánea de una respuesta de query guardada | `archive-template.md` |

Las páginas `entity` crecen con los años; `summary`/`concept`/`comparison`/`synthesis` se crean en
ingest o query; `archive` solo cuando el usuario guarda una respuesta.

## 6. Operación INGEST

Traer una fuente a `<dominio>/raw/` y **luego** compilarla en `<dominio>/`. Siempre ambos pasos.

### Fetch (raw/)
1. Obtener el contenido de la fuente (herramientas web/archivo). Si no hay acceso, pedir que la peguen.
2. Elegir el `<topic>`: reutilizar uno existente si encaja; crear solo si el tema es realmente distinto.
3. Guardar como `<dominio>/raw/<topic>/YYYY-MM-DD-slug.md` (slug kebab-case <= 60; si falta la fecha de publicación, omitir el prefijo y poner `Published: Unknown`; si el nombre existe, sufijo `-2`).
4. Cabecera de metadatos (Source/Collected/Published) + texto original fiel (limpiar ruido, no reescribir). Ver `raw-template.md`.

### Compile (wiki/) — objetivo: **10–15 páginas** tocadas por fuente
- **Step 0 — Takeaways (modo interactivo):** antes de escribir, mostrar 3–5 takeaways (claim central, entidades prominentes, páginas existentes afectadas). Saltar solo en ingest por lotes.
- **Step 1 — Summary (siempre):** `summary-<slug>.md` en el mismo topic que el raw.
- **Step 2 — Entity:** por cada cosa nombrada -> actualizar si existe (añadir la nueva summary a su tabla `Appearances`, refrescar `Updated`) o crear.
- **Step 3 — Concept:** por cada tema/idea -> fusionar en la página existente o crear una nueva nombrada por el concepto (no por la fuente).
- **Step 4 — Comparison y Synthesis:** crear/actualizar comparación cuando la fuente contrasta entidades; crear síntesis cuando la fuente + wiki soportan una conclusión de orden superior (usar campo `Wiki pages:`, no `Raw:`).
- **Anotación de conflicto:** si la fuente contradice contenido existente, anotarlo inline con atribución.

### Cascade Updates (solo dentro del mismo dominio)
Revisar el mismo topic, y entradas del `index.md` de otros topics con conceptos relacionados;
actualizar toda página materialmente afectada (refrescar `Updated`). Las páginas `archive` nunca se
cascadan. Efectos cross-dominio: mencionarlos al usuario, no aplicarlos solos.

### Post-Ingest
1. Actualizar `<dominio>/index.md` (añadir/actualizar filas de las páginas tocadas).
2. Actualizar `wiki/index.md` (solo las filas tocadas; añadir sección de dominio si es la primera).
3. Añadir al `<dominio>/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <primary page title>
   - Updated: <cascade-updated page title>
   ```
   (omitir las líneas `- Updated:` si no hubo cascade).

## 7. Operación QUERY

1. Resolver el dominio.
2. Leer `<dominio>/index.md` para localizar páginas relevantes.
3. Leer esas páginas y sintetizar una respuesta.
4. **Preferir el contenido de la Wiki** sobre el conocimiento del modelo. Citar con enlaces.
5. Responder en la conversación; **no escribir archivos** salvo que se pida.
6. Tras una respuesta sustancial, recomendar archivarla (sin auto-archivar).

**Formatos de salida:** prosa con citas (lookup/summary); tabla markdown (comparar); prosa Claim+Evidence (argumento); lista numerada (timeline); Marp (slides); tabla/código (datos).

**Archivado:** elegir plantilla por forma (comparison/synthesis/archive), escribir en el topic más
relevante, actualizar ambos índices y añadir al log:
```
## [YYYY-MM-DD] query | Archived: <page title>
```

## 8. Operación LINT

### Deterministas (auto-fix)
- **Consistencia del índice:** archivo sin entrada -> añadir con `(no summary)`; entrada sin archivo -> marcar `[MISSING]`; página bajo subheading equivocado -> mover; subheading vacío -> eliminar; sincronizar el índice global.
- **Enlaces internos:** destino inexistente -> buscar por nombre (1 match -> corregir; 0 o >1 -> reportar).
- **Referencias a raw:** cada enlace del campo `Raw:` debe apuntar a un archivo real de `raw/`.
- **See Also:** añadir cross-references obvias; quitar enlaces a archivos borrados.
- **Falta de `type:`** -> reportar (no asignar automáticamente).

### Heurísticas (solo reportar)
Contradicciones, afirmaciones obsoletas, huérfanas, cross-references faltantes, conceptos frecuentes
sin página, **vacíos de datos** (entidades muy referenciadas con poca cobertura -> candidatas a ingesta).

### Post-Lint
```
## [YYYY-MM-DD] lint | <N> issues found, <M> auto-fixed
```

## 9. Operación ACT (extensión de CEREBRO)

`ACT` **no** es una operación original de Karpathy: es nuestra capa operativa. Pasar del
conocimiento/estado a una **operación real** (actualizar una tarea, un estado, una compra). Se registra
en el log como `act`, con el mismo formato de prefijo.

## 10. Formato de `index.md`
Catálogo orientado a **contenido**. Agrupado por `topic` -> subheading de tipo
(`Concepts` / `Entities` / `Summaries` / `Comparisons & Syntheses` / `Archived`). Omitir subheadings sin
páginas. Ver `index-template.md`.

## 11. Formato de `log.md`
Cronológico, **append-only**. Cada entrada empieza con:
```
## [YYYY-MM-DD] <ingest|query|lint|act> | <título>
```
Parseable con `grep "^## \[" log.md | tail -5`. Nunca se edita el pasado.

## 12. Convenciones
- Markdown estándar con **enlaces relativos** dentro de la Wiki. Solo un nivel de `topic/`, sin anidar más.
- Fechas: `log`/`Collected`/`Archived` = hoy; `Updated` = cuándo cambió el contenido; `Published` = de la fuente (`Unknown` si no hay).
- Cada página (excepto `index.md`/`log.md`) lleva `type:`.
- INGEST actualiza el índice del dominio, el índice global y el log del dominio. ARCHIVE actualiza ambos índices y el log. LINT actualiza el log (e índices solo si auto-fix). **QUERY plano no escribe archivos.**
- Nombres de archivo: `summary-*`, `entity-*`, `concept-*`, `comparison-*`, `synthesis-*`, `archive-*`.

## 13. Convención bilingüe (CEREBRO)
Se conserva **verbatim** la estructura de Karpathy (frontmatter, headings de plantilla, subheadings del
índice, nombres de operaciones) **en inglés**, para que las plantillas y el LINT sean deterministas. La
**prosa** se escribe en **español**.

## 14. Rutas relativas (mapa CEREBRO)
Desde una página en `<dominio>/<topic>/`:
- a su raw -> `../raw/<topic>/<file>.md`
- a otra página del mismo topic -> `otra-pagina.md`
- a una página de otro topic -> `../<otro-topic>/otra-pagina.md`
