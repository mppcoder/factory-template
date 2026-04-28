# Отчет о проверке результата

## Что проверяли

- Canonical VPS layout rule для `/projects`.
- Запрет intermediate repos как sibling project roots.
- Наличие machine-readable `workspace_layout_policy`.
- Validator/eval coverage для drift этого правила.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-2026-04-28-flat-project-tree-intermediate-repo-gap.md`.
- Слой: `factory-template`.
- Статус remediation: fixed-in-current-scope.

## Что подтверждено

- Active docs и scenario-pack теперь требуют размещать temporary/intermediate/reconstructed/helper repos внутри repo целевого `greenfield-product`.
- `template-repo/tree-contract.yaml` содержит `workspace_layout_policy`.
- `template-repo/scripts/validate-tree-contract.py` проверяет правило в active source paths.
- Artifact Eval `project-root-boundary` создан и включен в `verify-all.sh`.

## Команды проверки

- `python3 template-repo/scripts/validate-tree-contract.py .`: PASS.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/project-root-boundary.yaml --output tests/artifact-eval/reports/project-root-boundary.md`: PASS.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/project-root-boundary.md`: PASS.
- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.
- `python3 template-repo/scripts/validate-codex-routing.py .`: PASS.
- `python3 template-repo/scripts/validate-gpt55-prompt-contract.py .`: PASS.
- `bash template-repo/scripts/verify-all.sh quick`: PASS, `VERIFY-ALL ПРОЙДЕН (quick)`.

## Итоговый вывод

Project-root boundary закреплен в docs, machine-readable contract и Artifact Eval. Quick verify прошел; sync status фиксируется через verified sync.
