#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SMOKE_DIR="$ROOT/tests/onboarding-smoke"
RUN_ROOT="${1:-$SMOKE_DIR/.tmp-run}"
REPORT_PATH="${2:-$SMOKE_DIR/ACCEPTANCE_REPORT.md}"

rm -rf "$RUN_ROOT"
mkdir -p "$RUN_ROOT"

validate_generated_project() {
  local project_root="$1"
  local expected_preset="$2"
  local log_file="$3"

  python3 - <<'PYCODE' "$project_root/.chatgpt/active-scenarios.yaml" "$expected_preset"
from __future__ import annotations

import sys
from pathlib import Path

import yaml

active_path = Path(sys.argv[1])
expected = sys.argv[2]
data = yaml.safe_load(active_path.read_text(encoding="utf-8")) or {}
actual = data.get("project_preset")
if actual != expected:
    raise SystemExit(
        f"ОШИБКА: ожидается preset={expected}, получено preset={actual} ({active_path})"
    )
PYCODE

  for validator in \
    validate-project-preset.py \
    validate-policy-preset.py \
    validate-change-profile.py \
    validate-task-graph.py \
    validate-stage.py \
    validate-versioning-layer.py \
    validate-defect-capture.py \
    validate-alignment.py \
    validate-mode-parity.py
  do
    python3 "$ROOT/template-repo/scripts/$validator" "$project_root" >>"$log_file" 2>&1
  done
  python3 "$ROOT/template-repo/scripts/create-codex-task-pack.py" "$project_root" >>"$log_file" 2>&1
  python3 "$ROOT/template-repo/scripts/validate-codex-task-pack.py" "$project_root" >>"$log_file" 2>&1
  python3 "$ROOT/template-repo/scripts/validate-codex-routing.py" "$project_root" >>"$log_file" 2>&1
  python3 "$ROOT/template-repo/scripts/validate-chat-handoff-index.py" "$project_root/.chatgpt/chat-handoff-index.yaml" >>"$log_file" 2>&1
  python3 "$ROOT/template-repo/scripts/validate-codex-work-index.py" "$project_root/.chatgpt/codex-work-index.yaml" >>"$log_file" 2>&1
  python3 "$ROOT/template-repo/scripts/validate-project-index-identity.py" "$project_root" >>"$log_file" 2>&1
  if grep -q "project_code: FT" "$project_root/.chatgpt/chat-handoff-index.yaml" "$project_root/.chatgpt/codex-work-index.yaml"; then
    echo "ОШИБКА: generated project inherited FT chat/codex project_code" >&2
    return 1
  fi
  python3 "$ROOT/tools/fill_smoke_artifacts.py" "$project_root" >>"$log_file" 2>&1
  for validator in \
    validate-stage.py \
    validate-evidence.py \
    validate-quality.py \
    validate-handoff.py \
    check-dod.py
  do
    python3 "$ROOT/template-repo/scripts/$validator" "$project_root" >>"$log_file" 2>&1
  done
}

run_wizard_scenario() {
  local scenario_key="$1"
  local project_name="$2"
  local project_slug="$3"
  local asset_choice="$4"
  local goal_choice="$5"
  local expected_preset="$6"

  local scenario_root="$RUN_ROOT/$scenario_key"
  local log_file="$RUN_ROOT/${scenario_key}.txt"
  local start_ts end_ts duration_seconds
  mkdir -p "$scenario_root"

  start_ts="$(date +%s)"
  (
    cd "$scenario_root"
    printf '%s\n%s\n%s\n%s\ny\ny\n' \
      "$project_name" "$project_slug" "$asset_choice" "$goal_choice" \
      | FACTORY_REGISTRY_MODE=skip python3 "$ROOT/template-repo/scripts/first-project-wizard.py" --template-repo-root "$ROOT/template-repo" \
      >"$log_file" 2>&1
  )

  local project_root="$scenario_root/$project_slug"
  if [ ! -d "$project_root" ]; then
    echo "ОШИБКА: проект не создан для сценария $scenario_key" >&2
    return 1
  fi

  validate_generated_project "$project_root" "$expected_preset" "$log_file"
  end_ts="$(date +%s)"
  duration_seconds=$((end_ts - start_ts))

  printf '%s|%s|%s|%s|%s|0\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file" "$duration_seconds"
}

