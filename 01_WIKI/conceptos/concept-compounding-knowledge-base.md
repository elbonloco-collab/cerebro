---
type: concept
---
# Base de Conocimiento Compuesta

> Sources: Andrej Karpathy (gist), 2026-04-04
> Raw: [2026-04-04-llm-wiki-karpathy-gist.md](../raw/llm-wiki/2026-04-04-llm-wiki-karpathy-gist.md)
> Updated: 2026-10-04

## Overview

Una **base de conocimiento compuesta** es aquella cuyo valor crece con cada fuente añadida porque el
conocimiento se **compila una vez y se mantiene vigente**, en lugar de re-derivarse en cada consulta.
Es la propiedad central que distingue al [Patrón LLM Wiki](concept-llm-wiki-pattern.md) de RAG.

## Por qué compone

En RAG el LLM re-descubre el conocimiento desde cero en cada pregunta: no hay acumulación. Una
pregunta que exige sintetizar cinco documentos obliga a localizar y ensamblar los fragmentos cada vez.

En el patrón LLM Wiki, cuando llega una fuente nueva el modelo no se limita a indexarla: la lee,
extrae lo clave y la **integra en la wiki existente** —actualiza páginas de entidad, revisa resúmenes
de tema, anota dónde los datos nuevos contradicen afirmaciones previas y refuerza o desafía la
síntesis—. Los cross-references ya están; las contradicciones ya están marcadas; la síntesis ya
refleja todo lo leído.

> "The wiki is a persistent, compounding artifact." — Karpathy

## El cuello de botella que se elimina

La parte tediosa de mantener una base de conocimiento no es leer ni pensar: es el **bookkeeping**
(actualizar cross-references, mantener resúmenes al día, notar contradicciones, sostener consistencia
en decenas de páginas). Los humanos abandonan las wikis porque el coste de mantenimiento crece más
rápido que el valor. Los LLM no se aburren, no olvidan una cross-reference y pueden tocar 15 archivos
en una pasada: el coste de mantenimiento se vuelve **casi cero**.

## Conexión histórica

En espíritu se relaciona con el **Memex** de Vannevar Bush (1945): un almacén de conocimiento
personal y curado, con "senderos asociativos" entre documentos. Lo que Bush no pudo resolver —quién
hace el mantenimiento— lo asume aquí el LLM.

## See Also

- [Patrón LLM Wiki](concept-llm-wiki-pattern.md)
- [LLM Wiki supera a RAG para conocimiento de largo plazo](synthesis-llm-wiki-beats-rag.md)
