# CEREBRO — MVP
## Sistema local de conocimiento y operaciones basado en Markdown

**Versión:** MVP 1.0  
**Fecha:** 2026-10-04  
**Estado:** Arquitectura base

## 1. Propósito

Cerebro es nuestro sistema/servidor local. Es el lugar donde se gestionan conocimiento, proyectos, clientes, decisiones, tareas, workflows, reglas, archivos y contexto.

La memoria persistente es principalmente **Markdown**.

**Obsidian** visualiza y permite trabajar sobre esa estructura.

**Donna** es nuestro asistente de IA y complementa a Cerebro.

**Telegram** es la interfaz inicial con Donna.

**Python** ejecuta las automatizaciones.

La arquitectura es:

```text
Usuario → Telegram → Donna → Cerebro/Markdown
                         ↓
                       Python
                         ↓
                      acciones
```

## 2. Objetivo del MVP

Construir una base pequeña, local y realmente funcional que permita:

- mantener una Wiki personal;
- gestionar proyectos;
- registrar decisiones;
- gestionar tareas y estados;
- documentar workflows y reglas;
- recibir instrucciones por Telegram;
- consultar y modificar Markdown mediante Donna;
- ejecutar automatizaciones con Python;
- visualizar todo desde Obsidian.

## 3. Fundamento: LLM Wiki de Karpathy

Fuente original:

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Cerebro adopta el concepto de una Wiki mantenida por LLM: conocimiento persistente, Markdown, relaciones, índice, log y operaciones de **INGEST / QUERY / LINT**.

La idea es:

```text
información → Wiki → conocimiento persistente
```

La IA ayuda a construir y mantener la Wiki, pero la memoria permanece en archivos.

Implementación comunitaria de referencia:

https://github.com/wpzero/karpathy-llm-wiki

## 4. Nuestra segunda capa

Karpathy aporta principalmente el modelo de conocimiento.

Cerebro añade una:

# PERSONAL OPERATIONS LAYER

Esta capa representa qué está pasando y qué debe hacerse.

Tipos básicos:

- **KNOWLEDGE:** algo que sabemos.
- **PROJECT:** trabajo existente.
- **TASK:** algo que hay que hacer.
- **STATE:** situación actual.
- **DECISION:** decisión tomada.
- **RULE:** regla.
- **WORKFLOW:** forma establecida de hacer algo.
- **EVENT:** algo que ocurrió.
- **CONTEXT:** situación relevante.
- **ACTION:** operación que debe ejecutarse.

Nuestra extensión conceptual es **ACT**:

```text
INGEST
QUERY
LINT
+
ACT
```

`ACT` no es una operación original de Karpathy; es nuestra capa operativa.

## 5. Estructura de carpetas MVP

```text
CEREBRO/
│
├── 00_INBOX/
│
├── 01_WIKI/
│   ├── index.md
│   ├── log.md
│   ├── conocimiento/
│   ├── personas/
│   ├── conceptos/
│   ├── herramientas/
│   └── referencias/
│
├── 02_OPERACIONES/
│   ├── tareas/
│   ├── decisiones/
│   ├── workflows/
│   ├── reglas/
│   ├── proyectos/
│   ├── compras/
│   └── estados/
│
├── 03_PROYECTOS/
│
├── 04_CLIENTES/
│
├── 05_RECURSOS/
│
├── 06_ARCHIVOS/
│
├── _SISTEMA/
│   ├── README.md
│   ├── SCHEMA.md
│   ├── REGLAS.md
│   ├── ESTADO.md
│   └── INDICE.md
│
└── _AUTOMATIZACIONES/
    ├── scripts/
    ├── telegram/
    └── tools/
```

Esta es una estructura inicial. No se crearán cientos de subcarpetas antes de comprobar su necesidad.

## 6. 00_INBOX

Entrada única para información todavía no clasificada:

```text
ENTRADA
↓
00_INBOX
↓
INTERPRETACIÓN
↓
CLASIFICACIÓN
↓
DESTINO
```

El usuario no debe tener que decidir siempre dónde guardar algo.

## 7. 01_WIKI

Es la memoria de conocimiento permanente.

Incluye conceptos, personas, herramientas, referencias y conocimiento general, RELACIONES entre personas y proyectos.

`index.md` permite localizar páginas relevantes.

`log.md` registra operaciones como:

```text
INGEST
QUERY
LINT
CREATE
UPDATE
LINK
```

## 8. 02_OPERACIONES

Es nuestra segunda capa.

