---
name: new-project
description: Crea un proyecto nuevo desde cero con el ciclo completo plan → build → test → review. Usar cuando el usuario pida iniciar, crear o bootstrapear un proyecto o prototipo nuevo.
---

# Crear proyecto nuevo

Orquesta el ciclo completo para levantar un proyecto desde cero.

## Pasos

1. Si el usuario no especificó lenguaje/stack, pregunta (una sola vez) cuál prefiere, ofreciendo una opción por defecto razonable según el tipo de proyecto.
2. Delega al subagente **planner**: estructura del proyecto, tooling mínimo (formatter, linter, test runner del stack), y primeros módulos.
3. Delega al subagente **builder** la implementación del plan. Debe incluir:
   - README.md con instrucciones de instalación y ejecución
   - Configuración de tests funcionando (aunque haya un solo test)
   - .gitignore adecuado al stack
4. Delega al subagente **tester**: ejecutar la suite y reportar.
5. Si el reporte tiene fallos → devolver al builder (máximo 3 ciclos).
6. Delega al subagente **reviewer** para la revisión final.
7. Inicializa git si no existe (`git init`, primer commit en rama main, luego crear rama de trabajo).

## Criterio de éxito

El proyecto compila/corre, los tests pasan, y otro miembro del equipo podría clonarlo y ejecutarlo siguiendo solo el README.
