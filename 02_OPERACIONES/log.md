# 02_OPERACIONES — Operations Log

> Log **append-only** (nunca se edita el pasado; solo se añade al final).
> Cada entrada empieza con `## [YYYY-MM-DD] <tipo> | <título>`.
> `<tipo>` = `project` | `task` | `decision` | `rule` | `workflow` | `state` | `purchase` | `act` | `event` | `context` | `action`.
> Parseable: `grep "^## \[" log.md | tail -5`.

## [2026-10-04] project | Producción de Eva
- Creado `proyectos/project-eva-produccion.md`; usa `workflows/workflow-produccion-musica.md`.

## [2026-10-04] decision | Workflow de música para proyectos nuevos
- Creada la decisión; enlaza el workflow de producción de música.

## [2026-10-04] rule | Usar el workflow de música en proyectos nuevos
- Creada la regla derivada de la decisión.

## [2026-10-04] task | Terminar el template
- Creada la tarea; pertenece al proyecto de Eva. Vence 2026-10-05.

## [2026-10-04] state | Café → agotado
- Estado `cafe` = `agotado` (antes `disponible`).

## [2026-10-04] event | Se acabó el café
- EVENT registrado (sin carpeta). Ver `index.md` → *Registro rápido*.

## [2026-10-04] context | Compras (café agotado)
- CONTEXT registrado: contexto de compras activo.

## [2026-10-04] action | Reponer café
- ACTION registrada: añadir café a la lista de compras.

## [2026-10-04] purchase | Lista de compras — añadir café
- Actualizada `compras/purchase-lista.md`.
