# Factory feedback: GPT-5.5 prompt contract drift

Дата: 2026-04-28
Source bug: `reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md`
Статус: applied

## Feedback

Фабрика должна иметь durable prompt-contract gate для model prompt migrations. Иначе stale task handoff и process-first legacy prompt style могут пройти через `.chatgpt` и generated task packs без автоматического сигнала.

## Factory-level change

- Добавить validator для GPT-5.5 prompt contract.
- Подключить validator к `verify-all.sh`.
- Добавить artifact eval spec, чтобы проверялся сам validator.
- Держать `quick` profile на `gpt-5.4-mini` как осознанный routing policy, без silent promotion.

## Acceptance

- Fresh baseline закреплен в template `.chatgpt` и generators.
- Old prompt-pattern drift ловится проверкой.
- Reports фиксируют official OpenAI source map и gap map.
