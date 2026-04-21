#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
python3 "$ROOT/tools/validate_factory_template_ops_policy.py"
python3 "$ROOT/tools/validate_google_drive_sources_config.py" "$ROOT/.chatgpt/google-drive-sources.yaml"
python3 "$ROOT/tools/validate_google_drive_sources_config.py" "$ROOT/template-repo/template/.chatgpt/google-drive-sources.yaml" --allow-placeholder
python3 "$ROOT/tools/test_gdrive_sources_sync.py"
python3 "$ROOT/template-repo/scripts/validate-handoff-response-format.sh" "$ROOT/.chatgpt/handoff-response.md"
