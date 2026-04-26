#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$ROOT/POST_UNZIP_SETUP.sh" >/dev/null 2>&1 || true
SCRIPTS="$ROOT/template-repo/scripts"
EXAMPLES=(factory/producer/reference/examples/example-change-small-fix factory/producer/reference/examples/example-change-brownfield-audit factory/producer/reference/examples/example-change-end-to-end)
CHECKS=(validate-project-preset.py validate-policy-preset.py validate-change-profile.py validate-task-graph.py validate-stage.py validate-evidence.py validate-quality.py validate-handoff.py check-dod.py validate-versioning-layer.py validate-defect-capture.py validate-alignment.py)
FAILS=0
printf '%-48s | %-28s | %-8s\n' 'Пример' 'Проверка' 'Статус'
printf '%s\n' '--------------------------------------------------------------------------------------------------------------'
for ex in "${EXAMPLES[@]}"; do
  base="$(basename "$ex")"
  for chk in "${CHECKS[@]}"; do
    tmp_log="$(mktemp)"
    if timeout 40s "$SCRIPTS/$chk" "$ROOT/$ex" >"$tmp_log" 2>&1; then
      status='OK'
    else
      status='FAIL'
      FAILS=$((FAILS+1))
      printf '\n[DETAIL] %s :: %s\n' "$base" "$chk"
      sed -n '1,80p' "$tmp_log"
    fi
    rm -f "$tmp_log"
    printf '%-48s | %-28s | %-8s\n' "$base" "$chk" "$status"
  done
done
printf '%s\n' '--------------------------------------------------------------------------------------------------------------'
printf 'ИТОГО: всего проверок=%s, неуспешных=%s\n' "$(( ${#EXAMPLES[@]} * ${#CHECKS[@]} ))" "$FAILS"
if [ "$FAILS" -gt 0 ]; then echo 'EXAMPLES TEST НЕ ПРОЙДЕН'; exit 1; fi
echo 'EXAMPLES TEST ПРОЙДЕН'
