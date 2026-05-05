# Готовность Universal Task Control к release

Дата проверки: 2026-05-05

## Итог

Universal Task Control готов как repo-native capability внутри `factory-template`: registry, handoff generation, issue bridge, lifecycle dashboard, task queue, docs, release notes and verification smoke are present and covered by `verify-all quick`.

Этот readiness pass не объявляет новый public release и не меняет `docs/releases/release-scorecard.yaml`; текущий release truth остается `2.5.8 Package Ready`.

## Проверенные контуры

| Контур | Evidence | Статус |
|---|---|---|
| Registry source | `template-repo/template/.chatgpt/task-registry.yaml` | passed |
| Registry validator | `template-repo/scripts/validate-task-registry.py` | passed |
| Handoff generator/validator | `template-repo/scripts/task-to-codex-handoff.py`, `template-repo/scripts/validate-codex-task-handoff.py` | passed |
| Issue bridge | `template-repo/scripts/issue-to-task-registry.py`, `tests/universal-task-control/positive/issues/feature-issue-draft.yaml` | passed |
| Preview/prepare/status/queue commands | `preview-task-handoff.py`, `prepare-task-pack.py`, `update-task-status.py`, `render-task-queue.py` | passed |
| Dashboard integration | `reports/project-lifecycle-dashboard.md`, `reports/project-status-card.md` | passed |
| Operator docs | `docs/operator/factory-template/07-universal-codex-handoff-factory.md`, `docs/operator/factory-template/08-chatgpt-codex-github-vps-one-paste-flow.md` | passed |
| Release notes | `RELEASE_NOTES.md`, `docs/releases/factory-template-release-notes.md` | passed |
| Smoke evidence | `reports/universal-task-control-happy-path-smoke.md`, `tests/universal-task-control/*` | passed |

## Targeted проверка

```bash
python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
python3 template-repo/scripts/task-to-codex-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
python3 template-repo/scripts/render-task-queue.py --registry template-repo/template/.chatgpt/task-registry.yaml --stdout
bash VALIDATE_RELEASE_NOTES_SOURCE.sh
python3 template-repo/scripts/validate-human-language-layer.py .
bash template-repo/scripts/verify-all.sh quick
```

## Граница release

- No daemon, web app, Telegram/Slack bot, database or background worker was added.
- No Codex auto-launch is claimed by queue/dashboard/handoff artifacts.
- Advisory layer remains separate from executable routing layer.
- No production deploy, public external report, auto-merge, security-sensitive action or secret handling is included in this capability.

## Вывод

Universal Task Control is release-ready as an internal repo-native factory capability and can remain in `Unreleased` notes until the next package/release decision.
