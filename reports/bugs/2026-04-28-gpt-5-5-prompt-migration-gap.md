# Bug report: GPT-5.5 prompt migration gap

Дата: 2026-04-28
Слой: `factory-template`
Статус: remediated in current scope

## Summary

Prompt-like слой фабрики не имел отдельного проверяемого GPT-5.5 prompt contract. Из-за этого:
- `.chatgpt/codex-input.md` мог оставаться stale handoff от прошлой задачи;
- generators могли продолжать собирать task-pack без outcome-first baseline;
- artifact eval не ловил drift старых prompt patterns.

## Evidence

- До remediation `.chatgpt/codex-input.md` содержал `CODEX HANDOFF — DOWNSTREAM MULTI-CYCLE SYNC PROOF`.
- `template-repo/scripts/create-codex-task-pack.py` генерировал routing/handoff pack без отдельного `GPT-5.5 prompt baseline`.
- `tests/artifact-eval/specs/` не содержал spec для GPT-5.5 prompt contract.

## Reproduction

1. Открыть `.chatgpt/codex-input.md`.
2. Проверить title и route fields.
3. Открыть `template-repo/scripts/create-codex-task-pack.py`.
4. Найти sections generated task pack.
5. Убедиться, что нет durable check на stale handoff и GPT-5.5 outcome-first baseline.

## Expected

Current task handoff должен быть актуальным, а prompt-like generators/templates должны фиксировать:
- GPT-5.5 is not a drop-in replacement;
- fresh baseline;
- outcome, success criteria, constraints, evidence requirements, output shape, stop rules;
- stable rules above dynamic task fields.

## Actual

Эти требования зависели от ручного audit и не проверялись repo-native validator/eval.

## Classification

Reusable factory defect: влияет на downstream-consumed template prompts, `.chatgpt` task packs и handoff workflow.

## Remediation

- Обновлен `.chatgpt/codex-input.md` под текущий GPT-5.5 migration handoff.
- Добавлен GPT-5.5 prompt baseline в generated task pack и normalized handoff.
- Обновлены template `.chatgpt` prompt placeholders на outcome-first shape.
- Добавлен `validate-gpt55-prompt-contract.py`.
- Добавлен artifact eval spec `gpt-5-5-prompt-contract`.
- `verify-all.sh` теперь запускает новый validator и artifact eval smoke включает новый spec.

## Verification

См. `.chatgpt/verification-report.md` и `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-migration-report.md`.
