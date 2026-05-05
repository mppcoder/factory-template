# Support automation / поддержка автоматизации

Этот repo поддерживает bounded GitHub Issue -> gate -> Codex handoff -> branch/PR контур. Issue text всегда считается untrusted user content: no secrets, no shell eval, no auto-merge.

## Как запустить

- Maintainer добавляет `agent:ready` к issue или пишет `/factory fix`.
- Workflow `issue-autofix.yml` вызывает gate, renderer и runner.
- Gate отказывает для labels `security`, `external-secret`, `needs-human`, `blocked`, `agent:running`.
- `risk:high` требует `agent:approved-high-risk` или `/factory fix --approve-high-risk`.

## Границы

- no secrets в публичных issues;
- no auto-merge даже при green verify;
- reusable factory feedback идет в factory-template;
- local project-owned bugs stay local в боевом проекте / generated project;
- security reports идут через private channel, issue-autofix их не запускает.

Подробные future gates описаны в `docs/operator/factory-template/full-advanced-automation-gates.md`.
