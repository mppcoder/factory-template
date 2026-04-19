#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$ROOT/POST_UNZIP_SETUP.sh" >/dev/null 2>&1 || true
SCRIPTS="$ROOT/template-repo/scripts"
EXAMPLES=(working-project-examples/example-change-small-fix working-project-examples/example-change-brownfield-audit working-project-examples/example-change-end-to-end)
CHECKS=(validate-project-preset.sh validate-policy-preset.sh validate-change-profile.sh validate-task-graph.sh validate-stage.sh validate-evidence.sh validate-quality.sh validate-handoff.sh check-dod.sh validate-versioning-layer.sh validate-defect-capture.sh validate-alignment.sh)
FAILS=0
printf '%-48s | %-28s | %-8s\n' 'Пример' 'Проверка' 'Статус'
printf '%s\n' '--------------------------------------------------------------------------------------------------------------'
for ex in "${EXAMPLES[@]}"; do
  base="$(basename "$ex")"
  for chk in "${CHECKS[@]}"; do
    if timeout 40s "$SCRIPTS/$chk" "$ROOT/$ex" >/dev/null 2>&1; then
      status='OK'
    else
      status='FAIL'
      FAILS=$((FAILS+1))
    fi
    printf '%-48s | %-28s | %-8s\n' "$base" "$chk" "$status"
  done
done
printf '%s\n' '--------------------------------------------------------------------------------------------------------------'
printf 'ИТОГО: всего проверок=%s, неуспешных=%s\n' "$(( ${#EXAMPLES[@]} * ${#CHECKS[@]} ))" "$FAILS"
if [ "$FAILS" -gt 0 ]; then echo 'EXAMPLES TEST НЕ ПРОЙДЕН'; exit 1; fi
echo 'EXAMPLES TEST ПРОЙДЕН'
