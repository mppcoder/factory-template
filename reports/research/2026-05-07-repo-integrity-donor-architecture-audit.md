# Аудит целостности repo и donor architecture

Дата отчета: 2026-05-08
Запрошенный artifact path: `reports/research/2026-05-07-repo-integrity-donor-architecture-audit.md`
Launch source: `chatgpt-handoff`
Handoff id/title: `allocation-blocked` / `Нужно выделить номер через repo chat-handoff-index / allocator.`
Execution mode: `single-session execution`
Child/subagent count: `0`

## Подтверждение маршрута

- Project profile: `factory-template / greenfield-product with factory-producer-owned layer`
- Selected profile/model/reasoning: `deep` / `gpt-5.5` / `high`
- Selected scenario: `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/15-handoff-to-codex.md`
- Pipeline stage: `deep audit / research -> gap-capture -> optional remediation handoffs`
- Handoff allowed: `true`
- Handoff shape: `codex-task-handoff`
- Defect capture path: conditional; executed for confirmed inconsistencies before remediation.

## Краткий итог

Repo is structurally coherent: the core architecture, release truth, donor/reference boundaries, bounded automation, Symphony-compatible workflow and curator proposal loop are present and validator-backed.

Two confirmed consistency defects were found and remediated:

1. `FACTORY_MANIFEST.yaml` correctly declared `factory_producer_layer: true`, but rendered dashboard/card output showed `Factory producer layer: False`.
2. Ops module readiness was green while `software_update_governance.baseline_status` remained `pending`.

No evidence was found that OpenClaw became a core dependency, that Symphony/Hermes layers became daemon/auto-merge automation, or that AI readiness was overclaimed. AI remains `not_applicable`.

## Матрица покрытия donor/source

| Donor/source | Imported principle | Repo-native implementation | Evidence | Validator coverage | Rejected parts | Remaining gap | Risk |
|---|---|---|---|---|---|---|---|
| Molyanov/AIF | Lightweight task state, plan/implement/review/done, Project Knowledge, waves/checkpoints/evals | `.chatgpt/task-state.yaml`, Project Knowledge Done Loop, `feature-execution-lite`, Artifact Eval Harness, learning patch loop | `docs/releases/plan-3-aif-molyanov-audit.md`, `docs/releases/2.6-roadmap.md`, `CURRENT_FUNCTIONAL_STATE.md` | `validate-task-state-lite.py`, `validate-project-knowledge-update.py`, Artifact Eval specs, quick verify | Claude-specific `.claude`, Claude commands, mandatory TeamCreate, model switching as core value | Further real downstream adoption is future/optional | Low; useful ideas are adapted without foreign workflow import |
| Hermes-like curator | Proposal loop for recurring patterns | `template-repo/scripts/factory-curator.py`, `reports/curator/*`, promotion flow | `docs/operator/factory-template/factory-curator.md`, `reports/advanced-automation/final-readout.md` | `validate-factory-curator.py`, curator promotion validator | Hidden self-learning, auto-apply, silent mutation | Future curator-class `FT-TASK` can be added only through explicit flow | Low |
| Symphony-compatible workflow | Issue/task tracker plus bounded agent execution | GitHub Issues + `.chatgpt/task-registry.yaml`, one-task runner, statuses/labels contract | `docs/operator/factory-template/symphony-compatible-workflow.md`, `WORKFLOW.md`, `reports/advanced-automation/source-map.md` | `validate-symphony-workflow.py`, task registry validators | Daemon, unrestricted concurrency, `pull_request_target`, auto-merge | Worktree isolation can mature later if concurrency is explicitly enabled | Low |
| OpenClaw optional reference | Real brownfield/runtime pilot as reference evidence | Optional domain pack and field reports; retained as evidence/reference, not core | `factory/producer/reference/domain-packs/openclaw-reference/README.md`, `reports/release/*field*`, `CURRENT_FUNCTIONAL_STATE.md` | `validate-tree-contract.py`, tree naming policy, language archive exceptions | Domain-specific core, public endpoint overclaim, raw secrets/runtime copy | Optional public HTTPS proof remains external approval boundary | Medium if future docs blur reference vs core; current state is bounded |
| Advanced automation / issue autofix | Safe issue -> gate -> handoff -> bounded runner path | `issue-autofix` gate, normalized handoff, bounded runner, approval gates, audit/readout | `reports/advanced-automation/source-map.md`, `reports/advanced-automation/final-readout.md`, `RELEASE_NOTES.md` | `validate-advanced-automation-gates.py`, `validate-bounded-runner.py`, issue-autofix support validators | Security issue autofix, production deploy, auto-merge, untrusted issue execution | Future full automation remains gated/disabled-by-default | Low |
| Standards navigator | Lifecycle evidence map and false-compliance guard | Standards registry, dashboard gate summary, module readiness, false compliance boundary | `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`, `reports/project-lifecycle-dashboard.md` | `validate-standards-gates.py`, `validate-project-lifecycle-dashboard.py` | Formal ISO/NIST/OWASP/WCAG/DORA/OpenAI compliance/certification claims | Ops readiness now in progress until software update baseline closes | Medium until software inventory baseline is filled |