```text
02_OPERACIONES/
├── tareas/
├── decisiones/
├── workflows/
├── reglas/
├── proyectos/
├── compras/
└── estados/
```

Conceptualmente:

```text
01_WIKI = qué sabemos
02_OPERACIONES = qué hacemos con ello
```

## 9. Markdown como memoria

Los Markdown son las unidades persistentes de información.

Modelo mental:

```text
MD = neurona
link = conexión
carpeta = región
Wiki = red
Cerebro = sistema
```

No es una afirmación biológica literal; es una forma de entender la arquitectura.

Las carpetas organizan físicamente.

Los enlaces Markdown organizan conceptualmente.

## 10. Obsidian

Obsidian es nuestra herramienta visual.

No es la memoria independiente del sistema.

```text
CEREBRO
↓
Markdown
↓
Obsidian
```

Obsidian sirve para:

- visualizar;
- navegar;
- editar;
- relacionar;
- usar el grafo.

## 11. Donna

Nuestro asistente se llama:

# DONNA

El nombre hace referencia a **Donna Paulsen de Suits**.

Donna no es el lugar donde vive la memoria.

```text
Donna
↓
consulta/actualiza
↓
Cerebro
```

Donna es la interfaz inteligente que complementa el sistema.

## 12. Telegram

Telegram permanece como interfaz principal del MVP.

Ya existe el bot.

Flujo:

```text
Usuario
↓
Telegram
↓
Donna
↓
Cerebro
↓
Markdown / Python
```

Puede recibir texto y, posteriormente, voz.

## 13. IA local

Donna utilizará gemma4:e2b-it-qat para las tareas realizadas mediante Telegram.

Debemos asumir que es un modelo pequeño y limitado.

Por eso el MVP debe usar:

- contexto reducido;
- prompts pequeños;
- herramientas concretas;
- respuestas estructuradas;
- búsqueda selectiva;
- poco texto innecesario.

No se debe enviar toda la Wiki al modelo.

## 14. IA fuerte de terminal

Las tareas pesadas de construcción y mantenimiento de Wiki se delegarán a la IA disponible en terminal que identificamos como Cline a traves de vs Code modelo deepseak v4
Su función será ayudar a:

- crear estructura;
- construir Markdown;
- reorganizar;
- mantener la Wiki;
- crear Schema;
- ejecutar trabajos complejos.

Tiene límites de uso, por lo que la arquitectura debe economizar tokens.

La división inicial es:

```text
Donna / Gemma
→ interacción diaria y tareas sencillas

IA de terminal
→ construcción y mantenimiento pesado
```

## 15. Python

Las automatizaciones serán scripts Python propios.

Principio:

```text
IA = interpreta / decide
Python = ejecuta
```

Python podrá:

- crear archivos;
- mover archivos;
- actualizar Markdown;
- procesar Inbox;
- crear proyectos;
- ejecutar tareas;
- interactuar con Telegram;
- validar estructura;
- ejecutar herramientas.

Ejemplo:

```text
Donna
↓
"crea un proyecto de música"
↓
Python
↓
crea carpetas + MD + enlaces
↓
Telegram
↓
confirmación
```


## 18. Captura natural

El usuario debe poder hablar normalmente.

Ejemplo:

> “Se acabó el café.”

Donna puede interpretar:

```text
tipo = STATE
objeto = café
estado = agotado
```

Otro:

> “Tengo que terminar el template mañana.”

```text
tipo = TASK
acción = terminar template
fecha = mañana
```

Otro:

> “Todos los proyectos nuevos de música deben usar este workflow.”

```text
tipo = RULE / DECISION
```

No todo lo dicho debe convertirse en un archivo nuevo. Puede actualizar un MD existente, crear uno, modificar un estado, crear una tarea o simplemente responder.

## 19. Regla contra preguntas innecesarias

Donna debe inferir cuando sea razonablemente seguro.

Debe preguntar solamente cuando la información faltante cambie materialmente la acción.

No:

> “¿Quieres que cree una nota?”

ante cada frase.

Sí preguntar cuando exista una ambigüedad que pueda provocar una acción incorrecta.

IMPORTANTE: La ia debe de aprender de los procesos y guadar los cambios de procesos en log.

## 20. INGEST

Para conocimiento externo:

```text
FUENTE
↓
INGEST
↓
ANÁLISIS
↓
MD
↓
INDEX
↓
LINKS
↓
LOG
```

## 21. QUERY

Cuando Donna necesita información:

