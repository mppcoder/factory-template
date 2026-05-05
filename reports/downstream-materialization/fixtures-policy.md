# Fixtures policy Universal Task Control / правила downstream projects

## Решение

`tests/universal-task-control/*` остаются factory-only fixtures и не копируются в generated downstream projects по умолчанию.

## Причины

- Negative fixtures специально содержат невалидные registry/handoff/issue examples; в generated project они выглядят как шум и могут быть приняты за пользовательскую очередь.
- Generated project должен получить runnable capability, а не factory test harness.
- Downstream smoke должен работать на temporary generated project и temporary task state, без мутации canonical factory state и без постоянного добавления test fixtures в user repo.
- Existing downstream projects могут иметь собственные задачи и evidence; тестовые fixture files не должны смешиваться с пользовательским lifecycle.

## Что materializes downstream

- `.chatgpt/task-registry.yaml`
- `scripts/*` для Universal Task Control
- `.github/ISSUE_TEMPLATE/*.yml`
- `docs/operator/universal-task-control.md`
- report target dirs: `reports/handoffs/`, `reports/release/`, `reports/bugs/`, `reports/factory-feedback/`

## Что остается factory-only

- `tests/universal-task-control/positive/*`
- `tests/universal-task-control/negative/*`
- factory release/readout reports under `reports/universal-task-control-*.md`
- factory smoke reports that reference canonical template paths

## Verification policy / правила проверки

Factory `verify-all quick` must continue to run positive and negative fixtures. Generated-project quick smoke must create a temporary project and exercise the root layout with `.chatgpt/task-registry.yaml`, not copy fixture trees into every generated repo.
