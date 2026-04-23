#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_DIR="$ROOT/onboarding-smoke"
RUN_ROOT="${1:-$SMOKE_DIR/.tmp-run}"
REPORT_PATH="${2:-$SMOKE_DIR/ACCEPTANCE_REPORT.md}"

rm -rf "$RUN_ROOT"
mkdir -p "$RUN_ROOT"

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
    validate-alignment.py
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

  printf '%s|%s|%s|%s\n' "$scenario_key" "$project_root" "$expected_preset" "$log_file"
}

GREENFIELD_RESULT="$(
  run_wizard_scenario \
    "greenfield-novice" \
    "Novice Greenfield Smoke" \
    "novice-greenfield-smoke" \
    "1" \
    "1" \
    "greenfield-product"
)"

BROWNFIELD_RESULT="$(
  run_wizard_scenario \
    "brownfield-novice" \
    "Novice Brownfield Smoke" \
    "novice-brownfield-smoke" \
    "2" \
    "1" \
    "brownfield-with-repo-modernization"
)"

IFS='|' read -r GF_KEY GF_PROJECT GF_PRESET GF_LOG <<<"$GREENFIELD_RESULT"
IFS='|' read -r BF_KEY BF_PROJECT BF_PRESET BF_LOG <<<"$BROWNFIELD_RESULT"
RUN_TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat >"$REPORT_PATH" <<EOF
# Onboarding Smoke Acceptance

- Run timestamp (UTC): \`$RUN_TS\`
- Runner: \`onboarding-smoke/run-novice-e2e.sh\`
- Root: \`$ROOT\`

## Scenario Results

1. \`$GF_KEY\`
- status: \`green\`
- expected preset: \`$GF_PRESET\`
- generated project: \`$GF_PROJECT\`
- log: \`$GF_LOG\`

2. \`$BF_KEY\`
- status: \`green\`
- expected preset: \`$BF_PRESET\`
- generated project: \`$BF_PROJECT\`
- log: \`$BF_LOG\`

## What Was Verified

- Beginner wizard route selection without manual preset terminology.
- Generated project preset alignment in \`.chatgpt/active-scenarios.yaml\`.
- Baseline validators (bootstrap path):
  - \`validate-project-preset.py\`
  - \`validate-policy-preset.py\`
  - \`validate-change-profile.py\`
  - \`validate-task-graph.py\`
  - \`validate-stage.py\`
  - \`validate-versioning-layer.py\`
  - \`validate-defect-capture.py\`
  - \`validate-alignment.py\`
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

echo "Novice onboarding smoke passed. Report: $REPORT_PATH"
