---
title: Dónde debe detenerse la autonomía de un agente
description: Una forma práctica de definir límites según los efectos externos, los permisos y las decisiones humanas.
diagram_alt: Flujo de un agente desde la propuesta y preparación, pasando por autorización, hasta ejecución y reconciliación.
diagram_caption: La libertad para proponer no implica permiso para ejecutar una acción externa.
---

La pregunta «¿cuánta autonomía debería tener este agente?» es demasiado amplia para responderla con un único ajuste. Un agente puede explorar opciones con libertad y, al mismo tiempo, no tener permiso para publicar, gastar dinero o modificar datos de un cliente. El límite debe definirse para cada acción.

Mi punto de partida es separar tres tipos de trabajo:

1. **Observar y proponer.** Leer el contexto permitido, comparar opciones, redactar un plan o explicar un hallazgo.
2. **Preparar.** Crear un artefacto reversible y visible para quien lo revisa, como un borrador de publicación o un cambio propuesto.
3. **Ejecutar.** Producir un efecto externo: publicar contenido, cambiar accesos, desplegar, comprar o enviar un mensaje.

La tercera clase necesita el contrato más claro. La confianza que expresa un agente no equivale a una autorización.

## Definir el límite antes de escribir el prompt

Para cada herramienta o acción, me pregunto:

- ¿Quién está autorizado y a qué tenant o cuenta afecta la acción?
- ¿Puede revertirse? Si es así, ¿cómo y por quién?
- ¿Qué evidencia debe existir antes de ejecutarla?
- ¿Cuál es el gasto, volumen o ritmo máximo permitido?
- ¿Debe una persona aprobar esta acción concreta?
- ¿Cómo sabremos si el sistema externo realmente la aceptó?

Estas preguntas se convierten en reglas de la aplicación. El modelo puede seleccionar una acción, pero la aplicación comprueba las reglas en el punto de ejecución. Si falta información necesaria, la acción se detiene en un estado explícito en lugar de continuar con una suposición.

La documentación de agentes de AWS Bedrock describe la confirmación del usuario antes de determinadas funciones y la opción de devolver el control para que la propia aplicación ejecute la acción. Son ejemplos útiles del mismo principio: la aplicación conserva la autoridad sobre los efectos externos. Los controles concretos dependen de cada plataforma. Consulta la documentación de [confirmación](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html) y [devolución del control](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html).

## Convertir la aprobación humana en un estado del sistema

La supervisión humana aporta poco si la aprobación es solo una frase en un prompt o una etiqueta visual. La decisión debe persistir y el backend debe comprobarla cuando se intenta ejecutar la acción. Un rechazo o una condición de parada deben seguir vigentes tras un reintento, una sesión nueva o la intervención de otro agente.

El registro debe identificar la acción propuesta, el alcance revisado, la decisión, quién revisó y el resultado de la ejecución. Si el agente cambia la propuesta después de aprobarla, la aprobación deja de cubrirla.

## Tratar los resultados ambiguos como ambiguos

Una acción externa puede agotar el tiempo de espera después de que el proveedor la haya aceptado. Reintentar a ciegas una publicación o un pago puede duplicar el efecto. El flujo necesita una clave de idempotencia cuando exista soporte, una forma de reconciliar el estado real del proveedor y un resultado «desconocido» hasta terminar esa comprobación.

En GrowthMesh, mi proyecto personal, el diseño separa la planificación agéntica de marketing y la revisión de contenido de las comprobaciones deterministas sobre acceso por tenant, aprobación, presupuestos, publicación y medición. Esa separación importa más que el número de agentes del flujo.

La regla práctica es sencilla: **dar al agente libertad para razonar dentro de una tarea acotada y hacer que las acciones con consecuencias pasen por contratos exigibles y observables.** Así, la autonomía puede revisarse y ampliarse deliberadamente, acción por acción.
