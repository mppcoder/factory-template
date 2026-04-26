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
assert_pass 'factory-template' validate-factory-template-ops.py bash "$ROOT/VALIDATE_FACTORY_TEMPLATE_OPS.sh"
assert_pass 'operator-preset-starter' validate-operator-env.py python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset starter
assert_pass 'operator-preset-production-example' validate-operator-env.py python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset production --allow-example-placeholders
assert_fail 'operator-preset-production-strict' validate-operator-env.py python3 "$ROOT/template-repo/scripts/validate-operator-env.py" "$ROOT" --env-file "$ROOT/deploy/.env.example" --preset production
make_project(){
  local workdir="$1" pname="$2" slug="$3" preset="$4" mode="$5" cls="$6" execm="$7" reg="${8:-skip}"
  rm -rf "$workdir"; mkdir -p "$workdir"
  (cd "$workdir" && printf '%s\n%s\n%s\n%s\n%s\n%s\n' "$pname" "$slug" "$preset" "$mode" "$cls" "$execm" | FACTORY_REGISTRY_MODE="$reg" timeout 60s bash "$ROOT/launcher.sh" >/dev/null)
}
convert_project_to_greenfield(){
  local project_root="$1"
  python3 - "$project_root" <<'PYCODE'
from pathlib import Path
import sys
import yaml

root = Path(sys.argv[1])
profile_path = root / ".chatgpt/project-profile.yaml"
stage_path = root / ".chatgpt/stage-state.yaml"
profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
profile["project_preset"] = "greenfield-product"
profile["recommended_mode"] = "greenfield"
profile["lifecycle_state"] = "greenfield-converted"
profile["target_project_preset"] = "greenfield-product"
profile["target_lifecycle_state"] = "greenfield-converted"
profile["conversion_required"] = False
profile_path.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8")
stage = yaml.safe_load(stage_path.read_text(encoding="utf-8")) or {}
stage.setdefault("project", {})["mode"] = "greenfield"
stage.setdefault("lifecycle", {})
stage["lifecycle"]["previous_lifecycle_state"] = stage["lifecycle"].get("lifecycle_state") or "brownfield-with-repo-adoption"
stage["lifecycle"]["lifecycle_state"] = "greenfield-converted"
stage["lifecycle"]["target_lifecycle_state"] = "greenfield-converted"
stage["lifecycle"]["conversion_required"] = False
stage["lifecycle"]["conversion_gate_status"] = "passed"
stage_path.write_text(yaml.safe_dump(stage, allow_unicode=True, sort_keys=False), encoding="utf-8")
PYCODE
}
SBASE="$ROOT/.matrix-test"; rm -rf "$SBASE"; mkdir -p "$SBASE"
POSITIVE_COMMON=(validate-project-preset.py validate-policy-preset.py validate-change-profile.py validate-task-graph.py validate-stage.py validate-versioning-layer.py validate-defect-capture.py validate-alignment.py)

assert_pass 'factory-template' 'project-core+producer-layer' python3 "$ROOT/template-repo/scripts/validate-tree-contract.py" "$ROOT"
assert_pass 'factory-template' 'greenfield-conversion-contract' python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$ROOT"

make_project "$SBASE/green-small-fix" 'Матрица greenfield small-fix' 'green-small-fix' greenfield-product greenfield small-fix manual
P="$SBASE/green-small-fix/green-small-fix"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'greenfield+small-fix+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'greenfield+small-fix+manual' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
assert_pass 'greenfield+small-fix+manual' validate-greenfield-conversion.py python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$P"
for c in validate-evidence.py validate-quality.py check-dod.py; do assert_fail 'greenfield+small-fix+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'greenfield+small-fix+manual' validate-handoff.py "$P/scripts/validate-handoff.py" "$P"

make_project "$SBASE/green-feature" 'Матрица greenfield feature' 'green-feature' greenfield-product greenfield feature hybrid
P="$SBASE/green-feature/green-feature"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'greenfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'greenfield+feature+hybrid' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
for c in validate-evidence.py validate-quality.py check-dod.py validate-handoff.py; do assert_fail 'greenfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done

