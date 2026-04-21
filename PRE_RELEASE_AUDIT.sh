#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
FAILS=0
check_absent(){ local pattern="$1"; if find "$ROOT" -path "$ROOT/.release-stage" -prune -o -name "$pattern" -print | grep -q .; then echo "ОШИБКА: найден запрещённый артефакт: $pattern"; FAILS=$((FAILS+1)); fi; }
check_exists(){ local file="$1"; [ -e "$ROOT/$file" ] || { echo "ОШИБКА: отсутствует обязательный файл: $file"; FAILS=$((FAILS+1)); }; }
for p in '.smoke-test' '.bugflow-test' 'audit-smoke-project' '*.log' '__pycache__' '.pytest_cache' '_sources-export' '_factory-sync-export' '_boundary-actions' '.matrix-test' '.factory-runtime'; do check_absent "$p"; done
if [ "${ALLOW_GIT_DIR:-1}" = "0" ]; then
  check_absent '.git'
fi
for f in README.md ENTRY_MODES.md POST_UNZIP_SETUP.sh MATRIX_TEST.sh RELEASE_BUILD.sh VERSION_SYNC_CHECK.sh VALIDATE_FACTORY_TEMPLATE_OPS.sh VALIDATE_FACTORY_FEEDBACK.sh DETECT_FACTORY_TEMPLATE_PHASE.sh PHASE_DETECTION_TEST.sh RELEASE_CHECKLIST.md VERIFY_SUMMARY.md RELEASE_NOTE_TEMPLATE.md COMMIT_MESSAGE_GUIDE.md factory-template-ops-policy.yaml .env.example .chatgpt/google-drive-sources.yaml .chatgpt/handoff-response.md factory_template_only_pack/templates/factory-template-boundary-actions.template.md registry/factory-versions.md registry/projects-created.md FACTORY_MANIFEST.yaml template-repo/TEMPLATE_MANIFEST.yaml template-repo/template/.env.example template-repo/template/.chatgpt/google-drive-sources.yaml template-repo/scripts/validate-google-drive-sources.sh template-repo/scripts/validate-codex-task-pack.sh template-repo/scripts/validate-handoff-response-format.sh template-repo/scripts/verified-sync.sh template-repo/scripts/execute-release-decision.sh template-repo/scripts/validate-verified-sync-prereqs.sh template-repo/scripts/validate-release-decision.sh template-repo/scripts/validate-release-notes-source.sh template-repo/scripts/validate-release-report.sh meta-template-project/RELEASE_NOTES.md VERIFIED_SYNC.sh EXECUTE_RELEASE_DECISION.sh VALIDATE_VERIFIED_SYNC_PREREQS.sh VALIDATE_RELEASE_DECISION.sh VALIDATE_RELEASE_NOTES_SOURCE.sh VALIDATE_RELEASE_REPORT.sh EXPORT_AND_SYNC_FACTORY_TEMPLATE_SOURCES_TO_GDRIVE.sh VERIFY_GDRIVE_SOURCES_SYNC.sh tools/sync_factory_template_sources_to_gdrive_api.py tools/test_gdrive_sources_sync.py tools/validate_google_drive_sources_config.py; do check_exists "$f"; done
if ! bash "$ROOT/VERSION_SYNC_CHECK.sh"; then FAILS=$((FAILS+1)); fi
if ! bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"; then FAILS=$((FAILS+1)); fi
if ! bash "$ROOT/PHASE_DETECTION_TEST.sh"; then FAILS=$((FAILS+1)); fi
if rg -n 'factory-v2\.3\.9-alignment-layer' "$ROOT/RELEASE_BUILD.sh" >/dev/null; then echo 'ОШИБКА: RELEASE_BUILD.sh содержит legacy release id'; FAILS=$((FAILS+1)); fi
if [ "$FAILS" -gt 0 ]; then echo 'PRE-RELEASE AUDIT НЕ ПРОЙДЕН'; exit 1; fi
echo 'PRE-RELEASE AUDIT ПРОЙДЕН'
