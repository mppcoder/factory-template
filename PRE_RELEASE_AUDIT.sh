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
for f in README.md ENTRY_MODES.md POST_UNZIP_SETUP.sh MATRIX_TEST.sh RELEASE_BUILD.sh VERSION_SYNC_CHECK.sh VALIDATE_FACTORY_TEMPLATE_OPS.sh VALIDATE_FACTORY_FEEDBACK.sh DETECT_FACTORY_TEMPLATE_PHASE.sh PHASE_DETECTION_TEST.sh RELEASE_CHECKLIST.md VERIFY_SUMMARY.md RELEASE_NOTES.md RELEASE_NOTE_TEMPLATE.md COMMIT_MESSAGE_GUIDE.md factory-template-ops-policy.yaml .env.example .chatgpt/handoff-response.md docs/releases/release-scorecard.yaml docs/tree-contract.md factory/producer/ops/templates/factory-template-boundary-actions.template.md factory/producer/registry/factory-versions.md factory/producer/registry/projects-created.md FACTORY_MANIFEST.yaml template-repo/TEMPLATE_MANIFEST.yaml template-repo/codex-routing.yaml template-repo/tree-contract.yaml template-repo/compatibility-aliases.yaml template-repo/template/.env.example template-repo/template/.chatgpt/direct-task-response.md template-repo/scripts/validate-tree-contract.py template-repo/scripts/validate-codex-task-pack.py template-repo/scripts/validate-codex-routing.py template-repo/scripts/validate-handoff-response-format.py template-repo/scripts/validate-25-ga-kpi-evidence.py template-repo/scripts/resolve-codex-task-route.py template-repo/scripts/bootstrap-codex-task.py template-repo/scripts/launch-codex-task.sh template-repo/scripts/verified-sync.py template-repo/scripts/execute-release-decision.py template-repo/scripts/validate-verified-sync-prereqs.py template-repo/scripts/validate-release-decision.py template-repo/scripts/validate-release-notes-source.py template-repo/scripts/validate-release-report.py template-repo/scripts/validate-release-scorecard.py docs/releases/factory-template-release-notes.md VERIFIED_SYNC.sh EXECUTE_RELEASE_DECISION.sh VALIDATE_VERIFIED_SYNC_PREREQS.sh VALIDATE_RELEASE_DECISION.sh VALIDATE_RELEASE_NOTES_SOURCE.sh VALIDATE_RELEASE_REPORT.sh; do check_exists "$f"; done
for f in UPGRADE_SUMMARY.md tests/onboarding-smoke/run-novice-e2e.sh tests/onboarding-smoke/ACCEPTANCE_REPORT.md factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh reports/bugs/2026-04-23-factory-ops-utcnow-warning.md; do check_exists "$f"; done
if ! bash "$ROOT/VERSION_SYNC_CHECK.sh"; then FAILS=$((FAILS+1)); fi
if ! bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"; then FAILS=$((FAILS+1)); fi
if ! python3 "$ROOT/template-repo/scripts/validate-tree-contract.py" "$ROOT"; then FAILS=$((FAILS+1)); fi
if ! bash "$ROOT/PHASE_DETECTION_TEST.sh"; then FAILS=$((FAILS+1)); fi
if ! python3 "$ROOT/template-repo/scripts/validate-release-scorecard.py" "$ROOT"; then FAILS=$((FAILS+1)); fi
if ! python3 "$ROOT/template-repo/scripts/validate-25-ga-kpi-evidence.py" "$ROOT"; then FAILS=$((FAILS+1)); fi
if rg -n 'factory-v2\.3\.9-alignment-layer' "$ROOT/RELEASE_BUILD.sh" >/dev/null; then echo 'ОШИБКА: RELEASE_BUILD.sh содержит legacy release id'; FAILS=$((FAILS+1)); fi
if [ "$FAILS" -gt 0 ]; then echo 'PRE-RELEASE AUDIT НЕ ПРОЙДЕН'; exit 1; fi
echo 'PRE-RELEASE AUDIT ПРОЙДЕН'
