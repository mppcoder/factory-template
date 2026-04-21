#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORT_NAME="${FACTORY_TEMPLATE_GDRIVE_EXPORT_NAME:-core-hot-15}"
EXPORT_DIR="$ROOT/_sources-export/factory-template/$EXPORT_NAME"
UPLOAD_DIR="$EXPORT_DIR/upload-to-sources"
REPORT_DIR="${FACTORY_TEMPLATE_SYNC_REPORT_DIR:-$ROOT/_sources-export/factory-template/_sync-reports}"

export PYTHONDONTWRITEBYTECODE=1

bash "$ROOT/EXPORT_FACTORY_TEMPLATE_SOURCES.sh"

if [ ! -d "$EXPORT_DIR" ]; then
  echo "ERROR: export directory not found: $EXPORT_DIR" >&2
  exit 1
fi

if [ ! -d "$UPLOAD_DIR" ]; then
  echo "ERROR: hot export upload dir not found: $UPLOAD_DIR" >&2
  exit 1
fi

if find "$UPLOAD_DIR" -mindepth 2 -type f | grep -q .; then
  echo "ERROR: hot export must stay flat without nested files: $UPLOAD_DIR" >&2
  exit 1
fi

python3 "$ROOT/tools/sync_factory_template_sources_to_gdrive_api.py" \
  "$EXPORT_DIR" \
  --report-dir "$REPORT_DIR" \
  "$@"
