#!/usr/bin/env bash
set -euo pipefail
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия$/{f=1}' "$ROOT/VERSION.md")"
REL_NAME="factory-v${VERSION}"
STAGE="$ROOT/.release-stage/$REL_NAME"
OUT_ZIP="${1:-$ROOT/../$REL_NAME.zip}"
rm -rf "$STAGE"
rm -f "$OUT_ZIP"
mkdir -p "$STAGE"
rsync -a --delete --exclude-from="$ROOT/.releaseignore" "$ROOT/" "$STAGE/"
find "$STAGE" -name '*.sh' -exec chmod +x {} +
find "$STAGE" -name '*.py' -exec chmod +x {} + || true
( cd "$STAGE" && bash VERSION_SYNC_CHECK.sh )
( cd "$STAGE" && ALLOW_GIT_DIR=0 bash PRE_RELEASE_AUDIT.sh )
( cd "$ROOT/.release-stage" && zip -qr "$OUT_ZIP" "$REL_NAME" )
echo "Собран чистый релиз: $OUT_ZIP"
