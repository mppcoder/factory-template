# Support automation / поддержка автоматизации

Боевой проект / generated project получает bounded GitHub Issue -> gate -> Codex handoff -> branch/PR контур. Issue text всегда считается untrusted user content: no secrets, no shell eval, no auto-merge.

## Как запустить

- Maintainer добавляет `agent:ready` к issue или пишет `/factory fix`.
- Workflow `issue-autofix.yml` вызывает gate, renderer и runner.
- Gate отказывает для labels `security`, `external-secret`, `needs-human`, `blocked`, `agent:running`.
- `risk:high` требует явного approval.

## Локальное и reusable

- local project-owned bugs stay local;
- reusable factory feedback escalates to factory-template;
- no secrets in public issues;
- security issues go through private channel;
- issue-autofix does not run on security labels;
- no auto-merge: PR остается на human review.

Подробные gates описаны в `docs/operator/full-advanced-automation-gates.md`.
