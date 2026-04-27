# Artifact Eval Harness gap

Дата: 2026-04-27
Статус: fixed-in-current-scope
Класс: quality-eval / template defect

## Симптом

`skill-tester-lite` описывает ручной optional QA loop для skills и prompt-like artifacts, но в repo нет reusable harness для одинаковой проверки scenario-pack, handoff blocks, runbooks, policy docs, template skills и advanced execution artifacts.

## Evidence

- `template-repo/skills/skill-tester-lite/SKILL.md` содержит только desk-test workflow без machine-readable spec.
- `template-repo/scripts/eval-artifact.py` отсутствовал.
- `template-repo/scripts/validate-artifact-eval-report.py` отсутствовал.
- `tests/artifact-eval/` отсутствовал, поэтому не было sample specs/reports и quick-safe smoke.
- Новый `feature-execution-lite` уже имеет execution-plan, checkpoint, decisions, task waves и final verification evidence, но не был target для artifact-level eval.

## Layer classification

- advisory/policy layer: `skill-tester-lite`, docs и sample specs задают правила оценки.
- executable routing layer: `eval-artifact.py`, `validate-artifact-eval-report.py` и optional quick smoke выполняют deterministic validation.

## Impact

Без общего harness качество prompt-like artifacts проверяется вручную и не оставляет сравнимого evidence. Это повышает риск regressions в route/handoff/runbook/policy слоях и не даёт проверить advanced execution artifacts без отдельного кастомного validator.

## Remediation

- Добавить generic artifact eval spec.
- Реализовать lightweight deterministic runner без внешних parallel runners.
- Добавить validator, который ловит пустые или фиктивные reports.
- Добавить sample evals для master-router, Codex handoff response, skill-tester-lite и feature-execution-lite.
- Подключить smoke в `verify-all.sh quick`.
