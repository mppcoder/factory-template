# Plan №6 orchestration productization gap / gap продуктового слоя

Date: 2026-04-28

## Кратко

Plan №5 закрыл repo-native full handoff orchestration runner и validator, но beginner-facing productization слой еще не был оформлен как проверяемый UX:

- нет compact cockpit/status artifact для parent handoff и child tasks;
- нет отдельного parent-plan template/validator wrapper для превращения большого ChatGPT handoff в `codex-orchestration/v1`;
- route receipt не имеет машинно проверяемого route-explain слоя;
- beginner full handoff UX scorecard не выделен как отдельный validator/eval;
- safe rehearsal не зафиксирован как release-facing report.

## Reproduce / evidence / воспроизведение

Проверенные источники:

- `docs/releases/plan-5-internal-hardening-roadmap.md` фиксирует Plan №5 как implemented/verified.
- `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md` описывает runner/runbook, но не содержит cockpit-lite и scorecard closeout UX.
- `template-repo/scripts/validate-codex-orchestration.py` проверяет core runner contract, но не оценивает beginner one-handoff UX как отдельный scorecard.
- `CURRENT_FUNCTIONAL_STATE.md` после Plan №5 рекомендует P4-S5/P4-S6 только при real downstream app и не имеет текущего Plan №6 productization status.

Дополнительный compatibility gap: incoming Plan №6 handoff использует `replacement_timing: future-user-action` для future P4-S5/P4-S6 placeholders, а Plan №5 runner принимал только `final-user-action`. Это корректный future-boundary metadata для текущего handoff и не должен считаться real downstream proof.

## Layer classification / классификация слоя

- advisory/policy layer: scenario-pack, operator docs, release-facing docs, beginner UX scorecard.
- executable routing layer: parent plan validator, cockpit renderer/validator, route explain script, quick verify integration.
- owner boundary: `internal-repo-follow-up`.

## Remediation decision / решение по исправлению

Исправлять в текущем Plan №6 scope:

- добавить cockpit-lite docs/template/renderer/validator;
- добавить parent orchestration plan template и validator wrapper;
- добавить route-explain слой;
- добавить beginner UX scorecard validator/fixtures/eval;
- провести safe synthetic rehearsal без real downstream/runtime claims;
- обновить release-facing docs и quick verification.

## Boundaries / границы

Не исправлять в этом scope:

- не импортировать AIF web app/daemon/SQLite/Telegram stack;
- не импортировать Claude-specific `.claude` layout, slash commands или TeamCreate как mandatory core;
- не заявлять real downstream/battle app proof;
- не переоткрывать Plan №5 runner/fallback/curated validator без отдельного evidence defect.
