# Feedback 062: handoff language validator should allow technical YAML keys

Источник: `reports/bugs/2026-05-08-handoff-language-yaml-scope-false-positive.md`

## Reusable issue

The handoff language validator must distinguish source-facing English labels from technical YAML keys inside structured blocks such as `goal_contract`.

## Required factory change

Keep blocking top-level human-facing labels like `Repo:`, `Goal:`, `Entry point:` and `Scope:`, but allow indented YAML keys such as `  scope:` in technical contract blocks.

## Acceptance

- Matrix factory-bugflow generated handoff passes `validate-handoff-language.py`.
- Negative fixture with top-level `Goal:` still fails.
- Full `bash template-repo/scripts/verify-all.sh` passes.
