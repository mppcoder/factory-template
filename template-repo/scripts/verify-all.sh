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
  grep -q "sanitized runtime transcript" "$tmp_dir/operator-env-field-pilot.md"
  grep -q "real VPS deploy status" "$tmp_dir/production-vps-field-pilot.md"
  grep -q "sanitized runtime transcript" "$tmp_dir/production-vps-field-pilot.md"
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
    vps-remote-ssh-orchestration \
    skill-tester-lite \
    feature-execution-lite \
    handoff-transcript-eval \
    project-knowledge-reuse-proof \
    beginner-full-handoff-ux \
    gpt-5-5-prompt-contract
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

run_downstream_application_proof_smoke() {
  python3 "$ROOT/template-repo/scripts/validate-downstream-application-proof.py" \
    "$ROOT/tests/downstream-application-proof/valid/downstream-application-proof-report.md"
  if python3 "$ROOT/template-repo/scripts/validate-downstream-application-proof.py" \
    "$ROOT/tests/downstream-application-proof/missing-evidence/downstream-application-proof-report.md" \
    >/tmp/downstream-application-proof-negative.log 2>&1; then
    echo "downstream application proof negative fixture unexpectedly passed" >&2
    cat /tmp/downstream-application-proof-negative.log >&2
    return 1
  fi
  rm -f /tmp/downstream-application-proof-negative.log
}

run_codex_orchestration_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" "$ROOT"
  python3 "$ROOT/template-repo/scripts/orchestrate-codex-handoff.py" \
    --root "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/valid/parent-plan.yaml" \
    --report "$tmp_dir/parent-orchestration-report.md" >/dev/null
  if python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" \
    "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/missing-child-routing/parent-plan.yaml" \
    >/tmp/codex-orchestration-missing-routing.log 2>&1; then
    echo "codex orchestration missing-routing negative fixture unexpectedly passed" >&2
    cat /tmp/codex-orchestration-missing-routing.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" \
    "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml" \
    >/tmp/codex-orchestration-secret.log 2>&1; then
    echo "codex orchestration secret-like negative fixture unexpectedly passed" >&2
    cat /tmp/codex-orchestration-secret.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" \
    "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/multi-block-handoff/parent-plan.yaml" \
    >/tmp/codex-orchestration-multi-block.log 2>&1; then
    echo "codex orchestration multi-block negative fixture unexpectedly passed" >&2
    cat /tmp/codex-orchestration-multi-block.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" \
    "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/user-action-as-subtask/parent-plan.yaml" \
    >/tmp/codex-orchestration-user-action.log 2>&1; then
    echo "codex orchestration user-action negative fixture unexpectedly passed" >&2
    cat /tmp/codex-orchestration-user-action.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-codex-orchestration.py" \
    "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/bad-placeholder/parent-plan.yaml" \
    >/tmp/codex-orchestration-bad-placeholder.log 2>&1; then
    echo "codex orchestration bad-placeholder negative fixture unexpectedly passed" >&2
    cat /tmp/codex-orchestration-bad-placeholder.log >&2
    return 1
  fi
  rm -f /tmp/codex-orchestration-missing-routing.log /tmp/codex-orchestration-secret.log /tmp/codex-orchestration-multi-block.log /tmp/codex-orchestration-user-action.log /tmp/codex-orchestration-bad-placeholder.log
  rm -rf "$tmp_dir"
}

run_codex_orchestration_runner_negative_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  local stdout_log="$tmp_dir/runner-negative.stdout"
  local stderr_log="$tmp_dir/runner-negative.stderr"
  local report_path="$tmp_dir/parent-orchestration-report.md"
  local sessions_dir="$tmp_dir/sessions"

  if python3 "$ROOT/template-repo/scripts/orchestrate-codex-handoff.py" \
    --root "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml" \
    --report "$report_path" \
    >"$stdout_log" 2>"$stderr_log"; then
    echo "FAIL: invalid orchestration plan unexpectedly passed runner validation" >&2
    cat "$stdout_log" >&2
    cat "$stderr_log" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  if find "$sessions_dir" -type f -name '*.md' 2>/dev/null | grep -q .; then
    echo "FAIL: invalid orchestration plan wrote child session files before failing" >&2
    find "$sessions_dir" -type f -name '*.md' -print >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  if [[ -e "$sessions_dir/secret-child.md" ]]; then
    echo "FAIL: invalid orchestration plan wrote child session files before failing" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  if grep -RE "API_KEY[[:space:]]*=" "$tmp_dir" >/dev/null 2>&1; then
    echo "FAIL: invalid orchestration plan wrote secret-like prompt content to output artifacts" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  rm -rf "$tmp_dir"
}

