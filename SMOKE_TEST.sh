#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$ROOT/.smoke-test"
PROJECT_SLUG="audit-smoke-project"
PROJECT_DIR="$WORKDIR/$PROJECT_SLUG"
LOG="$WORKDIR/smoke.log"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
: > "$LOG"
log(){ printf '%s\n' "$*" | tee -a "$LOG"; }
run(){ timeout 20s "$@" >>"$LOG" 2>&1; }
run_expect_fail(){ if timeout 20s "$@" >>"$LOG" 2>&1; then return 1; else return 0; fi; }

log '=== 0. Подготовка после распаковки ==='
run bash "$ROOT/POST_UNZIP_SETUP.sh"
run bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"
cat "$LOG"
: > "$LOG"

log '=== 1. Создание проекта ==='
cd "$WORKDIR"
printf 'Тестовый проект\n%s\nproduct-dev\nbrownfield\nfeature\nhybrid\n' "$PROJECT_SLUG" | FACTORY_REGISTRY_MODE=skip bash "$ROOT/launcher.sh" >>"$LOG" 2>&1
cat "$LOG"
: > "$LOG"

log '=== 2. Проверки на свежем проекте ==='
cd "$PROJECT_DIR"
run ./scripts/validate-project-preset.py .
run ./scripts/validate-policy-preset.py .
run ./scripts/validate-change-profile.py .
run ./scripts/validate-task-graph.py .
run ./scripts/validate-stage.py .
run_expect_fail ./scripts/validate-evidence.py . && log 'OK: свежий scaffold корректно не проходит evidence' || { log 'ОШИБКА: свежий scaffold не должен проходить evidence'; exit 1; }
run_expect_fail ./scripts/validate-quality.py . && log 'OK: свежий scaffold корректно не проходит quality' || { log 'ОШИБКА: свежий scaffold не должен проходить quality'; exit 1; }
run_expect_fail ./scripts/check-dod.py . && log 'OK: свежий scaffold корректно не проходит DoD' || { log 'ОШИБКА: свежий scaffold не должен проходить DoD'; exit 1; }
cat "$LOG"
: > "$LOG"

log '=== 3. Наполнение артефактов ==='
run python3 "$ROOT/tools/fill_smoke_artifacts.py"
run ./scripts/init-work-item.py .
run ./scripts/create-codex-task-pack.py .
cat "$LOG"
: > "$LOG"

echo '=== 4. Проверки после наполнения ==='
run ./scripts/validate-project-preset.py .
run ./scripts/validate-policy-preset.py .
run ./scripts/validate-task-graph.py .
run ./scripts/validate-change-profile.py .
run ./scripts/validate-stage.py .
run ./scripts/validate-evidence.py .
run ./scripts/validate-quality.py .
run ./scripts/validate-handoff.py .
run ./scripts/validate-codex-task-pack.py .
run ./scripts/validate-codex-routing.py .
run ./scripts/validate-handoff-response-format.py .chatgpt/handoff-response.md
run ./scripts/check-dod.py .
run ./scripts/export-sources-pack.sh .
cat "$LOG"

echo
echo "Smoke-test завершен успешно."
echo "Лог: $LOG"
echo "Проект: $PROJECT_DIR"
