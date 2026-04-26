#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODE="${1:-full}"
export PYTHONDONTWRITEBYTECODE=1

run_step() {
  local label="$1"
  shift
  printf '\n==> %s\n' "$label"
  "$@"
}

run_deploy_dry_run_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  cp "$ROOT/deploy/.env.example" "$tmp_dir/operator.env"
  {
    echo "DB_PASSWORD=verify-all-long-random-secret"
    echo "BACKUP_ENABLED=true"
    echo "DOMAIN=example.test"
    echo "TLS_EMAIL=ops@example.test"
    echo "ACME_AGREE=true"
  } >> "$tmp_dir/operator.env"

  cat > "$tmp_dir/docker" <<'FAKE_DOCKER'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "compose" && "${2:-}" == "version" ]]; then
  echo "Docker Compose version v2.verify"
  exit 0
fi
if [[ "${1:-}" != "compose" ]]; then
  echo "fake docker only supports compose" >&2
  exit 2
fi
shift
if [[ "${*: -1}" == "--services" ]]; then
  services=("app")
  for arg in "$@"; do
    case "$arg" in
      */app-db.yaml) services+=("db") ;;
      */backup.yaml) services+=("db-backup") ;;
      */reverse-proxy-tls.yaml|*/reverse-proxy.yaml) services+=("reverse-proxy") ;;
    esac
  done
  printf '%s\n' "${services[@]}"
  exit 0
fi
if [[ "${*: -1}" == "config" || " $* " == *" config "* ]]; then
  echo "services:"
  echo "  app: {}"
  exit 0
fi
echo "unsupported fake docker compose call: $*" >&2
exit 2
FAKE_DOCKER
  chmod +x "$tmp_dir/docker"

  PATH="$tmp_dir:$PATH" bash "$ROOT/template-repo/scripts/deploy-dry-run.sh" --env-file "$tmp_dir/operator.env" --preset starter
  PATH="$tmp_dir:$PATH" bash "$ROOT/template-repo/scripts/deploy-dry-run.sh" --env-file "$tmp_dir/operator.env" --preset app-db
  rm -rf "$tmp_dir"
}

run_quick() {
  run_step "POST_UNZIP_SETUP" bash "$ROOT/POST_UNZIP_SETUP.sh"
  run_step "VALIDATE_FACTORY_TEMPLATE_OPS" bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"
  run_step "validate-codex-task-pack" python3 "$ROOT/template-repo/scripts/validate-codex-task-pack.py" "$ROOT"
  run_step "validate-codex-routing" python3 "$ROOT/template-repo/scripts/validate-codex-routing.py" "$ROOT"
  run_step "validate-tree-contract" python3 "$ROOT/template-repo/scripts/validate-tree-contract.py" "$ROOT"
  run_step "validate-mode-parity" python3 "$ROOT/template-repo/scripts/validate-mode-parity.py" "$ROOT"
  run_step "validate-brownfield-transition" python3 "$ROOT/template-repo/scripts/validate-brownfield-transition.py" "$ROOT"
  run_step "validate-greenfield-conversion" python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$ROOT"
  run_step "validate-operator-env-starter" python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset starter
  run_step "validate-operator-env-production-example" python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset production --allow-example-placeholders
  run_step "deploy-dry-run-smoke-starter-app-db" run_deploy_dry_run_smoke
  run_step "validate-spec-traceability" python3 "$ROOT/template-repo/scripts/validate-spec-traceability.py" "$ROOT"
  run_step "validate-release-scorecard" python3 "$ROOT/template-repo/scripts/validate-release-scorecard.py" "$ROOT"
  run_step "validate-25-ga-kpi-evidence" python3 "$ROOT/template-repo/scripts/validate-25-ga-kpi-evidence.py" "$ROOT"
  run_step "validate-human-language-layer" python3 "$ROOT/template-repo/scripts/validate-human-language-layer.py" "$ROOT"
  run_step "PHASE_DETECTION_TEST" bash "$ROOT/PHASE_DETECTION_TEST.sh"
  run_step "VALIDATE_RELEASE_DECISION" bash "$ROOT/VALIDATE_RELEASE_DECISION.sh"
  run_step "VALIDATE_RELEASE_NOTES_SOURCE" bash "$ROOT/VALIDATE_RELEASE_NOTES_SOURCE.sh"
}

run_full() {
  run_step "CLEAN_VERIFY_ARTIFACTS (start)" bash "$ROOT/CLEAN_VERIFY_ARTIFACTS.sh"
  run_quick
  run_step "NOVICE_ONBOARDING_SMOKE" bash "$ROOT/onboarding-smoke/run-novice-e2e.sh"
  run_step "SMOKE_TEST" bash "$ROOT/SMOKE_TEST.sh"
  run_step "EXAMPLES_TEST" bash "$ROOT/EXAMPLES_TEST.sh"
  run_step "MATRIX_TEST" bash "$ROOT/MATRIX_TEST.sh"
  run_step "validate-25-ga-kpi-evidence (after full evidence)" python3 "$ROOT/template-repo/scripts/validate-25-ga-kpi-evidence.py" "$ROOT"
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