run_plan6_productization_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  python3 "$ROOT/template-repo/scripts/validate-parent-orchestration-plan.py" \
    --root "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/valid/parent-plan.yaml"
  python3 "$ROOT/template-repo/scripts/validate-parent-orchestration-plan.py" \
    --root "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/future-placeholder/parent-plan.yaml"
  if python3 "$ROOT/template-repo/scripts/validate-parent-orchestration-plan.py" \
    --root "$ROOT" \
    --plan "$ROOT/tests/codex-orchestration/fixtures/missing-child-routing/parent-plan.yaml" \
    >/tmp/plan6-parent-plan-negative.log 2>&1; then
    echo "plan6 parent-plan negative fixture unexpectedly passed" >&2
    cat /tmp/plan6-parent-plan-negative.log >&2
    return 1
  fi
  rm -f /tmp/plan6-parent-plan-negative.log

  python3 "$ROOT/template-repo/scripts/validate-orchestration-cockpit.py" \
    "$ROOT/template-repo/template/.chatgpt/orchestration-cockpit.yaml"
  python3 "$ROOT/template-repo/scripts/render-orchestration-cockpit.py" \
    --input "$ROOT/template-repo/template/.chatgpt/orchestration-cockpit.yaml" \
    --output "$tmp_dir/orchestration-cockpit.md"
  grep -q "Route receipt" "$tmp_dir/orchestration-cockpit.md"
  grep -q "Placeholder replacements" "$tmp_dir/orchestration-cockpit.md"

  python3 "$ROOT/template-repo/scripts/validate-route-explain.py" "$ROOT"
  python3 "$ROOT/template-repo/scripts/validate-beginner-handoff-ux.py" \
    "$ROOT/tests/beginner-handoff-ux/positive/handoff.md"
  if python3 "$ROOT/template-repo/scripts/validate-beginner-handoff-ux.py" \
    "$ROOT/tests/beginner-handoff-ux/multi-block/handoff.md" \
    >/tmp/beginner-handoff-ux-multi-block.log 2>&1; then
    echo "beginner handoff UX multi-block negative fixture unexpectedly passed" >&2
    cat /tmp/beginner-handoff-ux-multi-block.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-beginner-handoff-ux.py" \
    "$ROOT/tests/beginner-handoff-ux/hidden-shell/handoff.md" \
    >/tmp/beginner-handoff-ux-hidden-shell.log 2>&1; then
    echo "beginner handoff UX hidden-shell negative fixture unexpectedly passed" >&2
    cat /tmp/beginner-handoff-ux-hidden-shell.log >&2
    return 1
  fi
  rm -f /tmp/beginner-handoff-ux-multi-block.log /tmp/beginner-handoff-ux-hidden-shell.log
  rm -rf "$tmp_dir"
}

run_gpt55_prompt_contract_smoke() {
  python3 "$ROOT/template-repo/scripts/validate-gpt55-prompt-contract.py" "$ROOT"
}

run_project_lifecycle_dashboard_smoke() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  python3 "$ROOT/template-repo/scripts/validate-project-lifecycle-dashboard.py" \
    "$ROOT/template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml"
  python3 "$ROOT/template-repo/scripts/render-project-lifecycle-dashboard.py" \
    --input "$ROOT/template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml" \
    --output "$tmp_dir/project-lifecycle-dashboard.md"
  grep -q "Панель жизненного цикла проекта" "$tmp_dir/project-lifecycle-dashboard.md"
  grep -q "Следующий шаг" "$tmp_dir/project-lifecycle-dashboard.md"

  python3 "$ROOT/template-repo/scripts/validate-project-lifecycle-dashboard.py" \
    "$ROOT/tests/project-lifecycle-dashboard/valid/project-lifecycle-dashboard.yaml"
  if python3 "$ROOT/template-repo/scripts/validate-project-lifecycle-dashboard.py" \
    "$ROOT/tests/project-lifecycle-dashboard/false-green/project-lifecycle-dashboard.yaml" \
    >/tmp/project-lifecycle-dashboard-false-green.log 2>&1; then
    echo "project lifecycle dashboard false-green fixture unexpectedly passed" >&2
    cat /tmp/project-lifecycle-dashboard-false-green.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-project-lifecycle-dashboard.py" \
    "$ROOT/tests/project-lifecycle-dashboard/false-autoswitch/project-lifecycle-dashboard.yaml" \
    >/tmp/project-lifecycle-dashboard-false-autoswitch.log 2>&1; then
    echo "project lifecycle dashboard false-autoswitch fixture unexpectedly passed" >&2
    cat /tmp/project-lifecycle-dashboard-false-autoswitch.log >&2
    return 1
  fi
  if python3 "$ROOT/template-repo/scripts/validate-project-lifecycle-dashboard.py" \
    "$ROOT/tests/project-lifecycle-dashboard/bad-boundary/project-lifecycle-dashboard.yaml" \
    >/tmp/project-lifecycle-dashboard-bad-boundary.log 2>&1; then
    echo "project lifecycle dashboard bad-boundary fixture unexpectedly passed" >&2
    cat /tmp/project-lifecycle-dashboard-bad-boundary.log >&2
    return 1
  fi
  rm -f /tmp/project-lifecycle-dashboard-false-green.log /tmp/project-lifecycle-dashboard-false-autoswitch.log /tmp/project-lifecycle-dashboard-bad-boundary.log
  rm -rf "$tmp_dir"
}

