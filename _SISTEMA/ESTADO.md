# ESTADO.md — Estado de CEREBRO

**Versión:** MVP 1.0 (capa Karpathy)
**Última actualización:** 2026-10-04

## Hecho (Fase 1 — fundación Karpathy)

- [x] Repositorio Git inicializado (`main`).
- [x] Estructura física de carpetas creada.
- [x] Capa **raw**: `01_WIKI/raw/llm-wiki/2026-04-04-llm-wiki-karpathy-gist.md`.
- [x] Índice (único): `01_WIKI/index.md`.
- [x] **Log** de dominio: `01_WIKI/log.md` (append-only) ⭐.
- [x] Capa **schema**: `_SISTEMA/SCHEMA.md`, `REGLAS.md`, `ESTADO.md`, `README.md`.
- [x] **Plantillas**: `_SISTEMA/plantillas/` (raw, summary, entity, concept, comparison, synthesis, archive, index).
- [x] `AGENTS.md` en la raíz.
- [x] Primer **INGEST**: gist de Karpathy → summary + entity + 2x concept + 1x synthesis.

## Pendiente (Fase 2 — capa operativa de CEREBRO)

- [ ] Poblar `02_OPERACIONES/` (tareas, decisiones, workflows, reglas, proyectos, compras, estados).
- [ ] Definir `03_PROYECTOS/`, `04_CLIENTES/`, `05_RECURSOS/`, `06_ARCHIVOS/`.
- [ ] Configurar Obsidian (vault = esta carpeta).
- [ ] Conectar Telegram ↔ Donna.
- [ ] Conectar Donna/Gemma.
- [ ] Herramientas Python mínimas en `_AUTOMATIZACIONES/` (crear/validar/buscar).
- [ ] Probar captura → clasificación → Markdown; QUERY; ACT.

## Notas

- Dentro del MVP documento (`CEREBRO_MVP_MARKDOWN_OPERATIVO.md`) el ítem "log" ya existía como
  `01_WIKI/log.md`; aquí queda implementado como archivo **append-only del dominio** según el patrón
  de Karpathy, y elevado a elemento de primera importancia.
- `_REF_TMP/` es temporal (referencias usadas para construir CEREBRO); está en `.gitignore` y puede borrarse.
