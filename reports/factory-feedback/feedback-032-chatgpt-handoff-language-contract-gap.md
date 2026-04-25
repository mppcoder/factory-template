# Factory feedback

## Источник
bug-032-chatgpt-handoff-language-contract-gap

## Краткое описание
Repo rules требовали русский человекочитаемый handoff, но executable validation не проверяла upstream `.chatgpt/codex-input.md`. Из-за этого ChatGPT-generated handoff мог прийти на английском и пройти дальше как нормальный task input.

## Reusable issue
Да.

## Предлагаемое правило
- Любой ChatGPT-generated handoff для `factory-template` должен писать человекочитаемые цели, ограничения, требования, verification и completion sections на русском.
- Английский допустим только как technical literal value.
- `.chatgpt/codex-input.md` и normalized handoff artifacts должны проходить language-contract validator.

## Проверка
- Добавить validator для входящего handoff language contract.
- Подключить validator к `validate-codex-task-pack.py`, чтобы quick verify ловил нарушение.
- Обновить scenario-pack и generated guidance.
