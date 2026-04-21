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
printf 'Тестовый проект\n%s\nproduct-dev\nbrownfield\nfeature\nhybrid\nhttps://drive.google.com/drive/folders/smoke-test-project-folder?usp=drive_link\n' "$PROJECT_SLUG" | FACTORY_REGISTRY_MODE=skip bash "$ROOT/launcher.sh" >>"$LOG" 2>&1
cat "$LOG"
: > "$LOG"

log '=== 2. Проверки на свежем проекте ==='
cd "$PROJECT_DIR"
run ./scripts/validate-project-preset.sh .
run ./scripts/validate-policy-preset.sh .
run ./scripts/validate-change-profile.sh .
run ./scripts/validate-task-graph.sh .
run ./scripts/validate-stage.sh .
run ./scripts/validate-google-drive-sources.sh .
run_expect_fail ./scripts/validate-evidence.sh . && log 'OK: свежий scaffold корректно не проходит evidence' || { log 'ОШИБКА: свежий scaffold не должен проходить evidence'; exit 1; }
run_expect_fail ./scripts/validate-quality.sh . && log 'OK: свежий scaffold корректно не проходит quality' || { log 'ОШИБКА: свежий scaffold не должен проходить quality'; exit 1; }
run_expect_fail ./scripts/check-dod.sh . && log 'OK: свежий scaffold корректно не проходит DoD' || { log 'ОШИБКА: свежий scaffold не должен проходить DoD'; exit 1; }
cat "$LOG"
: > "$LOG"

log '=== 3. Наполнение артефактов ==='
run python3 "$ROOT/tools/fill_smoke_artifacts.py"
run ./scripts/init-work-item.sh .
cat "$LOG"
: > "$LOG"

echo '=== 4. Проверки после наполнения ==='
run ./scripts/validate-project-preset.sh .
run ./scripts/validate-policy-preset.sh .
run ./scripts/validate-task-graph.sh .
run ./scripts/validate-change-profile.sh .
run ./scripts/validate-stage.sh .
run ./scripts/validate-google-drive-sources.sh .
run ./scripts/validate-evidence.sh .
run ./scripts/validate-quality.sh .
run ./scripts/validate-handoff.sh .
run ./scripts/validate-handoff-response-format.sh .chatgpt/handoff-response.md
run ./scripts/check-dod.sh .
run ./scripts/export-sources-pack.sh .
cat "$LOG"

echo
echo "Smoke-test завершен успешно."
echo "Лог: $LOG"
echo "Проект: $PROJECT_DIR"
