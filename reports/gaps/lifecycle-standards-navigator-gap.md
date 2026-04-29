# Gap: навигатор и контрольный слой стандартов жизненного цикла

Дата: `2026-04-29`.
Parent task: `p9-lifecycle-standards-navigator`.
Route: `chatgpt-handoff -> parent orchestration -> lifecycle standards navigator/control layer`.

## Коротко

В repo уже есть сильный control layer: `project-lifecycle-dashboard`, `task-state-lite`, `stage-state`, `feature-execution-lite`, `orchestration-cockpit-lite`, `operator-dashboard` и controlled software update governance.

Gap: эти слои показывают состояние, маршрут, execution и runtime/deploy readiness, но не отвечают машинно и единообразно на вопрос:

> какие lifecycle/process/quality/security/accessibility/operations/AI standards должны быть проверены на текущей фазе, какая evidence нужна, и можно ли безопасно продвигать фазу без false green.

## Evidence из текущего repo

- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` показывает phase, gates, handoff/orchestration, release/runtime/software updates, но не содержит `standards_navigator`.
- `template-repo/template/.chatgpt/stage-state.yaml` содержит boolean gates, но не связывает их со standards evidence.
- `template-repo/template/.chatgpt/task-state.yaml` разделяет internal/external/runtime boundaries, но не содержит standards profile.
- `docs/operator/factory-template/06-project-lifecycle-dashboard.md` описывает dashboard как state/control readout, но без lifecycle standards map.
- `docs/feature-execution-lite.md` описывает волны, checkpoint и final verification, но не говорит, какие standards gates обязательны перед переходом фаз.
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md` описывает parent/child handoff, но не контролирует standards compliance claims.
- `template-repo/scripts/validate-project-lifecycle-dashboard.py` ловит false green, secret-like content и false auto-switch, но не ловит false certification/compliance, stale standards overclaim, production/commercial claim without production gates, AI app readiness without AI safety gate.

## Классификация слоя

- Gap type: reusable template/product lifecycle control gap.
- Affected contour: `factory-template` itself and all generated projects.
- Owner boundary: `internal-repo-follow-up`.
- Defect capture path: `required-gap-capture-first`.
- No external runtime, no secrets, no downstream battle project mutation.

## Требуемая remediation

Добавить lightweight standards navigator/control layer, который связывает существующие механизмы:

- `project-lifecycle-dashboard` как единая state/control визуализация;
- standards registry как machine-readable source map;
- lifecycle stage map как normative checklist per phase;
- `standards-gates.yaml` как generated-project evidence gate template;
- validators как false-green guardrail;
- offline-first watchlist как drift/proposal mechanism;
- docs/beginner UX как human-readable explanation.

## Что не входит в цель

- Не заявлять formal ISO/OWASP/WCAG/NIST/DORA/OpenAI certification.
- Не добавлять web UI, daemon, SQLite, background worker, realtime monitoring или Telegram notifications по умолчанию.
- Не менять versions silently: standards drift идет через `standards-update-proposal -> impact classification -> user approval -> template update`.
- Не смешивать advisory route text с executable model/profile switch.

## Текущий статус источников

Live/current source research was performed on `2026-04-29` against official sources where available. The repo records the source URLs in `template-repo/standards/lifecycle-standards-registry.yaml` and `template-repo/standards/standards-watchlist.yaml`.

Important nuance: ISO currently shows `ISO/IEC/IEEE 12207:2017` as published/current but also marks the standard as expected to be revised. Therefore the registry keeps `2017` as selected baseline and adds a `verify-current`/proposal gate for future revision.
