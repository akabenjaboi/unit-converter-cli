# CLAUDE.md — Reglas del proyecto

Instrucciones compartidas por todos los agentes y todo el equipo. Mantener este archivo corto y actualizado.

## Principios

- Este repo es agnóstico de stack. Antes de asumir un lenguaje o framework, detecta el stack real: revisa `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.csproj`, etc.
- Nunca inventes comandos de build/test: usa los definidos en el proyecto (scripts de `package.json`, `Makefile`, `justfile`) o pregunta.
- Cambios pequeños y atómicos. Un commit = una intención.

## Metodología de desarrollo

- Este proyecto usa **Superpowers** como metodología de desarrollo (brainstorm → diseño aprobado → plan → TDD → review). Instálalo con `/plugin install superpowers@claude-plugins-official` (ver README).
- Sigue los flujos de Superpowers cuando estén disponibles; estas reglas de proyecto los complementan, no los reemplazan.

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
