# Контролируемые обновления ПО

## Назначение

Этот слой фиксирует controlled update flow для ОС, VPS image, package manager, runtime stack, Docker/base images, GitHub Actions и production-critical dependencies. Он не является background monitoring, auto-upgrade daemon или scheduled remediation. Любое обновление выполняется только после analysis, upgrade proposal и явного approval пользователя.

Default для VPS:

```yaml
auto_update_policy: manual-approved-upgrade
auto_install_without_approval: forbidden
strict_controlled_mode: true
```

Security updates тоже не должны автоматически менять runtime без recorded project policy exception. Если проект осознанно разрешает часть unattended security updates, exception должен быть записан в `.chatgpt/software-inventory.yaml` и отражен в readiness/dashboard.

## Базовый снимок

При каждом deployment/runbook flow Codex фиксирует baseline в `.chatgpt/software-inventory.yaml`:

- OS distro name, version и codename;
- provider image id, если его можно получить без external secret/UI;
- kernel;
- package manager sources;
- состояние `unattended-upgrades` и apt timers;
- Docker и Docker Compose version;
- Node и Python versions;
- GitHub Actions versions;
- base Docker images, tags и digests, если доступны;
- package lockfiles;
- known critical runtime dependencies.

Ubuntu/VPS правило: выбранный Ubuntu LTS release является частью baseline. OS image release и later package update state фиксируются отдельно. Переход на новую Ubuntu LTS считается отдельным migration/upgrade project, а не silent maintenance step.

## Сведения об обновлениях

`.chatgpt/software-update-watchlist.yaml` хранит источники и findings. Для каждого watched component нужны:

- official docs URL/source name;
- release notes/changelog source;
- security advisory source;
- issue/bug tracker source;
- профильные форумы как secondary signal, если полезно;
- check cadence;
- `last_checked_at`;
- `last_relevant_finding`;
- project impact classification.

Impact classification:

- `not_relevant`
- `monitor_only`
- `security_relevant`
- `feature_relevant`
- `breaking_change_risk`
- `runtime_conflict_risk`
- `upgrade_candidate`
- `blocked`

Профильные форумы являются secondary signal, а не source-of-truth. Для high-impact изменений используйте official docs, release notes, changelog, advisories и issue tracker.

## Предложение обновления

`.chatgpt/software-update-readiness.yaml` хранит readiness и proposal status. Upgrade proposal должен включать:

- current version -> target version;
- причину обновления;
- какие фичи, баги или уязвимости затрагивают проект;
- affected repo/runtime layers;
- required backups;
- restore/rollback plan;
- test matrix;
- user approval gate;
- rollout plan;
- post-upgrade monitoring;
- fallback decision.

До approval допустимы только report-only действия: inventory, watchlist update, impact classification, readiness rendering и proposal draft. Auto-upgrade/remediation без explicit approval пользователя запрещены.

## Плавающие теги в критичных production-слоях

Для production-critical layers запрещены floating `latest` tags и неприкрепленные mutable refs, где это можно определить без false positives:

- Docker `image: ...:latest` в production/deploy compose;
- base Docker image без tag/digest в production Dockerfile;
- GitHub Actions `uses: owner/action@main` или `@master` в production/release workflows.

Если floating ref нужен временно, readiness должен содержать `accepted_reason`, owner boundary и follow-up action.

## Контракт dashboard

Lifecycle dashboard показывает:

- current baseline status;
- auto-update policy;
- last update intelligence check;
- relevant findings count;
- upgrade proposal status;
- next safe action;
- fallback action;
- blockers.

Owner boundary должен быть одним из разрешенных dashboard boundaries:

- `internal-repo-follow-up`
- `external-user-action`
- `runtime-action`
- `downstream-battle-action`
- `secret-boundary-blocker`

Dashboard не считается green, если статус baseline/readiness/proposal отмечен passed/completed/done/ready без evidence или accepted reason.

## Что Codex не обещает

- Не обещает background monitoring без реального scheduled workflow.
- Не выполняет auto-install, unattended runtime upgrade или remediation без approval.
- Не пишет secrets, tokens, `.env` content или private transcripts в reports/templates.
- Не трактует переход на новую Ubuntu LTS как обычный silent maintenance step.
