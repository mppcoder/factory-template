# Tech Spec: Plan 3 Artifact Eval Adoption

> generated_at: 2026-04-27T12:21:06+03:00
> status: approved
> feature_id: plan-3-eval-adoption
> В этом документе описано "как" агент делает решение простыми шагами.

## Кратко о подходе
Сделать P3-S3/P3-S4 через два repo-local слоя: расширить `tests/artifact-eval/specs` и generated reports, затем закрыть это изменение как advanced feature workspace с валидируемым checkpoint и closeout.

## User Intent Binding
Какие `US-*` из user-spec закрывает этот технический план.

- US-001 закрывается новыми specs/reports для direct task self-handoff, closeout ledger, downstream sync boundary, production proof boundary и расширением существующих handoff/feature specs.
- US-002 закрывается workspace `work/features/plan-3-eval-adoption` и последующим closeout в `work/completed`.
- US-003 закрывается явными docs/test boundaries: P3-S5 runtime QA остаётся отдельной стадией.

## Decisions
Лёгкий список решений. Если решение спорное или повлияло на scope, позже перенесите его в `decisions.md`.

- Использовать существующий Artifact Eval Harness вместо нового eval engine.
- Использовать repo-level `work/features`, потому что это factory change, а не template materialization внутри `template-repo/template`.
- Не импортировать внешние AIF runtime/UI механики.

## User-Spec Deviations
Заполняйте только если tech-spec меняет, сужает, расширяет или иначе переосмысливает user-spec. В approved tech-spec не должно оставаться `approval=pending`.

Нет.

## Что меняем
- `tests/artifact-eval/specs/*.yaml`
- `tests/artifact-eval/reports/*.md`
- `template-repo/scripts/verify-all.sh`
- release/state/test docs для P3-S3/P3-S4 evidence
- `work/features/plan-3-eval-adoption` до closeout

## Acceptance Criteria
Технические критерии приемки, которые дополняют пользовательские критерии из user-spec.

- Все Artifact Eval reports проходят `validate-artifact-eval-report.py`.
- Advanced workspace проходит `validate-feature-execution-lite.py --require-advanced`.
- Closed workspace проходит `validate-project-knowledge-update.py`.
- `bash template-repo/scripts/verify-all.sh quick` зелёный.

## Какие артефакты затрагиваем
- Artifact Eval Harness specs/reports.
- Feature Execution Lite workspace/closeout artifacts.
- Release-facing status docs.

## Как проверяем
Команды:

```bash
python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/*.md
python3 template-repo/scripts/validate-feature-execution-lite.py --workspace work/features/plan-3-eval-adoption --require-advanced
python3 template-repo/scripts/validate-project-knowledge-update.py . --workspace work/completed/plan-3-eval-adoption
bash template-repo/scripts/verify-all.sh quick
```

## Audit Wave Lite
Необязательная лёгкая финальная проверка. Для маленькой feature достаточно одного прохода глазами по коду/докам/тестам.

Проверить, что новые eval cases не заявляют production proof, что negative fixtures покрывают overclaim/source hygiene, и что release docs отделяют P3-S3/P3-S4 от P3-S5.

## Final Verification
Последний проход перед handoff/done: что запустить, что показать пользователю, что записать в decisions.

Запустить quick verify, затем `git status --short --branch`; при green и доступном origin сделать commit/push и назвать hash/sync status.

## Ограничения и риски
- Real VPS proof не выполняется и не утверждается.
- P3-S5 остаётся runtime QA boundary / 2.6 prep.
- Root contamination недопустим: generated-project artifacts не добавляются в repo root.
