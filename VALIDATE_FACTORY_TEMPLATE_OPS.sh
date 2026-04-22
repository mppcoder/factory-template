#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
python3 "$ROOT/tools/validate_factory_template_ops_policy.py"
python3 "$ROOT/template-repo/scripts/validate-handoff-response-format.py" "$ROOT/.chatgpt/handoff-response.md"
