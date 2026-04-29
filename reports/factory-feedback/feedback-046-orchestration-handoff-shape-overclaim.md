# Factory Feedback 046: neutral handoff, runtime execution mode

Date: 2026-04-29

## Learning

Do not encode actual orchestration into the ChatGPT/user-facing handoff name. A handoff can contain orchestration candidate signals, but actual orchestration exists only if Codex launches child/subagent sessions.

## Template Change

- Prefer `handoff_shape: codex-task-handoff`.
- Keep legacy `single-agent-handoff` and `parent-orchestration-handoff` readable for old artifacts.
- Add explicit runtime decision rule: Codex chooses `single-session execution` or `orchestrated-child-sessions` after task graph analysis.
- Final closeout must report actual execution mode and `child/subagent count`.

## Why It Matters

This prevents false orchestration claims and keeps the word "orchestration" tied to real parallel/delegated execution rather than to a planning label.
