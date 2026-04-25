#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_DIR="$ROOT/onboarding-smoke"
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
  mkdir -p "$scenario_root"

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

  printf '%s|%s|%s|%s\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file"
}

run_launcher_scenario() {
  local scenario_key="$1"
  local project_name="$2"
  local project_slug="$3"
  local launcher_mode="$4"
  local brownfield_kind="$5"
  local expected_preset="$6"

  local scenario_root="$RUN_ROOT/$scenario_key"
  local log_file="$RUN_ROOT/${scenario_key}.txt"
  mkdir -p "$scenario_root"

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
    FACTORY_REGISTRY_MODE=skip "${command[@]}" >"$log_file" 2>&1
  )

  local project_root="$scenario_root/$project_slug"
  if [ ! -d "$project_root" ]; then
    echo "ОШИБКА: проект не создан через guided launcher для сценария $scenario_key" >&2
    return 1
  fi

  validate_generated_project "$project_root" "$expected_preset" "$log_file"

  printf '%s|%s|%s|%s\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file"
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
    "greenfield-product"
)")
RESULTS+=("$(
  run_launcher_scenario \
    "guided-launcher-brownfield-audit" \
    "Guided Launcher Brownfield Audit Smoke" \
    "guided-launcher-brownfield-audit-smoke" \
    "brownfield" \
    "audit" \
    "brownfield-with-repo-audit"
)")
RUN_TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
cat <<EOF
# Onboarding Smoke Acceptance

- Run timestamp (UTC): \`$RUN_TS\`
- Runner: \`onboarding-smoke/run-novice-e2e.sh\`
- Root: \`$ROOT\`

## Scenario Results

EOF

index=1
for result in "${RESULTS[@]}"; do
  IFS='|' read -r SCENARIO_KEY PROJECT_ROOT EXPECTED_PRESET LOG_FILE <<<"$result"
  cat <<EOF
$index. \`$SCENARIO_KEY\`
- status: \`green\`
- expected preset: \`$EXPECTED_PRESET\`
- generated project: \`$PROJECT_ROOT\`
- log: \`$LOG_FILE\`

EOF
  index=$((index + 1))
done

cat <<EOF

## What Was Verified

- Beginner wizard route selection without manual preset terminology for all canonical presets.
- Guided launcher route selection and project creation through the unified entrypoint for greenfield and brownfield.
- Generated project preset alignment in \`.chatgpt/active-scenarios.yaml\`.
- Mode parity validation through \`validate-mode-parity.py\`.
- Canonical modes covered:
  - \`greenfield-product\`
  - \`brownfield-without-repo\`
  - \`brownfield-with-repo-modernization\`
  - \`brownfield-with-repo-integration\`
  - \`brownfield-with-repo-audit\`
- Baseline validators (bootstrap path):
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
- Long-flow novice acceptance (post-bootstrap):
  - \`tools/fill_smoke_artifacts.py\`
  - \`validate-stage.py\`
  - \`validate-evidence.py\`
  - \`validate-quality.py\`
  - \`validate-handoff.py\`
  - \`check-dod.py\`
EOF
} >"$REPORT_PATH"

echo "Novice onboarding smoke passed. Report: $REPORT_PATH"
