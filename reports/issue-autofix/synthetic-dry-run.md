# Синтетический dry-run issue-autofix

Дата: 2026-05-05

## Фикстуры

Positive:
- `tests/issue-autofix/positive/docs-change-issue.json`

Negative:
- `security-label`
- `external-secret`
- `blocked-label`
- `risk-high-no-approval`
- `missing-acceptance`
- `pull-request`
- `command-injection-text`
- `secret-like-content`

## Контур proof

`template-repo/scripts/issue-autofix-smoke.py` runs all fixtures in a temporary directory:

- gate;
- handoff renderer;
- `run.yaml` generation;
- bounded runner dry-run;
- audit ledger append;
- negative refusal checks.

## Safety / безопасность

- no live GitHub mutation;
- no live label sync;
- no real PR;
- no auto-merge;
- issue text is marked as `Untrusted User Content`;
- command-injection-like and secret-like text is refused.
