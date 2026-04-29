# Factory feedback: controlled software update governance gap

## Статус
open -> remediation-in-current-task

## Кратко
В шаблоне не было обязательного контура controlled software update governance для ОС, VPS image, runtime stack, base images, GitHub Actions и production-critical зависимостей. Из-за этого generated projects могли уходить в deploy/operate без фиксированного baseline, watchlist, readiness state и approval gate для upgrade proposal.

## Недостаточный contour
- Runbook packages не требовали фиксировать Ubuntu/VPS image release, kernel, package sources, Docker/Compose, Node/Python, lockfiles, base images/tags/digests и critical runtime dependencies.
- Lifecycle dashboard не показывал software update baseline, auto-update policy, update intelligence freshness, relevant findings, proposal status, safe next action, fallback и blockers.
- Generated project template не содержал inventory/watchlist/readiness artifacts для контролируемых обновлений.
- Validators не проверяли наличие этих artifacts и не блокировали false green без evidence.
- Release/operate docs не давали единого policy/spec слоя для manual-approved upgrade flow.

## Затронутые слои
- `docs/operator/runbook-packages/`
- `docs/operator/factory-template/06-project-lifecycle-dashboard.md`
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- generated project template `.chatgpt` и `reports/software-updates/`
- validators и quick verify
- release/operate docs: `CURRENT_FUNCTIONAL_STATE.md`, `CHANGELOG.md`

## Риск
Uncontrolled distro/runtime updates can silently break VPS deployments, generated projects and supportability. Особенно опасный путь: unattended upgrades или floating `latest`/base tags меняют Ubuntu packages, Docker/Compose/runtime или production-critical layers без recorded baseline, test matrix, rollback plan и явного approval пользователя.

## Remediation summary
- Добавить policy/spec `docs/operator/software-update-governance.md`.
- Materialize generated project artifacts: `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml`, `reports/software-updates/README.md`.
- Расширить lifecycle dashboard блоком `software_update_governance`.
- Обновить runbook packages для factory-template, greenfield и brownfield paths: baseline, unattended upgrades check, no auto-install without approval, watchlist/readiness, Ubuntu LTS migration as separate project.
- Добавить report-only helper scripts и validator.
- Подключить validator к quick/generated verify.
