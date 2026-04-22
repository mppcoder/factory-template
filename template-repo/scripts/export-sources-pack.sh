#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$ROOT/_sources-export"
if [ -d "$ROOT/.factory-sources/scenario-pack" ]; then
  SRC="$ROOT/.factory-sources/scenario-pack"
elif [ -d "$SCRIPT_DIR/../scenario-pack" ]; then
  SRC="$SCRIPT_DIR/../scenario-pack"
else
  echo "ОШИБКА: не найден scenario-pack для экспорта"; exit 1
fi
mkdir -p "$DEST"; rm -rf "$DEST/scenario-pack"; cp -R "$SRC" "$DEST/scenario-pack"; tar -czf "$DEST/scenario-pack.tar.gz" -C "$DEST" scenario-pack
echo "Сценарии экспортированы в: $DEST/scenario-pack"
echo "Reference archive сценариев: $DEST/scenario-pack.tar.gz"
