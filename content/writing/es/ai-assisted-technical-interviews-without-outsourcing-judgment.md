---
title: Entrevistas técnicas asistidas por IA sin delegar el criterio
description: Cómo revisar pruebas de Platform Engineering con ayuda de IA para encontrar evidencias y preparar mejores preguntas sin delegar la decisión de contratación.
illustration_alt: Comparación conceptual entre una puntuación de IA que determina una contratación y una revisión basada en evidencias que informa una entrevista humana.
illustration_caption: "Una representación conceptual del límite: la IA puede organizar evidencias y sugerir preguntas; la decisión de contratación corresponde a las personas."
---

Hace poco, durante un proceso de selección para incorporar Platform Engineers, construimos una revisión de pruebas técnicas asistida por IA. El objetivo era sencillo: reducir el trabajo manual de preparación sin convertir la IA en quien tomara la decisión de contratación.

La prueba tenía dos partes: el diseño de una solución técnica y ADRs que justificaban las decisiones tomadas. Un conjunto de agentes y *skills* analizaba la entrega según varios criterios y preparaba preguntas para la entrevista.

## De la entrega a señales útiles

La revisión podía señalar decisiones poco justificadas, *trade-offs* sin explorar y riesgos de fiabilidad, seguridad, coste u operabilidad. También podía detectar inconsistencias entre la arquitectura propuesta y sus ADRs.

El flujo buscado era:

**Entrega → evidencias → observaciones → puntos a explorar → preguntas para la entrevista.**

El resultado servía para iniciar una conversación técnica. No era un veredicto sobre si el candidato era «bueno» o «malo».

## Una puntuación es una inferencia, no una decisión

Este trabajo reforzó una preocupación que tengo sobre los sesgos de los LLM. Un modelo no evalúa un diseño desde una posición neutral. Los patrones que ha aprendido pueden favorecer tecnologías habituales, arquitecturas convencionales y determinadas formas de explicar una decisión. Eliminar atributos personales explícitos no elimina la posibilidad de sesgos indirectos.

Un candidato puede razonar bien y expresarlo de una forma que el modelo no espera. Una arquitectura poco habitual puede ser válida. Un *trade-off* bien justificado puede diferir de la solución que más aparece en los datos de entrenamiento.

Por eso, la pregunta importante no es solo si un LLM *puede* puntuar una prueba. Es **qué autoridad damos a esa puntuación**. Un porcentaje puede comprimir incertidumbre y desacuerdo en una cifra que parece más objetiva de lo que es.

## Tres límites para una evaluación asistida por IA

1. **Criterios antes que modelo.** Define qué quieres evaluar antes de pedirle al modelo que revise la entrega. Los criterios deben ser visibles y cuestionables.
2. **Evidencia antes que puntuación.** Una observación debe señalar una parte concreta de la entrega y explicar por qué importa. Una calificación sin fundamento ayuda poco en la entrevista.
3. **Preguntas antes que conclusiones.** Una inferencia del modelo debe convertirse en una pregunta que el entrevistador pueda contrastar con el candidato, también para entender por qué eligió una opción poco habitual.

Estos límites no hacen desaparecer el sesgo. Permiten examinar los juicios inciertos del modelo y evitan que se conviertan silenciosamente en decisiones.

## La autoridad permanece en el entrevistador

El resultado útil fue dedicar menos tiempo a preparar entrevistas y más tiempo a conversaciones técnicas profundas. La IA ayudó a convertir una entrega compleja en evidencias y preguntas concretas. El entrevistador seguía teniendo que escuchar, cuestionar el análisis, entender el contexto y tomar la decisión final.

El sesgo se vuelve especialmente peligroso cuando una inferencia se transforma automáticamente en una acción. En selección de personal, el sistema debe ayudar a las personas a ejercer mejor su criterio, no delegarlo en un modelo.
