#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$ROOT/POST_UNZIP_SETUP.sh" >/dev/null 2>&1 || true
FAILS=0
printf '%-42s | %-30s | %-10s | %-10s | %-8s\n' 'Сценарий' 'Проверка' 'Ожидание' 'Факт' 'Статус'
printf '%s\n' '----------------------------------------------------------------------------------------------------------------------------'
record(){ printf '%-42s | %-30s | %-10s | %-10s | %-8s\n' "$1" "$2" "$3" "$4" "$5"; }
assert_pass(){ local s="$1" c="$2"; shift 2; if "$@" >/dev/null 2>&1; then record "$s" "$c" pass pass OK; else record "$s" "$c" pass fail FAIL; FAILS=$((FAILS+1)); fi; }
assert_fail(){ local s="$1" c="$2"; shift 2; if "$@" >/dev/null 2>&1; then record "$s" "$c" fail pass FAIL; FAILS=$((FAILS+1)); else record "$s" "$c" fail fail OK; fi; }
assert_pass 'factory-template' validate-factory-template-ops.sh bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"
make_project(){
  local workdir="$1" pname="$2" slug="$3" preset="$4" mode="$5" cls="$6" execm="$7" reg="${8:-skip}"
  rm -rf "$workdir"; mkdir -p "$workdir"
  local drive_url="https://drive.google.com/drive/folders/${slug}-folder?usp=drive_link"
  (cd "$workdir" && printf '%s\n%s\n%s\n%s\n%s\n%s\n%s\n' "$pname" "$slug" "$preset" "$mode" "$cls" "$execm" "$drive_url" | FACTORY_REGISTRY_MODE="$reg" timeout 60s bash "$ROOT/launcher.sh" >/dev/null)
}
SBASE="$ROOT/.matrix-test"; rm -rf "$SBASE"; mkdir -p "$SBASE"
POSITIVE_COMMON=(validate-project-preset.sh validate-policy-preset.sh validate-change-profile.sh validate-task-graph.sh validate-stage.sh validate-versioning-layer.sh validate-defect-capture.sh validate-alignment.sh validate-google-drive-sources.sh)

make_project "$SBASE/green-small-fix" 'Матрица greenfield small-fix' 'green-small-fix' product-dev greenfield small-fix manual
P="$SBASE/green-small-fix/green-small-fix"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'greenfield+small-fix+manual' "$c" "$P/scripts/$c" "$P"; done
for c in validate-evidence.sh validate-quality.sh check-dod.sh; do assert_fail 'greenfield+small-fix+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'greenfield+small-fix+manual' validate-handoff.sh "$P/scripts/validate-handoff.sh" "$P"

make_project "$SBASE/green-feature" 'Матрица greenfield feature' 'green-feature' product-dev greenfield feature hybrid
P="$SBASE/green-feature/green-feature"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'greenfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done
for c in validate-evidence.sh validate-quality.sh check-dod.sh validate-handoff.sh; do assert_fail 'greenfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done

make_project "$SBASE/brown-feature" 'Матрица brownfield feature' 'brown-feature' legacy-modernization brownfield feature hybrid
P="$SBASE/brown-feature/brown-feature"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'brownfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done
for c in validate-evidence.sh validate-quality.sh check-dod.sh validate-handoff.sh; do assert_fail 'brownfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done

make_project "$SBASE/brown-audit" 'Матрица brownfield audit' 'brown-audit' audit-only brownfield brownfield-audit manual
P="$SBASE/brown-audit/brown-audit"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'brownfield+audit+manual' "$c" "$P/scripts/$c" "$P"; done
for c in validate-evidence.sh validate-quality.sh check-dod.sh; do assert_fail 'brownfield+audit+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'brownfield+audit+manual' validate-handoff.sh "$P/scripts/validate-handoff.sh" "$P"

for ex in example-change-small-fix example-change-brownfield-audit example-change-end-to-end; do
  P="$ROOT/working-project-examples/$ex"
  for c in validate-project-preset.sh validate-policy-preset.sh validate-change-profile.sh validate-task-graph.sh validate-stage.sh validate-evidence.sh validate-quality.sh validate-handoff.sh check-dod.sh validate-versioning-layer.sh validate-defect-capture.sh validate-alignment.sh; do
    assert_pass "$ex" "$c" "$ROOT/template-repo/scripts/$c" "$P"
  done
done

make_project "$SBASE/bugflow" 'Factory bugflow' 'factory-bugflow' product-dev brownfield feature hybrid
P="$SBASE/bugflow/factory-bugflow"
python3 "$ROOT/tools/fill_smoke_artifacts.py" "$P" >/dev/null 2>&1 || (
  cd "$P" && python3 "$ROOT/tools/fill_smoke_artifacts.py" >/dev/null
)
cp "$P/meta-feedback/factory-bug-report.md" "$P/.chatgpt/factory-bug-report.md"
python3 - <<PYCODE >/dev/null
from pathlib import Path
p=Path(r"$P/.chatgpt/factory-bug-report.md")
t=p.read_text(encoding='utf-8')
for a,b in {
'<!-- Укажите, где именно найден дефект -->':'Слой controlled back-sync',
'<!-- Укажите, в каком working project найден баг -->':'factory-bugflow',
'<!-- Опишите, в каком сценарии или шаге возникла ошибка -->':'Этап подготовки patch bundle',
'<!-- Опишите ожидаемое поведение -->':'Ожидалось получить patch bundle по safe-зонам',
'<!-- Опишите фактическое поведение -->':'Потребовалась ручная проверка patch summary',
}.items():
    t=t.replace(a,b)
