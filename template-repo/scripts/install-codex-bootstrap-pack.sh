#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
if [ -f "$ROOT" ]; then ROOT="$(dirname "$ROOT")"; fi
mkdir -p "$ROOT/.codex/agents" "$ROOT/docs"
if [ -d "./template-repo/scenario-pack" ]; then
  SCENARIO_ROOT="./template-repo/scenario-pack"
else
  SCENARIO_ROOT="./.factory-sources/scenario-pack"
fi
cp -f "$SCENARIO_ROOT/brownfield/10-evidence-pack-completion.md" "$ROOT/docs/" 2>/dev/null || true
cp -f "$SCENARIO_ROOT/brownfield/11-codex-assisted-stabilization.md" "$ROOT/docs/" 2>/dev/null || true
printf 'Codex bootstrap pack установлен в %s
' "$ROOT"