## Проверки целостности

| Check | Result | Evidence | Action |
|---|---|---|---|
| GA/package ready vs release/deploy pending | Non-defect clarification | `docs/releases/release-scorecard.yaml` and README say `2.5.8 Package Ready`, while lifecycle dashboard phase remains `release -> deploy` and deploy/runtime status is `pending`. | No release status change. Package-ready means repo/release artifact readiness, not deployed/operated production state. |
| Factory producer layer true vs dashboard false | Confirmed defect | `FACTORY_MANIFEST.yaml` vs rendered `reports/project-lifecycle-dashboard.md` before remediation | Bug report + renderer fix + regenerated dashboard/card. |
| Module readiness completed vs software update governance pending | Confirmed defect | Ops module referenced `software_update_governance` while baseline was pending | Bug report + Ops downgraded to `in_progress` + validator cross-field invariant. |
| AI not applicable boundary | Non-defect | AI module and `ai_safety_gate` are `not_applicable` with accepted reason; no AI app claim is present | No change. |
| OpenClaw optional reference does not leak into core | Non-defect with local hygiene note | Core docs state optional reference; tree contract allows only `factory/producer/reference/domain-packs/openclaw-reference` as source path. Historical/brownfield reports retain field evidence. An ignored local `openclaw.code-workspace` exists but is untracked and excluded by `.gitignore`. | No repo source change; do not promote ignored local workspace into tracked source. |
| Symphony/Hermes automation bounded | Non-defect | Workflow says max concurrency `1`; curator is read-only/proposal-only; automation readout forbids auto-merge, production deploy, security autofix and untrusted issue execution. | No change. |

## Подтвержденные дефекты

| Defect | Layer | Capture | Remediation |
|---|---|---|---|
| Dashboard factory producer layer drift | `factory-template` | `reports/bugs/2026-05-08-dashboard-factory-producer-layer-drift.md`, `reports/factory-feedback/feedback-059-dashboard-factory-producer-layer-drift.md` | Renderer overlays root `FACTORY_MANIFEST.yaml` for factory-template readout only; dashboard/card regenerated. |
| Module readiness software update false green | `shared` | `reports/bugs/2026-05-08-module-readiness-software-update-false-green.md`, `reports/factory-feedback/feedback-060-module-readiness-software-update-false-green.md` | Ops readiness is `in_progress`; dashboard validator blocks green modules that reference pending software update governance. |

## Уточнения без дефекта

- `2.5.8 Package Ready` and `GA-ready: true` are repo/release evidence states, not deploy/operate claims.
- `release`/`deploy` pending in lifecycle dashboard is acceptable because deploy/runtime proof is separate and approval-gated.
- AI remains not applicable because this repo has not declared AI model, agent or AI-output product behavior.
- OpenClaw evidence is reference/field-pilot evidence, not a core dependency.
- Advanced automation remains bounded, dry-run/gated and non-daemon by default.
- No formal ISO/NIST/OWASP/WCAG/DORA/OpenAI compliance is claimed.

## Обновленные артефакты

- `template-repo/scripts/render-project-lifecycle-dashboard.py`
- `template-repo/scripts/validate-project-lifecycle-dashboard.py`
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `reports/project-lifecycle-dashboard.md`
- `reports/project-status-card.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `docs/releases/post-2.5-gap-register.md`
- `reports/bugs/2026-05-08-dashboard-factory-producer-layer-drift.md`
- `reports/bugs/2026-05-08-module-readiness-software-update-false-green.md`
- `reports/factory-feedback/feedback-059-dashboard-factory-producer-layer-drift.md`
- `reports/factory-feedback/feedback-060-module-readiness-software-update-false-green.md`

## Статус проверки

Targeted verification passed:

- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `python3 template-repo/scripts/validate-standards-gates.py .`
- `python3 template-repo/scripts/validate-runbook-packages.py .`
- `python3 template-repo/scripts/validate-symphony-workflow.py .`
- `python3 template-repo/scripts/validate-factory-curator.py .`
- `python3 template-repo/scripts/validate-advanced-automation-gates.py .`
- `python3 template-repo/scripts/validate-tree-contract.py .`
- `python3 template-repo/scripts/validate-curated-pack-quality.py .`
- `python3 template-repo/scripts/validate-human-language-layer.py .`
- `bash template-repo/scripts/verify-all.sh quick`

`bash template-repo/scripts/verify-all.sh quick` ended with `VERIFY-ALL ПРОЙДЕН (quick)`.
`validate-human-language-layer.py` initially caught English active headings in this audit update; they were corrected before final verification. Final result: `active findings: 0`.

## Оставшийся gap

The software update governance baseline remains intentionally pending. Next safe action remains report-only: fill `.chatgpt/software-inventory.yaml`, verify unattended-upgrades/package/runtime state and update watchlist without installing updates.