make_project "$SBASE/brown-feature" 'Матрица brownfield feature' 'brown-feature' brownfield-with-repo-modernization brownfield feature hybrid
P="$SBASE/brown-feature/brown-feature"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'brownfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'brownfield+feature+hybrid' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
assert_pass 'brownfield+feature+hybrid' validate-brownfield-transition.py python3 "$ROOT/template-repo/scripts/validate-brownfield-transition.py" "$P" --with-repo
for c in validate-evidence.py validate-quality.py check-dod.py validate-handoff.py; do assert_fail 'brownfield+feature+hybrid' "$c" "$P/scripts/$c" "$P"; done
convert_project_to_greenfield "$P"
assert_pass 'brownfield+feature+converted' validate-greenfield-conversion.py python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$P" --require-converted

make_project "$SBASE/brown-no-repo" 'Матрица brownfield no repo' 'brown-no-repo' brownfield-without-repo brownfield brownfield-stabilization hybrid
P="$SBASE/brown-no-repo/brown-no-repo"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'brownfield+without-repo+hybrid' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'brownfield+without-repo+hybrid' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
assert_pass 'brownfield+without-repo+hybrid' validate-brownfield-transition.py python3 "$ROOT/template-repo/scripts/validate-brownfield-transition.py" "$P" --without-repo
assert_pass 'brownfield+without-repo+conversion-ready' conversion-target python3 "$ROOT/template-repo/scripts/validate-brownfield-transition.py" "$P" --without-repo
convert_project_to_greenfield "$P"
assert_pass 'brownfield+without-repo+converted' validate-greenfield-conversion.py python3 "$ROOT/template-repo/scripts/validate-greenfield-conversion.py" "$P" --require-converted

make_project "$SBASE/brown-audit" 'Матрица brownfield audit' 'brown-audit' brownfield-with-repo-audit brownfield brownfield-audit manual
P="$SBASE/brown-audit/brown-audit"
for c in "${POSITIVE_COMMON[@]}"; do assert_pass 'brownfield+audit+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'brownfield+audit+manual' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
for c in validate-evidence.py validate-quality.py check-dod.py; do assert_fail 'brownfield+audit+manual' "$c" "$P/scripts/$c" "$P"; done
assert_pass 'brownfield+audit+manual' validate-handoff.py "$P/scripts/validate-handoff.py" "$P"

for ex in example-change-small-fix example-change-brownfield-audit example-change-end-to-end; do
  P="$ROOT/factory/producer/reference/examples/$ex"
  for c in validate-project-preset.py validate-policy-preset.py validate-change-profile.py validate-task-graph.py validate-stage.py validate-evidence.py validate-quality.py validate-handoff.py check-dod.py validate-versioning-layer.py validate-defect-capture.py validate-alignment.py; do
    assert_pass "$ex" "$c" "$ROOT/template-repo/scripts/$c" "$P"
  done
done

