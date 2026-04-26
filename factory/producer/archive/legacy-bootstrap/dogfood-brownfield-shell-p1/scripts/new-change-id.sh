#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
STAMP="$(date +%Y%m%d)"
COUNTER_FILE="$ROOT/.change-counter"
if [[ -f "$COUNTER_FILE" ]]; then
  N=$(cat "$COUNTER_FILE")
else
  N=0
fi
N=$((N+1))
printf "%03d" "$N" > "$COUNTER_FILE"
printf "chg-%s-%03d\n" "$STAMP" "$N"
