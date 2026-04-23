#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODE="${1:-full}"

run_step() {
  local label="$1"
  shift
  printf '\n==> %s\n' "$label"
  "$@"
}

run_quick() {
  run_step "POST_UNZIP_SETUP" bash "$ROOT/POST_UNZIP_SETUP.sh"
  run_step "VALIDATE_FACTORY_TEMPLATE_OPS" bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"
  run_step "validate-codex-task-pack" python3 "$ROOT/template-repo/scripts/validate-codex-task-pack.py" "$ROOT"
  run_step "validate-codex-routing" python3 "$ROOT/template-repo/scripts/validate-codex-routing.py" "$ROOT"
  run_step "PHASE_DETECTION_TEST" bash "$ROOT/PHASE_DETECTION_TEST.sh"
  run_step "VALIDATE_RELEASE_DECISION" bash "$ROOT/VALIDATE_RELEASE_DECISION.sh"
  run_step "VALIDATE_RELEASE_NOTES_SOURCE" bash "$ROOT/VALIDATE_RELEASE_NOTES_SOURCE.sh"
}

run_full() {
  run_step "CLEAN_VERIFY_ARTIFACTS (start)" bash "$ROOT/CLEAN_VERIFY_ARTIFACTS.sh"
  run_quick
  run_step "SMOKE_TEST" bash "$ROOT/SMOKE_TEST.sh"
  run_step "EXAMPLES_TEST" bash "$ROOT/EXAMPLES_TEST.sh"
  run_step "MATRIX_TEST" bash "$ROOT/MATRIX_TEST.sh"
  run_step "CLEAN_VERIFY_ARTIFACTS (before audit)" bash "$ROOT/CLEAN_VERIFY_ARTIFACTS.sh"
  run_step "PRE_RELEASE_AUDIT" bash "$ROOT/PRE_RELEASE_AUDIT.sh"
}

usage() {
  cat <<USAGE
Usage: bash template-repo/scripts/verify-all.sh [quick|full|ci]

Modes:
  quick  - structural, routing/handoff, and release-facing validators.
  full   - quick + smoke/examples/matrix + pre-release audit (default).
  ci     - alias of full.
USAGE
}

case "$MODE" in
  quick)
    run_quick
    ;;
  full|ci)
    run_full
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    usage >&2
    exit 2
    ;;
esac

printf '\nVERIFY-ALL ПРОЙДЕН (%s)\n' "$MODE"
