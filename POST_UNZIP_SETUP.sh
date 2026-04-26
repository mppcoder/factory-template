#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for f in launcher.sh SMOKE_TEST.sh EXAMPLES_TEST.sh MATRIX_TEST.sh PRE_RELEASE_AUDIT.sh RELEASE_BUILD.sh CLEAN_VERIFY_ARTIFACTS.sh EXPORT_FACTORY_TEMPLATE_SOURCES.sh GENERATE_BOUNDARY_ACTIONS.sh VALIDATE_FACTORY_TEMPLATE_OPS.sh VALIDATE_FACTORY_FEEDBACK.sh INGEST_FACTORY_FEEDBACK.sh TRIAGE_INCOMING_LEARNINGS.sh DETECT_FACTORY_TEMPLATE_PHASE.sh PHASE_DETECTION_TEST.sh VERIFIED_SYNC.sh EXECUTE_RELEASE_DECISION.sh VALIDATE_VERIFIED_SYNC_PREREQS.sh VALIDATE_RELEASE_DECISION.sh VALIDATE_RELEASE_NOTES_SOURCE.sh VALIDATE_RELEASE_REPORT.sh; do chmod +x "$ROOT/$f" 2>/dev/null || true; done
chmod +x "$ROOT/template-repo/scripts/validate-codex-task-pack.py" 2>/dev/null || true
chmod +x "$ROOT/template-repo/launcher.sh" 2>/dev/null || true
chmod +x "$ROOT/template-repo/scripts"/*.sh 2>/dev/null || true
chmod +x "$ROOT/template-repo/scripts"/*.py 2>/dev/null || true
chmod +x "$ROOT/factory/producer/extensions/workspace-packs/factory-ops"/*.sh 2>/dev/null || true
chmod +x "$ROOT/factory/producer/extensions/workspace-packs/factory-ops"/*.py 2>/dev/null || true
chmod +x "$ROOT/tools"/*.py 2>/dev/null || true

echo 'Права на запуск обновлены.'
