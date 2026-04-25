# Отчет о завершении

## Что было запрошено
- Исправить upstream handoff language gap: ChatGPT-generated handoff не должен приходить с англоязычными человекочитаемыми разделами.
- Сначала пройти defect-capture path, затем remediation.

## Что реально сделано
- Создан `reports/bugs/bug-032-chatgpt-handoff-language-contract-gap.md`.
- Создан `reports/factory-feedback/feedback-032-chatgpt-handoff-language-contract-gap.md`.
- `scenario-pack/15-handoff-to-codex.md` теперь явно распространяет русский language contract на upstream ChatGPT-generated handoff в `.chatgpt/codex-input.md`.
- Добавлен validator `template-repo/scripts/validate-handoff-language.py`.
- `validate-codex-task-pack.py` теперь запускает language validator для `.chatgpt/codex-input.md` и `.chatgpt/normalized-codex-handoff.md`.
- `validate-handoff-response-format.py` дополнительно ловит англоязычные handoff sections вроде `Goal`, `Hard constraints`, `Required implementation`, `Verification commands`, `Completion requirements`.
- `create-codex-task-pack.py` и template task-pack guidance обновлены правилом: upstream handoff prose должен быть русским.

## Какие артефакты обновлены
- `.chatgpt/boundary-actions.md`
- `.chatgpt/codex-input.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/normalized-codex-handoff.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `README.md`
- `template-repo/README.md`
- `template-repo/codex-routing.yaml`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `template-repo/scripts/validate-handoff-language.py`
- `template-repo/scripts/validate-handoff-response-format.py`
- `template-repo/template/.chatgpt/codex-task-pack.md`
- `reports/model-routing/model-routing-proposal.md`
- `reports/bugs/bug-032-chatgpt-handoff-language-contract-gap.md`
- `reports/factory-feedback/feedback-032-chatgpt-handoff-language-contract-gap.md`

## Что не потребовалось
- Новый handoff обратно в ChatGPT не требуется.
- Обновление repo-first инструкции `factory-template ChatGPT Project` не требуется: repo/path/entrypoint/instruction contract не менялись.

## Итог закрытия
- `bug-032` исправлен в текущем scope.
- Upstream ChatGPT-generated handoff теперь имеет executable language-contract check в repo validators.
