# Factory feedback 045: chat handoff counter and closeout drift

Source bug: `reports/bugs/2026-04-29-chat-handoff-counter-and-closeout-drift.md`

## Learning

Stable chat titles need an executable allocation boundary, not only a documented title policy. Both ChatGPT handoff and Codex self-handoff must consume the same repo counter before the first visible handoff/self-handoff response.

Closeout must also distinguish:

- handoff shape: `single-agent-handoff` / `parent-orchestration-handoff`;
- actual execution mode: single live session, repo-native orchestrator, or child/subagent sessions;
- actual child/subagent count.

## Template action

- Keep `.chatgpt/chat-handoff-index.yaml` as the shared counter/source of truth.
- Make direct-task bootstrap allocate `kind: self_handoff` from the same counter.
- Require stable chat identity fields in handoff responses.
- Keep user-facing closeout Russian for `factory-template`.
