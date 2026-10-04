# CEREBRO

Sistema local de conocimiento y operaciones basado en **Markdown**, construido sobre el patrón
**LLM Wiki de Karpathy**.

- La memoria persistente es Markdown.
- **Obsidian** visualiza y edita la estructura (el vault es esta carpeta).
- **Donna** (IA vía Telegram, modelo gemma) y la IA de terminal (**Cline**) mantienen la wiki.
- **Python** ejecuta las automatizaciones.

## Fundamento — Karpathy LLM Wiki

- Gist original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Implementación de referencia: https://github.com/wpzero/karpathy-llm-wiki

Patrón: `información → Wiki → conocimiento persistente`.
El LLM construye y mantiene la Wiki; el humano cura fuentes, dirige el análisis y pregunta.

Operaciones: **INGEST · QUERY · LINT** (+ **ACT**, nuestra extensión operativa).

## Estructura

```text
CEREBRO/
├── 01_WIKI/                ← DOMINIO de conocimiento
│   ├── raw/                ← fuentes inmutables (capa 1)
│   ├── index.md            ← índice del dominio
│   ├── log.md              ← log append-only  ⭐
│   ├── conocimiento/       ← summaries
│   ├── personas/           ← entities (personas)
│   ├── conceptos/          ← concepts + syntheses
│   ├── herramientas/       ← entities (tools)
│   └── referencias/
├── _SISTEMA/               ← capa SCHEMA (contrato del sistema)
│   ├── README.md  SCHEMA.md  REGLAS.md  ESTADO.md
│   └── plantillas/         ← plantillas exactas de cada tipo de página
├── _AUTOMATIZACIONES/      ← scripts / telegram / tools  (fase 2)
├── 00_INBOX/               ← entrada sin clasificar
├── 02_OPERACIONES/           ← capa operativa: index.md · log.md · proyectos/ tareas/ decisiones/ reglas/ workflows/ estados/ compras/
└── 03_PROYECTOS/ … 06_ARCHIVOS/  ← (fase 2)
```

## Empezar

1. Abrir esta carpeta como *vault* en Obsidian.
2. El contrato del sistema está en `_SISTEMA/SCHEMA.md`.
3. El índice es `01_WIKI/index.md`; el log, `01_WIKI/log.md`.
4. La capa operativa (qué hacemos) vive en `02_OPERACIONES/`.
