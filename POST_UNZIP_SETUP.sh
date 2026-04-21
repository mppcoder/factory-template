#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for f in launcher.sh SMOKE_TEST.sh EXAMPLES_TEST.sh MATRIX_TEST.sh PRE_RELEASE_AUDIT.sh RELEASE_BUILD.sh CLEAN_VERIFY_ARTIFACTS.sh EXPORT_FACTORY_TEMPLATE_SOURCES.sh GENERATE_BOUNDARY_ACTIONS.sh VALIDATE_FACTORY_TEMPLATE_OPS.sh VALIDATE_FACTORY_FEEDBACK.sh INGEST_FACTORY_FEEDBACK.sh TRIAGE_INCOMING_LEARNINGS.sh DETECT_FACTORY_TEMPLATE_PHASE.sh PHASE_DETECTION_TEST.sh VERIFIED_SYNC.sh EXECUTE_RELEASE_DECISION.sh VALIDATE_VERIFIED_SYNC_PREREQS.sh VALIDATE_RELEASE_DECISION.sh VALIDATE_RELEASE_NOTES_SOURCE.sh VALIDATE_RELEASE_REPORT.sh; do chmod +x "$ROOT/$f" 2>/dev/null || true; done
chmod +x "$ROOT/template-repo/scripts/validate-codex-task-pack.sh" 2>/dev/null || true
chmod +x "$ROOT/template-repo/launcher.sh" 2>/dev/null || true
chmod +x "$ROOT/template-repo/scripts"/*.sh 2>/dev/null || true
chmod +x "$ROOT/workspace-packs/factory-ops"/*.sh 2>/dev/null || true
chmod +x "$ROOT/workspace-packs/factory-ops"/*.py 2>/dev/null || true
chmod +x "$ROOT/tools"/*.py 2>/dev/null || true

validate_drive_folder_url() {
  local url="$1"
  [[ "$url" == https://drive.google.com/drive/folders/* ]] && [[ "$url" != *"<replace-with-project-folder-id>"* ]]
}

if [ -t 0 ] && [ -t 1 ] && [ -f "$ROOT/.chatgpt/google-drive-sources.yaml" ]; then
  CURRENT_DRIVE_URL="$(FACTORY_TEMPLATE_ROOT="$ROOT" python3 - <<'PY'
from pathlib import Path
import os
import yaml
path = Path(os.environ["FACTORY_TEMPLATE_ROOT"]) / ".chatgpt/google-drive-sources.yaml"
data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
block = data.get("google_drive_sources", {})
if isinstance(block, dict):
    print(block.get("folder_url", ""))
else:
    print("")
PY
)"
  while true; do
    read -rp "URL папки Google Drive для Sources contour factory-template [${CURRENT_DRIVE_URL}]: " FACTORY_TEMPLATE_DRIVE_URL
    FACTORY_TEMPLATE_DRIVE_URL="${FACTORY_TEMPLATE_DRIVE_URL:-$CURRENT_DRIVE_URL}"
    FACTORY_TEMPLATE_DRIVE_URL="${FACTORY_TEMPLATE_DRIVE_URL//[$'\r\n']/}"
    if validate_drive_folder_url "$FACTORY_TEMPLATE_DRIVE_URL"; then
      break
    fi
    echo "Нужен реальный URL вида https://drive.google.com/drive/folders/... без placeholder."
  done
  FACTORY_TEMPLATE_DRIVE_URL="$FACTORY_TEMPLATE_DRIVE_URL" FACTORY_TEMPLATE_ROOT="$ROOT" python3 - <<'PY'
from pathlib import Path
import os, yaml
root = Path(os.environ["FACTORY_TEMPLATE_ROOT"])
path = root / ".chatgpt/google-drive-sources.yaml"
data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
block = data.get("google_drive_sources", {})
if not isinstance(block, dict):
    block = {}
block["folder_url"] = os.environ["FACTORY_TEMPLATE_DRIVE_URL"].strip()
data["google_drive_sources"] = block
path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
PY
  echo "Google Drive folder URL для factory-template обновлен: $FACTORY_TEMPLATE_DRIVE_URL"
fi
echo 'Права на запуск обновлены.'
