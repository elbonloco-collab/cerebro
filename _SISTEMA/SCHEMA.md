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

CEREBRO tiene dos capas: **`01_WIKI`** (qué sabemos) y **`02_OPERACIONES`** (qué hacemos con ello).

## 2. Las tres capas

| Capa | Dónde vive | Regla |
|------|-----------|-------|
| **Fuentes crudas** | `<dominio>/raw/<topic>/` | **Inmutable.** El LLM lee, nunca edita. Fuente de verdad. |
| **Wiki** | `<dominio>/<topic>/` | El LLM la posee por completo: crea, actualiza, cross-referencia. |
| **Schema** | `_SISTEMA/SCHEMA.md` (este archivo) | Define estructura, tipos y workflows. |

Plantillas exactas de cada tipo de página: `_SISTEMA/plantillas/` (Wiki) y `_SISTEMA/plantillas/operaciones/` (Operaciones).

> CEREBRO añade, sobre estas tres capas de conocimiento, una **capa operativa** (`02_OPERACIONES/`) — ver §15.

## 3. Dominios

CEREBRO se trata como **un único dominio**: hay **un solo** `index.md` y **un solo** `log.md`, y viven en la **raíz**.
Las carpetas (`01_WIKI/`, `02_OPERACIONES/`) son **regiones físicas**, no dominios con índice/log propio. (Si algún día hay áreas de conocimiento independientes, se podrán separar.)

**Resolución de dominio** (en este orden):
1. El usuario lo nombra explícitamente.
2. Inferido del contexto de la conversación.
3. Si es ambiguo: **preguntar**. Nunca elegir un dominio en silencio cuando hay varios.

## 4. Inicialización

Se dispara solo en el **primer INGEST** de un dominio. Crear únicamente lo que falte; **nunca sobrescribir**:
- `<dominio>/raw/` (+ `.gitkeep`)
- `index.md` (raíz) — catálogo único, si no existe
- `log.md` (raíz) — cronología única, si no existe

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
1. Actualizar `index.md` (raíz): añadir/actualizar filas de las páginas tocadas.
2. Añadir al `log.md` (raíz):
   ```
   ## [YYYY-MM-DD] ingest | <primary page title>
   - Updated: <cascade-updated page title>
   ```
   (omitir las líneas `- Updated:` si no hubo cascade).

## 7. Operación QUERY

1. Resolver el dominio.
2. Leer `index.md` (raíz) para localizar páginas relevantes.
3. Leer esas páginas y sintetizar una respuesta.
4. **Preferir el contenido de la Wiki** sobre el conocimiento del modelo. Citar con enlaces.
5. Responder en la conversación; **no escribir archivos** salvo que se pida.
6. Tras una respuesta sustancial, recomendar archivarla (sin auto-archivar).

**Formatos de salida:** prosa con citas (lookup/summary); tabla markdown (comparar); prosa Claim+Evidence (argumento); lista numerada (timeline); Marp (slides); tabla/código (datos).

**Archivado:** elegir plantilla por forma (comparison/synthesis/archive), escribir en el topic más
relevante, actualizar `index.md` y el log:
```
## [YYYY-MM-DD] query | Archived: <page title>
```

## 8. Operación LINT

### Deterministas (auto-fix)
- **Consistencia del índice:** archivo sin entrada -> añadir con `(no summary)`; entrada sin archivo -> marcar `[MISSING]`; página bajo subheading equivocado -> mover; subheading vacío -> eliminar.
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

## 10. Formato de `index.md` (raíz)
Catálogo **único** (conocimiento + operaciones). La sección Conocimiento se agrupa por `topic` -> subheading de tipo
(`Concepts` / `Entities` / `Summaries` / `Comparisons & Syntheses`); la sección Operaciones, por tipo. Omitir subheadings sin
páginas. Ver `index-template.md`.

## 11. Formato de `log.md` (raíz)
Cronológico, **append-only**. Cada entrada empieza con:
```
## [YYYY-MM-DD] <op> | <título>   (op = ingest · query · lint · act · project · task · decision · rule · workflow · state · event)
```
Parseable con `grep "^## \[" log.md | tail -5`. Nunca se edita el pasado.

## 12. Convenciones
- Markdown estándar con **enlaces relativos** dentro de la Wiki. Solo un nivel de `topic/`, sin anidar más.
- Fechas: `log`/`Collected`/`Archived` = hoy; `Updated` = cuándo cambió el contenido; `Published` = de la fuente (`Unknown` si no hay).
- Cada página (excepto `index.md`/`log.md`) lleva `type:`.
- INGEST actualiza `index.md` y `log.md`. ARCHIVE actualiza `index.md` y el log. LINT actualiza el log (e `index.md` solo si auto-fix). **QUERY plano no escribe archivos.**
- Nombres de archivo: `summary-*`, `entity-*`, `concept-*`, `comparison-*`, `synthesis-*`, `archive-*`.