```text
PREGUNTA
↓
buscar Wiki
↓
encontrar MD relevante
↓
leer contexto
↓
responder
```

No se debe cargar toda la Wiki en cada consulta.

## 22. LINT

El mantenimiento debe poder detectar:

- enlaces rotos;
- Markdown incorrecto;
- páginas huérfanas;
- duplicados;
- inconsistencias;
- información obsoleta;
- problemas del índice;
- reglas contradictorias.

Python y/o la IA de terminal pueden realizar estas revisiones.

## 23. ACT

Nuestra extensión operativa:

```text
INGEST
QUERY
LINT
ACT
```

Ejemplo:

```text
“Se acabó el café.”
↓
interpretar
↓
actualizar estado
↓
revisar reglas
↓
actualizar compras
```

ACT significa pasar del conocimiento/estado a una operación real.

## 24. Ubicación

La ubicación queda contemplada, pero **no es requisito del primer núcleo del MVP**.

La futura arquitectura debe utilizar eventos semánticos, no transmisión constante de coordenadas.

Ejemplos:

```text
HOME_ENTER
HOME_EXIT
WALMART_ENTER
BRAVO_ENTER
STUDIO_ENTER
STUDIO_EXIT
```

Después:

```text
ubicación
↓
evento
↓
contexto
↓
regla
↓
acción
```

Ejemplo:

```text
WALMART_ENTER
↓
contexto = compras
↓
compras pendientes
↓
Donna
↓
“Recuerda comprar café.”
```

## 25. Lo que queda fuera

Este MVP NO incluye como componentes necesarios:

- PostgreSQL;
- n8n;
- multiagentes complejos;
- escucha permanente;
- aplicación móvil propia;
- geofencing completo;
- cloud complejo;
- vector database;
- embeddings como requisito;
- RAG sofisticado;
- múltiples modelos innecesarios.

Podrán evaluarse después, pero no deben contaminar el núcleo inicial.

## 26. Criterio de arquitectura

Cada componente nuevo debe responder:

1. ¿Es necesario?
2. ¿Puede resolverse con Markdown?
3. ¿Puede resolverse con Python?
4. ¿Puede hacerlo Donna con una herramienta?
5. ¿Consume recursos o tokens innecesarios?
6. ¿Simplifica o complica Cerebro?

Si no aporta una mejora clara, no entra al MVP.

## 27. Criterio de éxito

El MVP debe poder demostrar estos flujos:

### Crear

> “Donna, crea un proyecto para una nueva producción de Eva.”

Resultado:

```text
Python
→ estructura
→ Markdown
→ enlaces
→ proyecto visible en Obsidian
```

### Registrar decisión

> “Decidí que todos los proyectos nuevos de música usarán este workflow.”

Resultado:

```text
Donna
→ interpreta
→ registra decisión/regla
→ relaciona workflow
```

### Consultar

> “Donna, ¿qué decisiones tenemos sobre Producer Pal?”

Resultado:

```text
QUERY
→ Wiki
→ decisiones relacionadas
→ respuesta
```

Si estos flujos funcionan, tenemos el núcleo real de Cerebro.

## 28. Orden de construcción

### Paso 1
Crear estructura física.

### Paso 2
Crear `SCHEMA.md`.

### Paso 3
Crear `REGLAS.md`.

### Paso 4
Crear Markdown reales de prueba.

### Paso 5
Configurar Obsidian.

### Paso 6
Conectar Telegram.

### Paso 7
Conectar Donna/Gemma.

### Paso 8
Crear herramientas Python mínimas.

### Paso 9
Probar captura → clasificación → Markdown.

### Paso 10
Probar QUERY.

### Paso 11
Probar ACT.

### Paso 12
Probar proyectos, tareas, decisiones y workflows.

Después se evalúan nuevas capacidades.

## 29. Definición final del MVP

> **Cerebro es un sistema local file-first que utiliza Markdown como memoria persistente, Obsidian como interfaz visual, Donna como asistente de IA vía Telegram y Python como capa de ejecución.**

Sobre el modelo LLM Wiki de Karpathy añadimos una segunda capa:

> **Personal Operations Layer**

que permite representar conocimiento, proyectos, tareas, estados, decisiones, reglas, workflows, eventos, contexto y acciones.

La arquitectura debe permanecer:

- local;
- simple;
- legible;
- modular;
- económica en tokens;
- económica en recursos;
- independiente de un proveedor concreto.

Todo lo demás es segunda fase.
