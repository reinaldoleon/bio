---
title: ¿Cómo saber si un flujo de IA funciona de verdad?
description: Cómo revisar fuentes, herramientas, validaciones y resultados finales en lugar de juzgar un sistema de IA solo por la respuesta del modelo.
diagram_alt: Evaluación desde entradas y fuentes, pasando por la traza del agente y controles de calidad, hasta el resultado publicado.
diagram_caption: Hay que evaluar el camino completo hasta el resultado observable, incluidos los rechazos y las revisiones.
---

Un modelo puede responder bien a una prueba mientras falla el producto que lo rodea. La fuente puede estar desactualizada. Una herramienta puede devolver datos de otro tenant. Una revisión puede omitirse. La publicación puede agotar el tiempo de espera después de crear un artefacto que nadie logra encontrar.

Por eso evalúo los flujos de IA como sistemas, desde la entrada hasta el resultado observable.

## Empezar por la decisión que debe respaldar el sistema

Una evaluación es útil cuando responde una pregunta de producto o ingeniería. «¿Es buena la respuesta?» es demasiado vago. Estas preguntas son más concretas:

- ¿Seleccionó el sistema fuentes pertinentes y permitidas?
- ¿Está respaldada por la evidencia adjunta cada afirmación importante?
- ¿Usó el agente la herramienta adecuada y respetó sus límites de autorización?
- ¿Rechazó un control de calidad una salida incompleta o sin sustento?
- ¿Coincide el artefacto publicado con la versión aprobada?
- Cuando la evidencia era insuficiente, ¿lo indicó el sistema y se detuvo?

Las respuestas requieren comprobaciones diferentes. Algunas son deterministas: validez del esquema, aislamiento entre tenants, referencias obligatorias, estado de aprobación o checksum del artefacto. Otras necesitan criterios de evaluación y revisión humana: si una narrativa es justa, útil o engañosa. Una puntuación agregada oculta esas diferencias.

## Evaluar el recorrido, no solo el texto final

Hay que conservar suficiente información de cada ejecución para reconstruir la secuencia: selección de fuentes, llamadas al modelo, herramientas, traspasos, controles, decisiones humanas y efectos externos. Una respuesta final puede parecer correcta por la razón equivocada; la traza ayuda a localizar el fallo.

Las guías de evaluación de agentes de OpenAI describen trazas, evaluadores, conjuntos de casos y ejecuciones de evaluación como recursos complementarios para analizar flujos. La lección general es inspeccionar primero fallos individuales y convertirlos después en casos repetibles. Consulta la [guía de evaluación de agentes](https://developers.openai.com/api/docs/guides/agent-evals) y la [guía de evaluación de trazas](https://developers.openai.com/api/docs/guides/trace-grading).

## Construir un conjunto pequeño de casos que distinga fallos

Empezaría con casos que representen decisiones reales:

- Un caso sencillo que el sistema debería completar.
- Dos fuentes aparentemente independientes que repiten el mismo informe original.
- Una fuente pertinente que no respalda exactamente la afirmación propuesta.
- Una respuesta válida cuya publicación debe detenerse porque falta aprobación.
- Un fallo del proveedor o una respuesta truncada.
- Una entrada modificada que no debe reescribir en silencio un artefacto ya publicado.

Para cada caso registraría el resultado esperado y el motivo. La evaluación debe distinguir un **rechazo correcto** de un **fallo al producir una salida**. De otro modo, un equipo podría mejorar su tasa de éxito debilitando el control.

## Mantener visible el estado de la evidencia

En CAUSIO, mi proyecto personal de inteligencia de mercado, el diseño separa hecho, inferencia, hipótesis y desconocido. La corroboración por afirmación y las reglas de publicación rodean el análisis del LLM. Esa estructura permite preguntar de dónde salió una conclusión y por qué se aceptó o rechazó un evento.

Para sistemas como este, mostraría señales separadas de suficiencia de evidencia, falsos positivos, eventos pertinentes omitidos, calidad de fuentes, continuidad temporal e integridad de publicación. La prioridad entre precisión y cobertura depende del coste de cada error. En inteligencia de mercado, una afirmación causal convincente pero sin sustento puede hacer más daño que una omisión prudente.

El objetivo no es obtener una cifra perfecta. Es disponer de un contrato repetible: **qué debe hacer el sistema, qué evidencia demuestra que lo hizo y qué bloquea la publicación cuando no lo consigue.**