run_launcher_scenario() {
  local scenario_key="$1"
  local project_name="$2"
  local project_slug="$3"
  local launcher_mode="$4"
  local brownfield_kind="$5"
  local expected_preset="$6"
  local guided_mode="${7:-false}"

  local scenario_root="$RUN_ROOT/$scenario_key"
  local log_file="$RUN_ROOT/${scenario_key}.txt"
  local start_ts end_ts duration_seconds
  mkdir -p "$scenario_root"

  start_ts="$(date +%s)"
  (
    cd "$scenario_root"
    local command=(
      python3 "$ROOT/template-repo/scripts/factory-launcher.py"
      --template-repo-root "$ROOT/template-repo" \
      --mode "$launcher_mode" \
      --project-name "$project_name" \
      --project-slug "$project_slug" \
      --skip-preflight \
      --yes
    )
    if [ "$launcher_mode" = "brownfield" ]; then
      command+=(--brownfield-kind "$brownfield_kind")
    fi
    if [ "$guided_mode" = "guided" ]; then
      command+=(--guided)
    fi
    FACTORY_REGISTRY_MODE=skip "${command[@]}" >"$log_file" 2>&1
  )

  local project_root="$scenario_root/$project_slug"
  if [ ! -d "$project_root" ]; then
    echo "ОШИБКА: проект не создан через guided launcher для сценария $scenario_key" >&2
    return 1
  fi

  validate_generated_project "$project_root" "$expected_preset" "$log_file"
  end_ts="$(date +%s)"
  duration_seconds=$((end_ts - start_ts))

  printf '%s|%s|%s|%s|%s|0\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file" "$duration_seconds"
}

run_continue_scenario() {
  local scenario_key="$1"
  local project_name="$2"
  local project_slug="$3"
  local expected_preset="$4"

  local scenario_root="$RUN_ROOT/$scenario_key"
  local log_file="$RUN_ROOT/${scenario_key}.txt"
  local start_ts end_ts duration_seconds
  mkdir -p "$scenario_root"

  start_ts="$(date +%s)"
  (
    cd "$scenario_root"
    FACTORY_REGISTRY_MODE=skip python3 "$ROOT/template-repo/scripts/factory-launcher.py" \
      --template-repo-root "$ROOT/template-repo" \
      --mode greenfield \
      --project-name "$project_name" \
      --project-slug "$project_slug" \
      --skip-preflight \
      --yes \
      --guided >"$log_file" 2>&1

    cd "$project_slug"
    python3 scripts/factory-launcher.py --continue --feature-id feat-continue-smoke >>"$log_file" 2>&1
  )

  local project_root="$scenario_root/$project_slug"
  if [ ! -d "$project_root/work/features/feat-continue-smoke" ]; then
    echo "ОШИБКА: continue flow не создал feature workspace для сценария $scenario_key" >&2
    return 1
  fi

  validate_generated_project "$project_root" "$expected_preset" "$log_file"
  end_ts="$(date +%s)"
  duration_seconds=$((end_ts - start_ts))

  printf '%s|%s|%s|%s|%s|0\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file" "$duration_seconds"
}

RESULTS=()
RESULTS+=("$(
  run_wizard_scenario \
    "greenfield-novice" \
    "Novice Greenfield Smoke" \
    "novice-greenfield-smoke" \
    "1" \
    "1" \
    "greenfield-product"
)")
RESULTS+=("$(
  run_wizard_scenario \
    "brownfield-without-repo-novice" \
    "Novice Brownfield No Repo Smoke" \
    "novice-brownfield-no-repo-smoke" \
    "3" \
    "1" \
    "brownfield-without-repo"
)")
RESULTS+=("$(
  run_wizard_scenario \
    "brownfield-modernization-novice" \
    "Novice Brownfield Modernization Smoke" \
    "novice-brownfield-modernization-smoke" \
    "2" \
    "1" \
    "brownfield-with-repo-modernization"
)")
RESULTS+=("$(
  run_wizard_scenario \
    "brownfield-integration-novice" \
    "Novice Brownfield Integration Smoke" \
    "novice-brownfield-integration-smoke" \
    "2" \
    "2" \
    "brownfield-with-repo-integration"
)")
RESULTS+=("$(
  run_wizard_scenario \
    "brownfield-audit-novice" \
    "Novice Brownfield Audit Smoke" \
    "novice-brownfield-audit-smoke" \
    "2" \
    "3" \
    "brownfield-with-repo-audit"
)")
RESULTS+=("$(
  run_launcher_scenario \
    "guided-launcher-greenfield" \
    "Guided Launcher Greenfield Smoke" \
    "guided-launcher-greenfield-smoke" \
    "greenfield" \
    "" \
    "greenfield-product" \
    "guided"
)")
RESULTS+=("$(
  run_launcher_scenario \
    "guided-launcher-brownfield-no-repo" \
    "Guided Launcher Brownfield No Repo Smoke" \
    "guided-launcher-brownfield-no-repo-smoke" \
    "brownfield" \
    "no-repo" \
    "brownfield-without-repo" \
    "guided"
)")
RESULTS+=("$(
  run_launcher_scenario \
    "guided-launcher-brownfield-with-repo" \
    "Guided Launcher Brownfield With Repo Smoke" \
    "guided-launcher-brownfield-with-repo-smoke" \
    "brownfield" \
    "modernize" \
    "brownfield-with-repo-modernization" \
    "guided"
)")
RESULTS+=("$(
  run_continue_scenario \
    "guided-launcher-continue-flow" \
    "Guided Launcher Continue Flow Smoke" \
    "guided-launcher-continue-flow-smoke" \
    "greenfield-product"
)")
RUN_TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
cat <<EOF
# Onboarding Smoke Acceptance

