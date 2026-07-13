# CLAUDE.md — Reglas del proyecto

Instrucciones compartidas por todos los agentes y todo el equipo. Mantener este archivo corto y actualizado.

## Principios

- Este repo es agnóstico de stack. Antes de asumir un lenguaje o framework, detecta el stack real: revisa `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.csproj`, etc.
- Nunca inventes comandos de build/test: usa los definidos en el proyecto (scripts de `package.json`, `Makefile`, `justfile`) o pregunta.
- Todo cambio de código pasa por el ciclo: **plan → implementación → tests → review**. Usa los subagentes de `.claude/agents/` para cada fase.
- Cambios pequeños y atómicos. Un commit = una intención.

## Flujo de trabajo con agentes

1. Features o proyectos nuevos: delega el diseño al agente `planner`.
2. La implementación la hace `builder`, siguiendo el plan.
3. `tester` escribe/ejecuta tests y devuelve un reporte. Si falla, el reporte vuelve a `builder` para corregir (máximo 3 iteraciones antes de escalar al humano).
4. `reviewer` revisa el diff final antes de proponer commit/PR.

## Git y GitHub

- Nunca hacer push directo a `main`. Trabajar en ramas `feat/`, `fix/`, `chore/`.
- Commits en formato convencional: `feat: ...`, `fix: ...`, `test: ...`.
- Los PRs deben incluir: qué cambia, cómo se probó, y riesgos conocidos.

## Tests

- Ejecutar tests con `.claude/hooks/run-tests.sh` (detecta el runner del proyecto automáticamente).
- Ningún trabajo se considera terminado con tests en rojo.
- Todo bug corregido deja un test de regresión.

## Seguridad

- Nunca commitear secretos, tokens o credenciales. Usar variables de entorno y GitHub Secrets.
- No ejecutar comandos destructivos (rm -rf, git push --force) sin confirmación humana.
