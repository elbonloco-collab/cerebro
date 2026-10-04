# Index Template
# ————————————————————————————————————————————————————————————————
# Índice de DOMINIO  →  úsalo en  `<dominio>/index.md`   (en CEREBRO: `01_WIKI/index.md`)

# {Domain} — Base de Conocimiento

## {topic-name}

{One-line description of this topic.}

### Concepts
| Page | Summary | Updated |
|------|---------|---------|
| [{Page Title}]({topic-name}/{page}.md) | {One-line summary} | {YYYY-MM-DD} |

### Entities
| Page | Summary | Updated |
|------|---------|---------|
| [{Entity Name}]({topic-name}/{entity}.md) | {One-line summary} | {YYYY-MM-DD} |

### Summaries
| Page | Summary | Updated |
|------|---------|---------|
| [Summary: {Source}]({topic-name}/{summary}.md) | {One-line summary} | {YYYY-MM-DD} |

### Comparisons & Syntheses
| Page | Summary | Updated |
|------|---------|---------|
| [{Comparison or Synthesis Title}]({topic-name}/{page}.md) | {One-line summary} | {YYYY-MM-DD} |

### Archived
| Page | Summary | Updated |
|------|---------|---------|
| [{Archived Title}]({topic-name}/{archived}.md) | [Archived] {One-line summary} | {YYYY-MM-DD} |

{Omit any subheading whose type has no pages in this topic.}

# ————————————————————————————————————————————————————————————————
# Índice GLOBAL (cross-dominio)  →  úsalo en  `<vault>/index.md`  (en CEREBRO: `wiki/index.md`)

# Knowledge Base Index

## {domain-name}

{One-line description of this domain.}

### Concepts
| Page | Summary | Updated |
|------|---------|---------|
| [{Page Title}](../{domain-name}/{topic}/{page}.md) | {One-line summary} | {YYYY-MM-DD} |

### Entities
| Page | Summary | Updated |
|------|---------|---------|
| [{Entity Name}](../{domain-name}/{topic}/{entity}.md) | {One-line summary} | {YYYY-MM-DD} |

### Summaries
| Page | Summary | Updated |
|------|---------|---------|
| [Summary: {Source}](../{domain-name}/{topic}/{summary}.md) | {One-line summary} | {YYYY-MM-DD} |

### Comparisons & Syntheses
| Page | Summary | Updated |
|------|---------|---------|
| [{Comparison or Synthesis Title}](../{domain-name}/{topic}/{page}.md) | {One-line summary} | {YYYY-MM-DD} |

### Archived
| Page | Summary | Updated |
|------|---------|---------|
| [{Archived Title}](../{domain-name}/{topic}/{archived}.md) | [Archived] {One-line summary} | {YYYY-MM-DD} |

{Omit any subheading whose type has no pages in this domain.}
# Nota CEREBRO: la wiki del dominio vive directamente bajo `<dominio>/<topic>/`
# (no hay subcarpeta `wiki/` extra), por eso la ruta global es `../{dominio}/{topic}/{page}.md`.
