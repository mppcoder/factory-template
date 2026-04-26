#!/usr/bin/env bash
set -euo pipefail
SRC_DIR="${1:-scenario-pack}"
OUT_FILE="${2:-scenario-pack-export.txt}"
find "$SRC_DIR" -type f | sort > "$OUT_FILE"
echo "Список сценариев выгружен в $OUT_FILE"
