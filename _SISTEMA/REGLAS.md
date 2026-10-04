# REGLAS.md — Reglas de CEREBRO

1. **Memoria = Markdown.** Todo el conocimiento vive en archivos Markdown versionados en Git.
2. **`raw/` es inmutable.** El LLM lee las fuentes crudas, nunca las modifica.
3. **El LLM escribe la Wiki; el humano la lee y pregunta.**
4. **Cada página lleva `type:`** en el frontmatter (`summary` | `entity` | `concept` | `comparison` | `synthesis` | `archive`). Excepciones: `index.md` y `log.md`.
5. **`index.md` y `log.md` se mantienen siempre.** Todo INGEST/ARCHIVE/LINT-fix los actualiza.
6. **`log.md` es append-only.** Nunca se edita una entrada pasada. Prefijo obligatorio: `## [YYYY-MM-DD] <op> | <título>`.
7. **Enlaces relativos** dentro de la Wiki; un solo nivel de `topic/`.
8. **Economía de tokens.** No cargar toda la Wiki: usar los índices para localizar páginas. Donna (modelo pequeño) trabaja con contexto reducido, prompts pequeños y respuestas estructuradas.
9. **Inferir cuando sea razonablemente seguro; preguntar solo cuando la ambigüedad cambie materialmente la acción.**
10. **Anotar contradicciones** inline con atribución a la fuente; no borrar silenciosamente.
11. **Efectos cross-dominio:** se reportan al usuario, no se aplican automáticamente.
12. **Python ejecuta, la IA interpreta.** Las automatizaciones son scripts Python propios.
13. **Aprender de los procesos.** La IA guarda cambios de proceso en el log.
14. Si un componente nuevo no aporta una mejora clara, **no entra** al sistema.