make_project "$SBASE/bugflow" 'Factory bugflow' 'factory-bugflow' greenfield-product brownfield feature hybrid
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
assert_pass 'factory-bugflow' detect-factory-issues.py python3 "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/detect-factory-issues.py" "$P"
assert_pass 'factory-bugflow' check-template-drift.py python3 "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/check-template-drift.py" "$ROOT" "$P"
assert_pass 'factory-bugflow' create-codex-task-pack.py "$ROOT/template-repo/scripts/create-codex-task-pack.py" "$P"
assert_pass 'factory-bugflow' validate-codex-task-pack.py "$ROOT/template-repo/scripts/validate-codex-task-pack.py" "$P"
assert_pass 'factory-bugflow' validate-codex-routing.py "$ROOT/template-repo/scripts/validate-codex-routing.py" "$P"
assert_pass 'factory-bugflow' validate-tree-contract.py "$ROOT/template-repo/scripts/validate-tree-contract.py" "$P"
assert_pass 'factory-bugflow' validate-handoff-response-format.py "$ROOT/template-repo/scripts/validate-handoff-response-format.py" "$P/.chatgpt/handoff-response.md"
assert_pass 'factory-bugflow' validate-handoff-language.py "$ROOT/template-repo/scripts/validate-handoff-language.py" "$P/.chatgpt/handoff-response.md"
assert_fail 'factory-bugflow' 'reject-english-handoff-labels' bash -lc "printf '%s\n' '## Handoff в Codex' 'Repo: demo' 'Goal: do work' | '$ROOT/template-repo/scripts/validate-handoff-language.py' -"
assert_pass 'factory-bugflow' boundary-actions.md test -f "$P/.chatgpt/boundary-actions.md"
assert_pass 'factory-bugflow' validate-defect-capture.py "$ROOT/template-repo/scripts/validate-defect-capture.py" "$P"
assert_pass 'factory-bugflow' validate-alignment.py "$ROOT/template-repo/scripts/validate-alignment.py" "$P"
assert_fail 'factory-bugflow' validate-factory-feedback.py bash "$ROOT/VALIDATE_FACTORY_FEEDBACK.sh" "$P"
python3 - <<PYCODE >/dev/null
from pathlib import Path
root = Path(r"$P") / "meta-feedback"
task = (root / "factory-task.md").read_text(encoding="utf-8")
for old, new in {
    "<!-- Почему фабрику нужно доработать -->": "Codex task pack должен фиксированно включать boundary-actions.md в handoff-артефакты.",
    "<!-- Из какого проекта или цикла пришел feedback -->": "Матрица проверки factory-bugflow в factory-template.",
    "<!-- Опишите требуемое изменение -->": "Нужно валидировать и воспроизводимо собирать feedback loop через self-tests.",
    "<!-- Перечислите основные файлы -->": "template-repo/scripts/create-codex-task-pack.py, MATRIX_TEST.sh, tools/ingest_factory_feedback.py",
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
assert_pass 'factory-bugflow' validate-factory-feedback.py bash "$ROOT/VALIDATE_FACTORY_FEEDBACK.sh" "$P"
assert_pass 'factory-bugflow' ingest-factory-feedback.sh bash "$ROOT/INGEST_FACTORY_FEEDBACK.sh" "$P" --dry-run
printf '\nMATRIX_SAFE_ZONE_EXAMPLE_DRIFT\n' >> "$P/.chatgpt/examples/done-report.example.md"
printf '\nMATRIX_SAFE_ZONE_TASK_BLOCK_DRIFT\n' >> "$P/tasks/codex/codex-task-mandatory-bug-capture.block.md"
printf '\nMATRIX_SAFE_WORK_TEMPLATE_DRIFT\n' >> "$P/work-templates/user-spec.md.template"
printf '\nMATRIX_ADVISORY_PROJECT_KNOWLEDGE_DRIFT\n' >> "$P/project-knowledge/project.md"
printf '\nMATRIX_MANUAL_PROJECT_WORK_DRIFT\n' >> "$P/work/_task-template.md"
assert_pass 'factory-bugflow' export-template-patch.sh "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh" "$ROOT" "$P" --dry-run
assert_pass 'factory-bugflow' 'tiered-preview-v3-multizone' python3 - <<PYCODE
import json
from pathlib import Path
bundle = Path(r"$P/_factory-sync-export")
metadata = json.loads((bundle / "bundle-metadata.json").read_text(encoding="utf-8"))
preview = json.loads((bundle / "preview-changes.json").read_text(encoding="utf-8"))
generated = sorted(
    path.relative_to(bundle / "generated-files").as_posix()
    for path in (bundle / "generated-files").rglob("*")
    if path.is_file()
)
assert metadata["sync_contract_version"] == 3
assert set(metadata["tiers"]) >= {"safe-generated", "safe-clone", "advisory-review", "manual-project-owned"}
assert metadata["tiers"]["safe-generated"]["generated"] >= 3
assert metadata["tiers"]["advisory-review"]["total"] >= 1
assert metadata["tiers"]["manual-project-owned"]["total"] >= 1
assert len(generated) >= 3
assert any(item["tier"] == "safe-generated" and item["will_generate"] for item in preview)
assert all(not item.get("will_generate") for item in preview if item["tier"] not in {"safe-generated", "safe-clone"})
assert not any(path.startswith("project-knowledge/") for path in generated)
assert not any(path.startswith("work/") for path in generated)
PYCODE
assert_pass 'factory-bugflow' 'apply-template-patch.sh --check' "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh" "$P/_factory-sync-export" --check
assert_pass 'factory-bugflow' 'apply-template-patch.sh --apply-safe-zones --with-project-snapshot' "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh" "$P/_factory-sync-export" --apply-safe-zones --with-project-snapshot
printf '\nMATRIX_MANUAL_CHANGE_MARKER\n' >> "$P/README.md"
assert_pass 'factory-bugflow' upgrade-report.py python3 "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py" "$ROOT" "$P" --format text
assert_pass 'factory-bugflow' 'upgrade-report.py russian-markdown' python3 "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py" "$ROOT" "$P" --format markdown --output "$P/_factory-sync-export/matrix-upgrade-summary.md"
assert_pass 'factory-bugflow' 'upgrade-report-russian-body' python3 - "$P/_factory-sync-export/matrix-upgrade-summary.md" <<'PYCODE'
import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding="utf-8")
for forbidden in [
    "Generated (UTC)",
    "Factory root",
    "Downstream project root",
    "Template version",
    "Sync contract version",
    "Verdict",
    "Safe apply materializes",
    " from `",
    "status=`",
    "reason:",
    "operator action:",
    "Rollback metadata is mandatory",
    "Prepare/refresh bundle",
    "Review bundle before apply",
    "Apply safe zones",
    "Inspect rollback state",
    "Roll back safe-zone",
    "`--dry-run` and `--check` are read-only",
    "ChatGPT Project Sources refresh is not part",
]:
    assert forbidden not in text, forbidden
