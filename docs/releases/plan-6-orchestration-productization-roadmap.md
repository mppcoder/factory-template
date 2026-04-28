# Plan №6: beginner-first full handoff UX productization / продуктовый слой

Date: 2026-04-28

## Область

Plan №6 добавляет productization слой поверх уже закрытого Plan №5.

Plan №5 считать implemented/verified: repo-native orchestration runner, parent report, core validator, runner fail-fast, curated pack quality, sync fallback evidence and domain acceptance examples уже закрыты.

Plan №6 не переоткрывает runner/fallback/curated validator без отдельного defect evidence. Цель Plan №6: сделать full handoff orchestration читаемым для новичка, наблюдаемым и проверяемым как поток `one handoff -> parent orchestration -> child tasks -> понятный closeout`.

## Source map / карта источников

- Plan №5 evidence: `docs/releases/plan-5-internal-hardening-roadmap.md`.
- Current status: `CURRENT_FUNCTIONAL_STATE.md`.
- Verification evidence: `TEST_REPORT.md`.
- Gap register: `docs/releases/post-2.5-gap-register.md`.
- AIF/Molyanov audit boundary: `docs/releases/plan-3-aif-molyanov-audit.md`.
- Full handoff runbook: `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`.
- Handoff scenario: `template-repo/scenario-pack/15-handoff-to-codex.md`.
- Executable routing contract: `template-repo/codex-routing.yaml`.

## Completed Plan №5 evidence / закрытые evidence

| Evidence | Status | Boundary |
|---|---|---|
| Parent orchestration runner and validator | implemented/verified | repo executable |
| Parent report and child handoff/session files | implemented/verified | repo evidence |
| `user_actions_policy: defer-to-final-closeout` | implemented/verified | orchestration guardrail |
| Secret-like fail-fast before writing artifacts | implemented/verified | security |
| Curated pack quality validator | implemented/verified | reference packs |
| Git sync fallback evidence matrix | implemented/verified | release evidence |

## Plan №6 new gaps / новые gap'ы

| ID | Gap | Evidence | Target | Boundary |
|---|---|---|---|---|
| `P6-GAP-01` | Beginner-readable cockpit/status view absent. | Runner report exists, but no compact status artifact for parent/children/blockers/next action. | `docs/operator/factory-template/05-orchestration-cockpit-lite.md`, template artifact, renderer/validator. | repo UX |
| `P6-GAP-02` | Parent handoff normalization not separately productized. | Core orchestration validator exists, but no template wrapper that teaches big handoff -> `codex-orchestration/v1`. | parent plan template and validator wrapper. | repo executable |
| `P6-GAP-03` | Route explanation is implicit. | Routing config has keywords/profiles, but route receipt does not expose deterministic evidence/keywords/live catalog boundary. | route-explain script and doc/update. | repo routing |
| `P6-GAP-04` | Beginner full handoff UX lacks scorecard. | Artifact Eval has orchestration coverage, but not one-copy-paste/no-hidden-step/final-continuation UX checklist. | scorecard validator, fixtures, eval report. | repo eval |
| `P6-GAP-05` | Safe rehearsal evidence absent. | Plan №5 dry-run proves runner mechanics, not beginner-facing synthetic rehearsal report. | report under `reports/orchestration/`. | repo evidence |
| `P6-GAP-06` | Future boundary placeholders need explicit normalization. | Incoming handoff uses `future-user-action`; runner accepted only `final-user-action`. | allow future boundary metadata without claiming real proof. | executable validator |

## Дорожная карта

### P6-S0 — audit/source map/gap map / аудит

Status: implemented in this plan.

Output:
- this roadmap;
- `reports/bugs/2026-04-28-plan-6-orchestration-productization-gap.md`;
- release-facing planning updates.

### P6-S1 — cockpit-lite / панель статуса

Status: implemented in this plan.

Output:
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md`;
- `template-repo/template/.chatgpt/orchestration-cockpit.yaml`;
- `reports/orchestration/orchestration-cockpit.md.template`;
- `template-repo/scripts/render-orchestration-cockpit.py`;
- `template-repo/scripts/validate-orchestration-cockpit.py`.

### P6-S2 — parent plan normalization / нормализация

Status: implemented in this plan.

Output:
- `template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template`;
- `template-repo/scripts/validate-parent-orchestration-plan.py`;
- positive/negative fixtures reused from `tests/codex-orchestration/fixtures/*`.

### P6-S3 — route explanation / объяснение маршрута

Status: implemented in this plan.

Output:
- `template-repo/scripts/explain-codex-route.py`;
- `template-repo/scripts/validate-route-explain.py`;
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md` route receipt guidance.

### P6-S4 — beginner UX scorecard / scorecard новичка

Status: implemented in this plan.

Output:
- `template-repo/scripts/validate-beginner-handoff-ux.py`;
- `tests/beginner-handoff-ux/*`;
- `tests/artifact-eval/specs/beginner-full-handoff-ux.yaml`;
- `tests/artifact-eval/reports/beginner-full-handoff-ux.md`.

### P6-S5 — safe rehearsal / безопасная репетиция

Status: implemented in this plan.

Output:
- `reports/orchestration/plan-6-safe-rehearsal.md`;
- dry-run/execute-safe evidence only;
- no real VPS mutation, no secrets, no downstream proof claim.

### P6-S6 — release-facing closeout / закрытие

Status: implemented in this plan after verification.

Output:
- `CURRENT_FUNCTIONAL_STATE.md`;
- `TEST_REPORT.md`;
- `CHANGELOG.md`;
- `RELEASE_NOTES.md`;
- `docs/releases/post-2.5-gap-register.md`.

## Future boundary / будущая граница

P4-S5/P4-S6 real downstream/battle app proof remains a future boundary. It requires a real downstream repo, real `APP_IMAGE`, approved VPS/staging target, secrets outside repo and sanitized transcript. Plan №6 synthetic rehearsal is not that proof.
