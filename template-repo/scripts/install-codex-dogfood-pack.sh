#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
if [ -f "$ROOT" ]; then ROOT="$(dirname "$ROOT")"; fi
mkdir -p "$ROOT/.codex/agents" "$ROOT/docs"
cp -f ./.factory-sources/scenario-pack/brownfield/10-evidence-pack-completion.md "$ROOT/docs/" 2>/dev/null || true
cp -f ./.factory-sources/scenario-pack/brownfield/11-codex-assisted-stabilization.md "$ROOT/docs/" 2>/dev/null || true
printf 'Codex dogfood pack установлен в %s
' "$ROOT"