run_curated_pack_quality_smoke() {
  python3 "$ROOT/template-repo/scripts/validate-curated-pack-quality.py" "$ROOT"
  python3 "$ROOT/template-repo/scripts/validate-curated-pack-quality.py" \
    "$ROOT" \
    --manifest "$ROOT/tests/curated-pack-quality/valid/sources-profiles.yaml"
  if python3 "$ROOT/template-repo/scripts/validate-curated-pack-quality.py" \
    "$ROOT" \
    --manifest "$ROOT/tests/curated-pack-quality/missing-routing-doc/sources-profiles.yaml" \
    >/tmp/curated-pack-quality-negative.log 2>&1; then
    echo "curated pack quality negative fixture unexpectedly passed" >&2
    cat /tmp/curated-pack-quality-negative.log >&2
    return 1
  fi
  rm -f /tmp/curated-pack-quality-negative.log
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
  run_step "validate-project-lifecycle-dashboard" python3 "$ROOT/scripts/validate-project-lifecycle-dashboard.py" "$ROOT/.chatgpt/project-lifecycle-dashboard.yaml"
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
  run_step "validate-gpt55-prompt-contract" run_gpt55_prompt_contract_smoke
  run_step "validate-tree-contract" python3 "$ROOT/template-repo/scripts/validate-tree-contract.py" "$ROOT"
  run_step "validate-mode-parity" python3 "$ROOT/template-repo/scripts/validate-mode-parity.py" "$ROOT"
  run_step "validate-brownfield-transition" python3 "$ROOT/template-repo/scripts/validate-brownfield-transition.py" "$ROOT"
  run_step "validate-greenfield-conversion" python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$ROOT"
  run_step "validate-operator-env-starter" python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset starter
  run_step "validate-operator-env-production-example" python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset production --allow-example-placeholders
  run_step "placeholder-app-image-builder-dry-run" python3 "$ROOT/template-repo/scripts/build-placeholder-app-image.py" --env-file "$ROOT/deploy/.env.example" --static-dir "$ROOT/deploy/static-placeholder" --dry-run --install-volume
  run_step "deploy-dry-run-smoke-starter-app-db" run_deploy_dry_run_smoke
  run_step "validate-spec-traceability" python3 "$ROOT/template-repo/scripts/validate-spec-traceability.py" "$ROOT"
  run_step "validate-task-state-lite" python3 "$ROOT/template-repo/scripts/validate-task-state-lite.py" "$ROOT/template-repo/template"
  run_step "task-state-lite-smoke" run_task_state_lite_smoke
  run_step "validate-feature-execution-lite" python3 "$ROOT/template-repo/scripts/validate-feature-execution-lite.py" "$ROOT"
  run_step "validate-learning-patch-loop" python3 "$ROOT/template-repo/scripts/validate-learning-patch-loop.py" "$ROOT"
  run_step "learning-patch-loop-smoke" run_learning_patch_loop_smoke
  run_step "artifact-eval-smoke" run_artifact_eval_smoke
  run_step "downstream-application-proof-smoke" run_downstream_application_proof_smoke
  run_step "codex-orchestration-smoke" run_codex_orchestration_smoke
  run_step "codex-orchestration-runner-negative-smoke" run_codex_orchestration_runner_negative_smoke
  run_step "plan6-productization-smoke" run_plan6_productization_smoke
  run_step "project-lifecycle-dashboard-smoke" run_project_lifecycle_dashboard_smoke
  run_step "curated-pack-quality-smoke" run_curated_pack_quality_smoke
  run_step "validate-verified-sync-fallback-evidence" python3 "$ROOT/template-repo/scripts/validate-verified-sync-fallback-evidence.py" "$ROOT/reports/release/verified-sync-fallback-evidence.md"
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
