#!/usr/bin/env bash
# Detector universal de test runner. Corre la suite del proyecto sin importar el stack.
set -u
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

run() { echo ">> $*"; "$@"; exit $?; }

# Prioridad: comandos definidos por el propio proyecto
if [ -f package.json ] && grep -q '"test"' package.json; then
  if [ -f pnpm-lock.yaml ]; then run pnpm test; fi
  if [ -f yarn.lock ]; then run yarn test; fi
  run npm test --silent
fi
if [ -f Makefile ] && grep -qE '^test:' Makefile; then run make test; fi
if [ -f justfile ] && grep -qE '^test' justfile; then run just test; fi

# Runners por lenguaje
if [ -f pyproject.toml ] || [ -f pytest.ini ] || [ -d tests ] && ls tests/*.py >/dev/null 2>&1; then
  command -v pytest >/dev/null && run pytest -q
fi
if [ -f go.mod ]; then run go test ./...; fi
if [ -f Cargo.toml ]; then run cargo test; fi
if [ -f pom.xml ]; then run mvn -q test; fi
if [ -f build.gradle ] || [ -f build.gradle.kts ]; then run ./gradlew test; fi
if ls *.csproj */*.csproj >/dev/null 2>&1; then run dotnet test; fi
if [ -f Gemfile ]; then run bundle exec rake test; fi
if [ -f composer.json ] && [ -f vendor/bin/phpunit ]; then run vendor/bin/phpunit; fi

echo "run-tests.sh: no se detectó ningún test runner. Configura 'test' en package.json/Makefile o ajusta este script."
exit 0
