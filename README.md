# CEREBRO

Sistema local de conocimiento y operaciones basado en **Markdown**, construido sobre el patrón
**LLM Wiki de Karpathy**.

- La memoria persistente es Markdown.
- **Obsidian** visualiza y edita la estructura (el vault es esta carpeta).
- **Donna** (IA vía Telegram, modelo gemma) y la IA de terminal (**Cline**) mantienen el sistema.
- **Python** ejecuta las automatizaciones.

## Fundamento — Karpathy LLM Wiki

- Gist original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Implementación de referencia: https://github.com/wpzero/karpathy-llm-wiki

Patrón: `información → Wiki → conocimiento persistente`.
El LLM construye y mantiene; el humano cura fuentes, dirige el análisis y pregunta.

Operaciones: **INGEST · QUERY · LINT** (+ **ACT**, nuestra extensión operativa).

## Estructura

```text
CEREBRO/
├── index.md                ← catálogo ÚNICO (conocimiento + operaciones)
├── log.md                  ← cronología ÚNICA (append-only)  ⭐
├── 01_WIKI/                ← conocimiento (qué sabemos)
│   ├── raw/                ← fuentes inmutables
│   └── conocimiento/ personas/ conceptos/ herramientas/ referencias/
├── 02_OPERACIONES/         ← operaciones (qué hacemos)
│   ├── proyectos/ decisiones/ reglas/ workflows/   (nota propia)
│   └── tareas.md  estados.md  compras.md           (archivos-lista)
├── _SISTEMA/               ← capa schema (contrato del sistema)
│   ├── README.md  SCHEMA.md  DONNA.md  REGLAS.md  ESTADO.md
│   └── plantillas/  (+ plantillas/operaciones/)
├── 00_INBOX/               ← entrada sin clasificar (capturas)
└── _AUTOMATIZACIONES/  03_PROYECTOS/ … 06_ARCHIVOS/   ← (fase 3)
```

## Empezar

1. Abrir esta carpeta como *vault* en Obsidian.
2. El contrato del sistema está en `_SISTEMA/SCHEMA.md` (y el corto para Donna en `_SISTEMA/DONNA.md`).
3. El catálogo es `index.md`; la cronología, `log.md`.