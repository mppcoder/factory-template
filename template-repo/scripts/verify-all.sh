#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "$SCRIPT_DIR/../template-repo" ]]; then
  ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
else
  ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi
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
  python3 "$ROOT/template-repo/scripts/validate-operator-env.py" \
    "$ROOT" \
    --env-file "$tmp_dir/operator.env" \
    --preset production \
    --field-pilot-report "$tmp_dir/operator-env-field-pilot.md" >/dev/null
  PATH="$tmp_dir:$PATH" bash "$ROOT/template-repo/scripts/deploy-dry-run.sh" \
    --env-file "$tmp_dir/operator.env" \
    --preset production \
    --field-pilot-report "$tmp_dir/production-vps-field-pilot.md"
  grep -q "evidence boundary" "$tmp_dir/operator-env-field-pilot.md"
  grep -q "real VPS deploy status" "$tmp_dir/production-vps-field-pilot.md"
  rm -rf "$tmp_dir"
}

run_artifact_eval_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  local specs_dir="$ROOT/tests/artifact-eval/specs"
  for spec in \
    master-router \
    direct-task-self-handoff \
    codex-handoff-response \
    done-closeout-external-actions \
    downstream-sync-boundary \
    production-vps-proof-boundary \
    skill-tester-lite \
    feature-execution-lite
  do
    python3 "$ROOT/template-repo/scripts/eval-artifact.py" \
      "$specs_dir/$spec.yaml" \
      --output "$tmp_dir/$spec.md" >/dev/null
    python3 "$ROOT/template-repo/scripts/validate-artifact-eval-report.py" "$tmp_dir/$spec.md"
  done
  python3 "$ROOT/template-repo/scripts/validate-artifact-eval-report.py" "$ROOT"/tests/artifact-eval/reports/*.md
  rm -rf "$tmp_dir"
}

run_task_state_lite_smoke() {
  python3 "$ROOT/template-repo/scripts/validate-task-state-lite.py" "$ROOT/tests/task-state-lite/valid"
  if python3 "$ROOT/template-repo/scripts/validate-task-state-lite.py" "$ROOT/tests/task-state-lite/missing-state" >/tmp/task-state-lite-negative.log 2>&1; then
    echo "task-state-lite negative fixture unexpectedly passed" >&2
    cat /tmp/task-state-lite-negative.log >&2
    return 1
  fi
  rm -f /tmp/task-state-lite-negative.log
}

run_learning_patch_loop_smoke() {
  python3 "$ROOT/template-repo/scripts/validate-learning-patch-loop.py" "$ROOT/tests/learning-patch-loop/valid"
  if python3 "$ROOT/template-repo/scripts/validate-learning-patch-loop.py" "$ROOT/tests/learning-patch-loop/fake-proposal" >/tmp/learning-patch-fake.log 2>&1; then
    echo "learning-patch fake proposal fixture unexpectedly passed" >&2
    cat /tmp/learning-patch-fake.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-learning-patch-loop.py" "$ROOT/tests/learning-patch-loop/overclaim" >/tmp/learning-patch-overclaim.log 2>&1; then
    echo "learning-patch overclaim fixture unexpectedly passed" >&2
    cat /tmp/learning-patch-overclaim.log >&2
    return 1
  fi
  rm -f /tmp/learning-patch-fake.log /tmp/learning-patch-overclaim.log
}

run_project_knowledge_done_loop_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  mkdir -p "$tmp_dir/work/features" "$tmp_dir/work/completed"
  cp -R "$ROOT/tests/project-knowledge-done-loop/feat-closeout-smoke" "$tmp_dir/work/features/feat-closeout-smoke"
  python3 "$ROOT/template-repo/scripts/close-feature-workspace.py" \
    "$tmp_dir/work/features/feat-closeout-smoke" \
    --root "$ROOT" \
    --archive-base "$tmp_dir/work/completed" \
    --artifact-eval-report "$ROOT/tests/artifact-eval/reports/feature-execution-lite.md"
  python3 "$ROOT/template-repo/scripts/validate-project-knowledge-update.py" \
    "$ROOT" \
    --workspace "$tmp_dir/work/completed/feat-closeout-smoke"
  rm -rf "$tmp_dir"
}

project_preset() {
  python3 - "$ROOT/.chatgpt/project-profile.yaml" <<'PY'
from pathlib import Path
import sys
try:
    import yaml
except Exception:
    print("")
    raise SystemExit(0)
path = Path(sys.argv[1])
if not path.exists():
    print("")
    raise SystemExit(0)
data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
print(data.get("project_preset", ""))
PY
}

run_generated_project_quick() {
  run_step "validate-project-preset" python3 "$ROOT/scripts/validate-project-preset.py" "$ROOT"
  run_step "validate-policy-preset" python3 "$ROOT/scripts/validate-policy-preset.py" "$ROOT"
  run_step "validate-change-profile" python3 "$ROOT/scripts/validate-change-profile.py" "$ROOT"
  run_step "validate-task-graph" python3 "$ROOT/scripts/validate-task-graph.py" "$ROOT"
  run_step "validate-stage" python3 "$ROOT/scripts/validate-stage.py" "$ROOT"
  run_step "validate-task-state-lite" python3 "$ROOT/scripts/validate-task-state-lite.py" "$ROOT"
  run_step "validate-feature-execution-lite" python3 "$ROOT/scripts/validate-feature-execution-lite.py" "$ROOT"
  run_step "validate-learning-patch-loop" python3 "$ROOT/scripts/validate-learning-patch-loop.py" "$ROOT"
  run_step "validate-versioning-layer" python3 "$ROOT/scripts/validate-versioning-layer.py" "$ROOT"
  run_step "validate-defect-capture" python3 "$ROOT/scripts/validate-defect-capture.py" "$ROOT"
  run_step "validate-alignment" python3 "$ROOT/scripts/validate-alignment.py" "$ROOT"
  run_step "validate-tree-contract" python3 "$ROOT/scripts/validate-tree-contract.py" "$ROOT"
  run_step "validate-mode-parity" python3 "$ROOT/scripts/validate-mode-parity.py" "$ROOT"
  case "$(project_preset)" in
    brownfield-*)
      run_step "validate-brownfield-transition" python3 "$ROOT/scripts/validate-brownfield-transition.py" "$ROOT"
      ;;
    greenfield-product|"")
      run_step "validate-greenfield-conversion" python3 "$ROOT/scripts/validate-greenfield-conversion.py" "$ROOT"
      ;;
  esac
  run_step "validate-codex-task-pack" python3 "$ROOT/scripts/validate-codex-task-pack.py" "$ROOT"
  run_step "validate-codex-routing" python3 "$ROOT/scripts/validate-codex-routing.py" "$ROOT"
  run_step "validate-evidence" python3 "$ROOT/scripts/validate-evidence.py" "$ROOT"
  run_step "validate-quality" python3 "$ROOT/scripts/validate-quality.py" "$ROOT"
}

run_quick() {
  if [[ ! -f "$ROOT/POST_UNZIP_SETUP.sh" ]]; then
    run_generated_project_quick
    return
  fi
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
  run_step "validate-task-state-lite" python3 "$ROOT/template-repo/scripts/validate-task-state-lite.py" "$ROOT/template-repo/template"
  run_step "task-state-lite-smoke" run_task_state_lite_smoke
  run_step "validate-feature-execution-lite" python3 "$ROOT/template-repo/scripts/validate-feature-execution-lite.py" "$ROOT"
  run_step "validate-learning-patch-loop" python3 "$ROOT/template-repo/scripts/validate-learning-patch-loop.py" "$ROOT"
  run_step "learning-patch-loop-smoke" run_learning_patch_loop_smoke
  run_step "artifact-eval-smoke" run_artifact_eval_smoke
  run_step "project-knowledge-done-loop-smoke" run_project_knowledge_done_loop_smoke
  run_step "validate-release-scorecard" python3 "$ROOT/template-repo/scripts/validate-release-scorecard.py" "$ROOT"
  run_step "validate-25-ga-kpi-evidence" python3 "$ROOT/template-repo/scripts/validate-25-ga-kpi-evidence.py" "$ROOT"
  run_step "validate-human-language-layer" python3 "$ROOT/template-repo/scripts/validate-human-language-layer.py" "$ROOT"
  run_step "PHASE_DETECTION_TEST" bash "$ROOT/PHASE_DETECTION_TEST.sh"
  run_step "VALIDATE_RELEASE_DECISION" bash "$ROOT/VALIDATE_RELEASE_DECISION.sh"
  run_step "VALIDATE_RELEASE_NOTES_SOURCE" bash "$ROOT/VALIDATE_RELEASE_NOTES_SOURCE.sh"
}

run_full() {
  if [[ ! -f "$ROOT/CLEAN_VERIFY_ARTIFACTS.sh" ]]; then
    run_generated_project_quick
    return
  fi
  run_step "CLEAN_VERIFY_ARTIFACTS (start)" bash "$ROOT/CLEAN_VERIFY_ARTIFACTS.sh"
  run_quick
  run_step "NOVICE_ONBOARDING_SMOKE" bash "$ROOT/tests/onboarding-smoke/run-novice-e2e.sh"
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
