# Factory feedback 045: chat handoff counter and closeout drift

Source bug: `reports/bugs/2026-04-29-chat-handoff-counter-and-closeout-drift.md`

## Learning

Stable chat titles need an executable allocation boundary, not only a documented title policy. This original learning incorrectly used one shared counter for both ChatGPT handoff and Codex self-handoff; that part is superseded by `feedback-050-card-wrap-and-codex-numbering.md`.

Closeout must also distinguish:

- handoff shape: `single-agent-handoff` / `parent-orchestration-handoff`;
- actual execution mode: single live session, repo-native orchestrator, or child/subagent sessions;
- actual child/subagent count.

## Template action

- Keep `.chatgpt/chat-handoff-index.yaml` as the ChatGPT chat-title counter/source of truth.
- Superseded on 2026-04-29: direct-task bootstrap now allocates `kind: self_handoff` from `.chatgpt/codex-work-index.yaml`, not from the ChatGPT `FT-CH` counter.
- Require stable chat identity fields in handoff responses.
- Keep user-facing closeout Russian for `factory-template`.
