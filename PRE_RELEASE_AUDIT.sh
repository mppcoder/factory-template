#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILS=0
check_absent(){ local pattern="$1"; if find "$ROOT" -path "$ROOT/.release-stage" -prune -o -name "$pattern" -print | grep -q .; then echo "ОШИБКА: найден запрещённый артефакт: $pattern"; FAILS=$((FAILS+1)); fi; }
check_exists(){ local file="$1"; [ -e "$ROOT/$file" ] || { echo "ОШИБКА: отсутствует обязательный файл: $file"; FAILS=$((FAILS+1)); }; }
for p in '.smoke-test' '.bugflow-test' 'audit-smoke-project' '*.log' '__pycache__' '.pytest_cache' '_sources-export' '_factory-sync-export' '_boundary-actions' '.matrix-test'; do check_absent "$p"; done
for f in README.md ENTRY_MODES.md POST_UNZIP_SETUP.sh MATRIX_TEST.sh RELEASE_BUILD.sh VERSION_SYNC_CHECK.sh VALIDATE_FACTORY_TEMPLATE_OPS.sh VALIDATE_FACTORY_FEEDBACK.sh RELEASE_CHECKLIST.md VERIFY_SUMMARY.md RELEASE_NOTE_TEMPLATE.md COMMIT_MESSAGE_GUIDE.md factory-template-ops-policy.yaml factory_template_only_pack/templates/factory-template-boundary-actions.template.md registry/factory-versions.md registry/projects-created.md FACTORY_MANIFEST.yaml template-repo/TEMPLATE_MANIFEST.yaml meta-template-project/RELEASE_NOTES.md; do check_exists "$f"; done
if ! bash "$ROOT/VERSION_SYNC_CHECK.sh"; then FAILS=$((FAILS+1)); fi
if ! bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"; then FAILS=$((FAILS+1)); fi
if rg -n 'factory-v2\.3\.9-alignment-layer' "$ROOT/RELEASE_BUILD.sh" >/dev/null; then echo 'ОШИБКА: RELEASE_BUILD.sh содержит legacy release id'; FAILS=$((FAILS+1)); fi
if [ "$FAILS" -gt 0 ]; then echo 'PRE-RELEASE AUDIT НЕ ПРОЙДЕН'; exit 1; fi
echo 'PRE-RELEASE AUDIT ПРОЙДЕН'
