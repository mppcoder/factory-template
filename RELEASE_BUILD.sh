#!/usr/bin/env bash
set -euo pipefail
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия$/{f=1}' "$ROOT/VERSION.md")"
REL_NAME="factory-v${VERSION}"
STAGE="$ROOT/.release-stage/$REL_NAME"
OUT_ZIP="${1:-$ROOT/_incoming/$REL_NAME.zip}"
OUT_DIR_RAW="$(dirname "$OUT_ZIP")"
mkdir -p "$OUT_DIR_RAW"
OUT_DIR="$(cd "$OUT_DIR_RAW" && pwd)"
OUT_BASE="$(basename "$OUT_ZIP")"
MANIFEST_REL="factory/producer/packaging/release-package-manifest.yaml"
MANIFEST_STAGE="$STAGE/$MANIFEST_REL"
MANIFEST_OUT="$OUT_DIR/${OUT_BASE%.zip}.manifest.yaml"
CHECKSUM_OUT="$OUT_DIR/$OUT_BASE.sha256"
BUILD_TIMESTAMP_UTC="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
SOURCE_COMMIT="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || printf 'unknown')"
rm -rf "$STAGE"
rm -f "$OUT_ZIP" "$MANIFEST_OUT" "$CHECKSUM_OUT"
mkdir -p "$STAGE" "$OUT_DIR"
rsync -a --delete --exclude-from="$ROOT/.releaseignore" "$ROOT/" "$STAGE/"
find "$STAGE" -name '*.sh' -exec chmod +x {} +
find "$STAGE" -name '*.py' -exec chmod +x {} + || true
python3 - "$STAGE/bootstrap" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

bootstrap = Path(sys.argv[1])
if not bootstrap.exists():
    raise SystemExit(0)

slug_by_number = {
    "01": "what-is-factory-core",
    "02": "how-to-create-working-project",
    "03": "connect-sources-in-chatgpt-project",
    "04": "stage-pipeline",
    "05": "handoff-to-codex",
    "06": "brownfield-mode",
    "07": "update-template-repo-through-meta-template",
    "08": "change-id-and-task-graph",
    "09": "change-classes-and-modes",
    "10": "policy-presets",
    "11": "project-presets",
    "12": "good-artifact-examples",
    "13": "verify-result-and-fill-brownfield-core",
    "14": "change-from-intake-to-done",
    "15": "small-fix-and-brownfield-audit-examples",
    "16": "artifact-quality-check",
    "17": "registry-and-project-origin",
    "18": "feedback-drift-and-codex-task-pack",
    "19": "factory-improvement-loop",
    "20": "matrix-test-and-controlled-back-sync",
    "21": "mandatory-defect-capture",
    "22": "alignment-layer",
}

for path in sorted(bootstrap.glob("*.md")):
    match = re.match(r"^(\d{2})-", path.name)
    if not match:
        continue
    number = match.group(1)
    slug = slug_by_number.get(number)
    if not slug:
        continue
    target = path.with_name(f"{number}-{slug}.md")
    if path == target:
        continue
    if target.exists():
        raise SystemExit(f"bootstrap filename normalization collision: {target}")
    path.rename(target)
PY
mkdir -p "$(dirname "$MANIFEST_STAGE")"
cat > "$MANIFEST_STAGE" <<EOF
schema: factory-release-package/v1
factory_version: "$VERSION"
source_commit: "$SOURCE_COMMIT"
build_timestamp_utc: "$BUILD_TIMESTAMP_UTC"
archive_filename: "$OUT_BASE"
archive_root: "$REL_NAME/"
npm_path_supported: false
filename_compatibility: ascii-only archive paths
max_archive_path_length: 180
canonical_install_paths:
  - GitHub clone/download
  - release artifact archive
fallback_install_path: manual archive upload to /projects/factory-template/_incoming
included_major_directories:
  - .chatgpt/
  - bootstrap/
  - deploy/
  - docs/
  - factory/
  - project-knowledge/
  - scripts/
  - template-repo/
  - tests/
excluded_transient_paths:
  - .git/
  - .release-stage/
  - .smoke-test/
  - .matrix-test/
  - .pytest_cache/
  - __pycache__/
  - _artifacts/
  - _boundary-actions/
  - _factory-sync-export/
  - _sources-export/
  - .tmp-run/
  - logs and *.log
required_first_run_commands:
  - cd $REL_NAME
  - bash POST_UNZIP_SETUP.sh
  - python3 template-repo/scripts/validate-release-package.py /projects/factory-template/_incoming/$OUT_BASE --checksum /projects/factory-template/_incoming/$OUT_BASE.sha256 --manifest /projects/factory-template/_incoming/${OUT_BASE%.zip}.manifest.yaml
  - bash template-repo/scripts/verify-all.sh quick
verification_status:
  stage_version_sync: pending
  stage_pre_release_audit: pending
  archive_validator: pending
known_limitations:
  - GitHub Release publication is not performed by RELEASE_BUILD.sh.
  - npm install/download path is not supported because this repo has no package.json packaging contract.
EOF
( cd "$STAGE" && bash VERSION_SYNC_CHECK.sh )
( cd "$STAGE" && ALLOW_GIT_DIR=0 bash PRE_RELEASE_AUDIT.sh )
python3 - "$MANIFEST_STAGE" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
text = text.replace("stage_version_sync: pending", "stage_version_sync: passed")
text = text.replace("stage_pre_release_audit: pending", "stage_pre_release_audit: passed")
path.write_text(text, encoding="utf-8")
PY
( cd "$ROOT/.release-stage" && zip -qr "$OUT_ZIP" "$REL_NAME" )
cp "$MANIFEST_STAGE" "$MANIFEST_OUT"
( cd "$OUT_DIR" && sha256sum "$OUT_BASE" > "$CHECKSUM_OUT" )
python3 "$ROOT/template-repo/scripts/validate-release-package.py" "$OUT_ZIP" --checksum "$CHECKSUM_OUT" --manifest "$MANIFEST_OUT"
python3 - "$MANIFEST_STAGE" "$MANIFEST_OUT" <<'PY'
from pathlib import Path
import sys
for raw in sys.argv[1:]:
    path = Path(raw)
    text = path.read_text(encoding="utf-8")
    text = text.replace("archive_validator: pending", "archive_validator: passed")
    path.write_text(text, encoding="utf-8")
PY
( cd "$ROOT/.release-stage" && zip -qr "$OUT_ZIP" "$REL_NAME" )
( cd "$OUT_DIR" && sha256sum "$OUT_BASE" > "$CHECKSUM_OUT" )
python3 "$ROOT/template-repo/scripts/validate-release-package.py" "$OUT_ZIP" --checksum "$CHECKSUM_OUT" --manifest "$MANIFEST_OUT"
echo "Собран чистый релиз: $OUT_ZIP"
echo "Manifest: $MANIFEST_OUT"
echo "SHA256: $CHECKSUM_OUT"
