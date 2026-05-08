# Итоговый отчёт по закрытию изменения

## Что было запрошено

- Обновить Codex CLI до доступной линии `0.129.0`.
- Перевести `factory-template` на goal-first contract.
- Использовать experimental `goals` как рабочий runtime candidate по явному указанию пользователя.

## Что реально сделано

- `@openai/codex` обновлен глобально до `0.129.0`; `codex --version` показывает `codex-cli 0.129.0`.
- Router получил goal-first normalization gate.
- Добавлен `template-repo/scenario-pack/03-goal-first-intake.md`.
- Handoff, closeout, routing, docs and templates обновлены под `goal_contract`.
- Добавлены `goal-contract.yaml.template`, `goal-state.yaml.template`, active `.chatgpt/goal-contract.yaml` and `.chatgpt/goal-state.yaml`.
- Добавлен валидатор `validate-goal-contract.py` и fixtures для valid/vague/proxy/live-validation/broad/budget cases.
- Generated/core parity artifacts обновлены для downstream template sync.

## Статус цели

- achieved

## Evidence относительно DoD

- `bash template-repo/scripts/verify-all.sh quick`: PASS.
- Targeted goal-contract/routing/handoff/mode/tree/language validators: PASS.

## Guard от proxy signals

- Goal закрыт по evidence vs DoD; proxy-only signals explicitly denied.

## Какие артефакты обновлены

- `AGENTS.md`
- `.chatgpt/goal-contract.yaml`
- `.chatgpt/goal-state.yaml`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `template-repo/AGENTS.md`
- `template-repo/codex-routing.yaml`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/03-goal-first-intake.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/template/.chatgpt/*goal*`
- `template-repo/scripts/validate-goal-contract.py`
- `tests/goal-contract/*`
- operator docs and routing validators

## Что осталось вне объёма

- Включение `/goal` внутри уже открытой Codex session не заявлялось и не выполнялось как auto-switch.
- Production/destructive/secrets runtime не входил в scope.

## Итог закрытия

- Goal-first transition выполнен и проверен.
