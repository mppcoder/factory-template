# Plan №5: внутреннее усиление runner и quality evidence

Date: 2026-04-28

## Область

Plan №5 не переоткрывает завершенный `2.6` template/runtime proof и не заявляет, что Plan №4 `P4-S5` real downstream/battle app pilot уже выполнен.

Цель Plan №5 — repo-local hardening после Plan №4:
- runner layer и operational reports polish;
- quality validator для curated/reference packs beyond structural checks;
- production hardening git sync fallback там, где repo evidence показывает реальные gaps;
- novice/domain acceptance expansion beyond parity smoke без требования real downstream app;
- VPS Remote SSH-first Full Handoff Orchestration Layer.

## Карта источников

Подготовка уже есть:
- Plan №4 `P4-S0..P4-S4` завершили repo-local preparation: roadmap, downstream proof docs/template, validator, handoff transcript eval и Project Knowledge reuse proof.
- Plan №4 `P4-S5/P4-S6` остаются future/blocked external contour: нужен real downstream repo, real `APP_IMAGE`, approved VPS/staging target, secrets outside repo и sanitized transcript.
- `CURRENT_FUNCTIONAL_STATE.md` прямо оставляет gaps: runner/operational reports polish, curated pack quality validator, git sync fallback hardening, novice/domain acceptance и future field pilots.
- Existing routing contract уже разделяет advisory layer и executable routing layer. Advisory тексты не переключают model/profile/reasoning в уже открытой session; надежная граница — новый task launch/profile selection.
- Official Codex boundary note: Codex CLI и IDE extension работают с локальным/выбранным repo context, а cloud delegation является отдельным режимом; OpenAI docs также разделяют `Codex Local` controls для CLI/IDE/app local workflows и `Codex Cloud` controls для delegated cloud tasks. Reference: `https://developers.openai.com/codex/cli`, `https://developers.openai.com/codex/ide`, `https://developers.openai.com/codex/app`, `https://help.openai.com/en/articles/11369540-icodex-in-chatgpt`.

## Карта gap'ов

| ID | Gap | Evidence | Plan №5 target | Boundary |
|---|---|---|---|---|
| `P5-GAP-01` | Parent orchestration layer отсутствует: один большой handoff не раскладывается repo-native образом в child sessions. | Есть `launch-codex-task.sh` и profile routing, но нет parent runner/report contract. | `P5-S1/P5-S2/P5-S3` | repo |
| `P5-GAP-02` | Operational reports фиксируют launch route, но не parent/child result contract. | `.chatgpt/task-launch.yaml`, normalized handoff. | `P5-S3` | repo |
| `P5-GAP-03` | Curated/reference packs проверяются структурно и частично semantically, но нет отдельного quality validator для usefulness/phase/profile fit/noise. | `sources-profiles.yaml`, export tooling. | `P5-S4` | repo |
| `P5-GAP-04` | Git sync fallback есть, но fallback evidence не оформлен как release-facing coverage matrix. | `verified-sync.py`, `factory_automation_common.py`. | `P5-S5` | repo evidence / remote runtime |
| `P5-GAP-05` | Novice acceptance smoke покрывает parity/guided flow, но мало domain scenario acceptance examples. | `tests/onboarding-smoke/run-novice-e2e.sh`. | `P5-S6` | repo, future downstream optional |
| `P5-GAP-06` | Cloud/App wording can drift into false default path. | Existing docs mention VS Code manual UI, but no orchestration-specific validator. | `P5-S1/P5-S2` | repo docs / operator UI |

## Дорожная карта

### P5-S0 — audit/source map/gap map after Plan №4

Output:
- this roadmap source map;
- gap map;
- explicit scope boundary.

Acceptance:
- no claim that Plan №4 real downstream app proof ran;
- no claim that Plan №5 needs a real downstream app.

### P5-S1 — VPS Remote SSH-first orchestration contract

Output:
- `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`;
- updates to `template-repo/template/docs/codex-workflow.md`;
- updates to `docs/operator/factory-template/03-mode-routing-factory-template.md`.

Default path:
- Browser ChatGPT Project produces one large handoff.
- VS Code Remote SSH window opens the VPS repo.
- Codex extension in that Remote SSH window receives the handoff.
- Repo-native orchestrator splits work into subtask specs.
- Codex CLI sessions run on VPS/repo context per explicit profile/model/reasoning.
- Parent report collects results and blockers.

Guardrails:
- Codex App/Cloud Director is optional, not default.
- Already-open sessions are not reliable auto-switch.
- Parent orchestrator does not do specialist work inline when a child route says separate session/profile.

### P5-S2 — repo-native orchestration runner

Output:
- dry-run safe script in `template-repo/scripts/`;
- positive and negative fixtures under `tests/codex-orchestration/`;
- orchestration report under `reports/orchestration/` or explicit output path.

Required behavior:
- read YAML/JSON orchestration plan generated from one large handoff;
- classify/confirm subtasks as `quick/build/deep/review`;
- resolve each subtask through existing routing/profile config;
- generate per-subtask handoff/session files;
- default dry-run prints commands and writes reports;
- launch separate Codex CLI subprocesses only with explicit `--execute`;
- record selected profile/model/reasoning/scenario per subtask;
- move all user-required/external/runtime/downstream actions to `deferred_user_actions` at final closeout;
- use safe temporary placeholders where possible and record `placeholder_replacements` for final replacement reminders;
- detect stale/missing model mapping and report instead of silently falling back;
- keep secrets outside repo.

### P5-S3 — operational reports polish

Output:
- parent orchestration report template/format;
- per-subtask result contract;
- final parent closeout contract;
- failure/blocker taxonomy.

Taxonomy must distinguish:
- internal repo follow-up;
- external user action;
- runtime action;
- downstream/battle action.

### P5-S4 — curated/reference pack quality validator

Output:
- `validate-curated-pack-quality.py`;
- positive and negative fixtures;
- quick verify integration.

Checks:
- usefulness and purpose by profile;
- phase/profile fit;
- stale duplicates;
- missing routing-critical docs;
- over-noisy packs;
- no missing files in manifest.

### P5-S5 — git sync fallback hardening and evidence

Output:
- inspect existing verified sync fallback strategy;
- add docs/tests/fixtures only where gaps are real;
- avoid rewriting stable sync logic without defect evidence;
- report coverage for blocked push, remote drift, protected branch, branch ahead/dirty state and fallback instructions.

### P5-S6 — novice/domain acceptance expansion

Output:
- domain scenario acceptance template/examples that extend beyond parity smoke;
- real downstream field pilots remain future external contour.

### P5-S7 — verification and release-facing closeout

Output:
- update `CURRENT_FUNCTIONAL_STATE.md`, `docs/releases/post-2.5-gap-register.md`, `TEST_REPORT.md` and release-facing docs as required;
- run targeted validators and quick verify;
- commit/push if verify green and remote sync is available;
- final closeout includes git status, commit hash/sync status or explicit blocker.

## Статус

Current stage: `P5-S0 -> P5-S7 implementation`.

Release status is unchanged: this roadmap is internal hardening and does not declare a new release-ready state.