p.write_text(t, encoding='utf-8')
PYCODE
assert_pass 'factory-bugflow' detect-factory-issues.py python3 "$ROOT/workspace-packs/factory-ops/detect-factory-issues.py" "$P"
assert_pass 'factory-bugflow' check-template-drift.py python3 "$ROOT/workspace-packs/factory-ops/check-template-drift.py" "$ROOT" "$P"
assert_pass 'factory-bugflow' create-codex-task-pack.sh "$ROOT/template-repo/scripts/create-codex-task-pack.sh" "$P"
assert_pass 'factory-bugflow' validate-codex-task-pack.sh "$ROOT/template-repo/scripts/validate-codex-task-pack.sh" "$P"
assert_pass 'factory-bugflow' validate-handoff-response-format.sh "$ROOT/template-repo/scripts/validate-handoff-response-format.sh" "$P/.chatgpt/handoff-response.md"
assert_pass 'factory-bugflow' boundary-actions.md test -f "$P/.chatgpt/boundary-actions.md"
assert_pass 'factory-bugflow' validate-defect-capture.sh "$ROOT/template-repo/scripts/validate-defect-capture.sh" "$P"
assert_pass 'factory-bugflow' validate-alignment.sh "$ROOT/template-repo/scripts/validate-alignment.sh" "$P"
assert_fail 'factory-bugflow' validate-factory-feedback.sh bash "$ROOT/VALIDATE_FACTORY_FEEDBACK.sh" "$P"
python3 - <<PYCODE >/dev/null
from pathlib import Path
root = Path(r"$P") / "meta-feedback"
task = (root / "factory-task.md").read_text(encoding="utf-8")
for old, new in {
    "<!-- Почему фабрику нужно доработать -->": "Codex task pack должен фиксированно включать boundary-actions.md в handoff-артефакты.",
    "<!-- Из какого проекта или цикла пришел feedback -->": "Матрица проверки factory-bugflow в factory-template.",
    "<!-- Опишите требуемое изменение -->": "Нужно валидировать и воспроизводимо собирать feedback loop через self-tests.",
    "<!-- Перечислите основные файлы -->": "template-repo/scripts/create-codex-task-pack.sh, MATRIX_TEST.sh, tools/ingest_factory_feedback.py",
    "<!-- Как понять, что доработка завершена -->": "VALIDATE_FACTORY_FEEDBACK.sh проходит, ingest не падает, matrix green.",
    "<!-- Да / нет / определить позже -->": "Нет",
}.items():
    task = task.replace(old, new)
(root / "factory-task.md").write_text(task, encoding="utf-8")
bug = (root / "factory-bug-report.md").read_text(encoding="utf-8")
for old, new in {
    "<!-- Укажите проект, пример, сценарий или шаг -->": "Factory matrix bugflow scenario.",
    "<!-- Укажите рабочий проект -->": "factory-bugflow",
    "<!-- Укажите сценарий, validator, launcher или другой шаг -->": "Feedback ingestion and meta-feedback validation.",
    "<!-- Опишите ожидаемое поведение фабрики -->": "Ingest script должен корректно валидировать feedback и не падать на runtime error.",
    "<!-- Опишите фактическое поведение -->": "Сырой feedback должен блокироваться validator до ingest.",
    "<!-- Если обход найден, кратко опишите его -->": "Временно запускать validator отдельно и не делать ingest с --allow-incomplete без ручной оценки.",
    "<!-- Кратко сформулируйте желаемое исправление -->": "Сделать ingest устойчивым и покрыть feedback loop тестом.",
    "<!-- Перечислите предполагаемые файлы -->": "tools/ingest_factory_feedback.py, tools/validate_factory_feedback.py, MATRIX_TEST.sh",
}.items():
    bug = bug.replace(old, new)
(root / "factory-bug-report.md").write_text(bug, encoding="utf-8")
PYCODE
assert_pass 'factory-bugflow' validate-factory-feedback.sh bash "$ROOT/VALIDATE_FACTORY_FEEDBACK.sh" "$P"
assert_pass 'factory-bugflow' ingest-factory-feedback.sh bash "$ROOT/INGEST_FACTORY_FEEDBACK.sh" "$P" --dry-run
assert_pass 'factory-bugflow' export-template-patch.sh "$ROOT/workspace-packs/factory-ops/export-template-patch.sh" "$ROOT" "$P" --dry-run
assert_pass 'factory-bugflow' 'apply-template-patch.sh --check' "$ROOT/workspace-packs/factory-ops/apply-template-patch.sh" "$P/_factory-sync-export" --check
assert_pass 'factory-bugflow' 'apply-template-patch.sh --apply-safe-zones' "$ROOT/workspace-packs/factory-ops/apply-template-patch.sh" "$P/_factory-sync-export" --apply-safe-zones

printf '%s\n' '----------------------------------------------------------------------------------------------------------------------------'
if [ "$FAILS" -gt 0 ]; then echo "MATRIX TEST НЕ ПРОЙДЕН: fail=$FAILS"; exit 1; fi
echo 'MATRIX TEST ПРОЙДЕН'