## 13. Convención de idioma por capa
- **Capa Wiki (`01_WIKI`):** se conserva **verbatim** la estructura de Karpathy (frontmatter, headings de plantilla, subheadings del
índice, nombres de operaciones) **en inglés**, para que las plantillas y el LINT sean deterministas. La
**prosa** va en **español**.
- **Capa Operativa (`02_OPERACIONES`):** es capa propia de CEREBRO, así que headings y subheadings van en **español**; las **claves de frontmatter** y los **valores de `type`** se mantienen en **inglés**.

## 14. Rutas relativas (mapa CEREBRO)
Desde una página en `<dominio>/<topic>/`:
- a su raw -> `../raw/<topic>/<file>.md`
- a otra página del mismo topic -> `otra-pagina.md`
- a una página de otro topic -> `../<otro-topic>/otra-pagina.md`

---

## 15. Capa operativa — `02_OPERACIONES`

CEREBRO añade, sobre la capa de conocimiento, una **capa operativa**: qué hacemos con lo que sabemos.
- `01_WIKI` = qué sabemos.
- `02_OPERACIONES` = qué hacemos con ello.

```text
02_OPERACIONES/
├── proyectos/  decisiones/  reglas/  workflows/
├── tareas.md   estados.md   compras.md
```

El índice (`index.md`) y el log (`log.md`) son **únicos** y viven en la **raíz**. Plantillas: `_SISTEMA/plantillas/operaciones/`.

## 16. Tipos operativos

Cada página operativa (excepto `index.md` y `log.md`) lleva frontmatter `type:`:

| `type` | Carpeta | Qué es |
|--------|---------|--------|
| `project` | `proyectos/` | trabajo existente |
| `task` | casilla en la nota del proyecto (o `tareas.md`) | algo que hay que hacer |
| `decision` | `decisiones/` | decisión tomada |
| `rule` | `reglas/` | regla |
| `workflow` | `workflows/` | forma establecida de hacer algo |
| `state` | fila en `estados.md` | situación actual |
| `purchase` | casilla en `compras.md` | lista/registro de compra |

**Campos comunes:** `type`, `status`, `created`, `updated`.
**Campos por tipo:**
- `project`: `status` (activo/pausado/cerrado), `cliente`.
- `task`: `status` (pendiente/en progreso/hecha/bloqueada), `due`, `project`.
- `decision`: `status` (vigente/superada), `date`, `project`.
- `rule`: `status` (activa/inactiva).
- `workflow`: `status` (activo/inactivo).
- `state`: `variable`, `value`.
- `purchase`: `status` (abierta/comprada).

Los tipos **`event`**, **`context`** y **`action`** ya no son entidades propias (ver §19): el **evento** vive solo en `log.md`, la **acción es una tarea**, y el **contexto** se absorbe en el proyecto/estado al que aplica.

## 17. Operación ACT

`ACT` (extensión de CEREBRO, no de Karpathy) pasa del conocimiento/estado a una **operación real**.
1. Interpretar la instrucción.
2. Aplicar el cambio en `02_OPERACIONES/` (crear/actualizar la página del tipo).
3. Actualizar `index.md` (raíz).
4. Añadir al `log.md` (raíz) con `op` = el tipo (`task`, `state`, …) o `act`.

> Nota: por ahora `index.md`/`log.md` los actualiza **Cline a mano** en cada operación (como en Karpathy). Que el **escritor único sea Python** es una **meta futura**, no un hecho.

## 18. Índice y log (único, en la raíz)

- `index.md` (raíz) — catálogo único (conocimiento + operaciones). Se actualiza en cada operación.
- `log.md` (raíz) — cronología append-only. Formato:
  ```
  ## [YYYY-MM-DD] <tipo> | <título>
  ```
  Parseable: `grep "^## \[" log.md | tail -5`.

## 19. EVENT · CONTEXT · ACTION (sin entidad propia)

Decisión de CEREBRO:
- **EVENT** (evento): vive **solo** en `log.md` (su naturaleza es cronológica).
- **ACTION** (acción): **es una tarea** → misma regla que `task`; no es tipo aparte.

- **CONTEXT** (contexto): **no es entidad propia**; se absorbe en el proyecto o estado al que aplica.

> Nota: `PROJECT`, `DECISION`, `RULE` y `WORKFLOW` tienen **nota propia**; `TASK`, `STATE` y `PURCHASE` viven dentro de un archivo (`tareas.md` / nota de proyecto, `estados.md`, `compras.md`).
