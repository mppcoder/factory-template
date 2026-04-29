# Bug: orchestration handoff shape overclaims actual execution

Date: 2026-04-29

## Summary

The routing contract used `parent-orchestration-handoff` as a pre-execution handoff shape. This made the handoff sound like actual multi-agent orchestration before Codex had analyzed the task graph or launched child/subagent sessions.

## Evidence

- `template-repo/scenario-pack/00-master-router.md` required choosing `single-agent-handoff` vs `parent-orchestration-handoff` before issuing the handoff.
- `template-repo/scenario-pack/15-handoff-to-codex.md` repeated that pre-execution split.
- `template-repo/scripts/codex_task_router.py` returned `parent-orchestration-handoff` when it detected orchestration-like keywords.
- This allowed closeout confusion: a handoff could be called orchestration while actual `child/subagent count` was `0`.

## Expected Behavior

- User-facing handoff should be one neutral `codex-task-handoff`.
- Codex should analyze the received task and decide actual `execution_mode`.
- If Codex launches child/subagent sessions, closeout reports `orchestrated-child-sessions` and the real child/subagent count.
- If no child/subagent sessions were launched, closeout reports `single-session execution` and `child/subagent count: 0`.

## Classification

- Layer: executable routing + advisory scenario contract.
- Defect type: handoff identity / execution-mode overclaim.
- Reusable template issue: yes.

## Remediation

- Make `codex-task-handoff` the default handoff shape.
- Treat old `single-agent-handoff` / `parent-orchestration-handoff` as legacy-readable values only.
- Move orchestration choice to Codex runtime after route receipt and task graph analysis.
- Require actual execution mode and child/subagent count in closeout.