PYCODE
assert_pass 'factory-bugflow' 'rollback-template-patch.sh --check' "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh" "$P/_factory-sync-export" --check
assert_pass 'factory-bugflow' 'rollback-template-patch.sh --rollback --restore-project-snapshot' "$ROOT/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh" "$P/_factory-sync-export" --rollback --restore-project-snapshot
assert_fail 'factory-bugflow' 'manual-marker-after-rollback' grep -q 'MATRIX_MANUAL_CHANGE_MARKER' "$P/README.md"
assert_pass 'factory-bugflow' 'project-work-restored-after-rollback' grep -q 'MATRIX_MANUAL_PROJECT_WORK_DRIFT' "$P/work/_task-template.md"
assert_pass 'routing-quick' resolve-codex-task-route.py bash -lc "python3 '$ROOT/template-repo/scripts/resolve-codex-task-route.py' '$P' --launch-source chatgpt-handoff --task-text 'docs triage search in repo' | grep -q 'selected_profile=quick'"
assert_pass 'routing-build' resolve-codex-task-route.py bash -lc "python3 '$ROOT/template-repo/scripts/resolve-codex-task-route.py' '$P' --launch-source chatgpt-handoff --task-text 'fix feature remediation in launcher' | grep -q 'selected_profile=build'"
assert_pass 'routing-deep' resolve-codex-task-route.py bash -lc "python3 '$ROOT/template-repo/scripts/resolve-codex-task-route.py' '$P' --launch-source chatgpt-handoff --task-text 'root cause audit architecture inconsistency' | grep -q 'selected_profile=deep'"
assert_pass 'routing-review' resolve-codex-task-route.py bash -lc "python3 '$ROOT/template-repo/scripts/resolve-codex-task-route.py' '$P' --launch-source chatgpt-handoff --task-text 'review tests cleanup verification' | grep -q 'selected_profile=review'"
assert_pass 'direct-task-bootstrap' bootstrap-codex-task.py python3 "$ROOT/template-repo/scripts/bootstrap-codex-task.py" "$P" --launch-source direct-task --task-text "bug regression root cause review the failure"
assert_pass 'direct-task-routing' validate-codex-routing.py "$ROOT/template-repo/scripts/validate-codex-routing.py" "$P"

printf '%s\n' '----------------------------------------------------------------------------------------------------------------------------'
if [ "$FAILS" -gt 0 ]; then echo "MATRIX TEST НЕ ПРОЙДЕН: fail=$FAILS"; exit 1; fi
echo 'MATRIX TEST ПРОЙДЕН'
