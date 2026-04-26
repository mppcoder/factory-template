#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
if [ -f "$ROOT" ]; then
  ROOT="$(dirname "$ROOT")"
fi
REQ=("$ROOT/README.md" "$ROOT/VERSION.md" "$ROOT/CHANGELOG.md" "$ROOT/CURRENT_FUNCTIONAL_STATE.md")
for f in "${REQ[@]}"; do
  [ -f "$f" ] || { echo "ОШИБКА: отсутствует $f"; exit 1; }
done
ORIGIN="$ROOT/.chatgpt/project-origin.md"
if [ -f "$ORIGIN" ] && [ -f "$ROOT/VERSION.md" ]; then
  FACTORY_ORIGIN=$(grep -A1 '^## Версия фабрики' "$ORIGIN" | tail -n1 | tr -d '')
  FACTORY_VERSION=$(grep -A1 '^## Версия фабрики-источника' "$ROOT/VERSION.md" | tail -n1 | tr -d '')
  if [ -n "$FACTORY_ORIGIN" ] && [ -n "$FACTORY_VERSION" ] && [ "$FACTORY_ORIGIN" != "$FACTORY_VERSION" ]; then
    echo "ОШИБКА: версия фабрики в project-origin.md не совпадает с VERSION.md"
    exit 1
  fi
fi
for f in "$ROOT/VERSION.md" "$ROOT/CHANGELOG.md" "$ROOT/CURRENT_FUNCTIONAL_STATE.md"; do
  if ! rg -q '[А-Яа-яЁё]' "$f"; then
    echo "ОШИБКА: файл $f не содержит русскоязычного содержания"
    exit 1
  fi
done
echo "VERSIONING LAYER ПРОЙДЕН"
