# Bug: generated rehearsal project exposed stale dashboard state and no fallback card artifact

- id: `bug-2026-05-07-rehearsal-route-audit-state-card-drift`
- detected: `2026-05-07`
- source: `Beginner First Rehearsal E` ChatGPT Project route audit
- affected repo: `https://github.com/mppcoder/beginner-first-rehearsal-20260507e`
- owner_boundary: factory template launcher/materialization and generated `.chatgpt` state
- severity: medium

## Symptom

The rehearsal ChatGPT Project correctly printed the allocator blocker because it had no materialized write path to `.chatgpt/chat-handoff-index.yaml`.

The same audit also found real generated-project drift:

- no fallback `reports/project-status-card.md` or `reports/project-lifecycle-dashboard.md` was present for ChatGPT to use when it cannot run the renderer;
- generated dashboard still referenced factory-template handoff `FT-CH-0011-unified-roadmap`, while the generated repo chat index had no such item;
- `.chatgpt/stage-state.yaml` was `done`, but `.chatgpt/task-state.yaml` remained `current_state: intake`;
- `.chatgpt/active-scenarios.yaml` retained `status: нужно_обновить_repo_first_инструкцию` after the rehearsal Project was already created and used.

## Expected behavior

Generated projects should be self-consistent after first-project rehearsal closeout:

- ChatGPT first answer can use a repo-rendered fallback card from `reports/project-status-card.md` or `reports/project-lifecycle-dashboard.md`;
- dashboard `active_change` must not point to factory-only `FT-CH` items unless the generated repo has that materialized chat index item;
- done stage must not coexist with task-state `intake`;
- the generated project should clearly distinguish a normal allocator blocker from actual repo-state drift.

## Reproduction

1. Create a new greenfield project through the factory launcher and first-project rehearsal flow.
2. Create a ChatGPT Project for the generated repo with repo-first instruction.
3. Ask it to verify the repo-first route.
4. Observe allocator blocker plus card/state drift findings.

## Layer classification

- generated project materialization: `template-repo/launcher.sh`;
- rehearsal artifact filler: `tools/fill_smoke_artifacts.py`;
- dashboard validator cross-artifact consistency: `template-repo/scripts/validate-project-lifecycle-dashboard.py`;
- current downstream rehearsal repo state.

## Fix direction

- sanitize generated dashboard `active_change`, `multi_step_execution` and `handoff_orchestration` during launcher materialization;
- render fallback project card/dashboard reports into generated projects;
- update smoke artifact filler to set task-state done and refresh rendered reports;
- make dashboard validation fail when generated dashboard references a missing chat handoff id or when `done_complete=true` coexists with `task-state` intake.