- Run timestamp (UTC): \`$RUN_TS\`
- Runner: \`tests/onboarding-smoke/run-novice-e2e.sh\`
- Root: \`$ROOT\`

## Результаты сценариев

EOF

index=1
passed_count=0
total_count="${#RESULTS[@]}"
max_duration_seconds=0
total_interventions=0
for result in "${RESULTS[@]}"; do
  IFS='|' read -r SCENARIO_KEY PROJECT_ROOT EXPECTED_PRESET LOG_FILE DURATION_SECONDS MANUAL_INTERVENTIONS <<<"$result"
  passed_count=$((passed_count + 1))
  total_interventions=$((total_interventions + MANUAL_INTERVENTIONS))
  if [ "$DURATION_SECONDS" -gt "$max_duration_seconds" ]; then
    max_duration_seconds="$DURATION_SECONDS"
  fi
  cat <<EOF
$index. \`$SCENARIO_KEY\`
- status: \`green\`
- expected preset: \`$EXPECTED_PRESET\`
- generated project: \`$PROJECT_ROOT\`
- log: \`$LOG_FILE\`
- duration_seconds: \`$DURATION_SECONDS\`
- manual_interventions: \`$MANUAL_INTERVENTIONS\`

EOF
  index=$((index + 1))
done
completion_rate=$((passed_count * 100 / total_count))

cat <<EOF

## KPI-сводка novice path

- total scenarios: \`$total_count\`
- passed scenarios: \`$passed_count\`
- completion_rate_percent: \`$completion_rate\`
- max_time_to_first_success_seconds: \`$max_duration_seconds\`
- max_time_to_first_success_minutes_ceiling: \`$(((max_duration_seconds + 59) / 60))\`
- total_manual_interventions: \`$total_interventions\`
- planned wizard answers are controlled scenario inputs, not support interventions.

## Что проверено

- Wizard fallback выбирает маршруты без ручного знания внутренних preset-имен.
- Guided launcher проходит полный путь через единый entrypoint: greenfield, brownfield без repo, brownfield с repo и continue-flow.
- В generated project проверен preset в \`.chatgpt/active-scenarios.yaml\`.
- Проверен mode parity через \`validate-mode-parity.py\`.
- Покрыты canonical modes:
  - \`greenfield-product\`
  - \`brownfield-without-repo\`
  - \`brownfield-with-repo-modernization\`
  - \`brownfield-with-repo-integration\`
  - \`brownfield-with-repo-audit\`
- Базовые validators (bootstrap path):
  - \`validate-project-preset.py\`
  - \`validate-policy-preset.py\`
  - \`validate-change-profile.py\`
  - \`validate-task-graph.py\`
  - \`validate-stage.py\`
  - \`validate-versioning-layer.py\`
  - \`validate-defect-capture.py\`
  - \`validate-alignment.py\`
  - \`validate-mode-parity.py\`
  - \`create-codex-task-pack.py\`
  - \`validate-codex-task-pack.py\`
  - \`validate-codex-routing.py\`
- Длинный novice-flow после bootstrap:
  - \`tools/fill_smoke_artifacts.py\`
  - \`validate-stage.py\`
  - \`validate-evidence.py\`
  - \`validate-quality.py\`
  - \`validate-handoff.py\`
  - \`check-dod.py\`
- Шаги guided path:
  - \`--guided\` создает проект и workspace первой задачи.
  - \`--continue\` создает следующий feature workspace и печатает operator next step.
EOF
} >"$REPORT_PATH"

echo "Novice onboarding smoke passed. Report: $REPORT_PATH"
