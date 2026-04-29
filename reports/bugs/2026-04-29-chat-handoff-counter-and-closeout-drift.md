# Bug: chat handoff counter and closeout wording drift

- id: `bug-2026-04-29-chat-handoff-counter-and-closeout-drift`
- date: `2026-04-29`
- source: user remediation request after stable chat index implementation
- severity: high
- layer: advisory/policy + executable routing + closeout contract

## Evidence

- Closeout response used English section labels and English prose even though `factory-template` human-facing closeout must be Russian.
- Closeout said `parent orchestration handoff handled in this session` with `child/subagent count: 0`, which confused handoff shape with actual subagent/orchestration execution.
- `allocate-chat-handoff-id.py` existed, but the executable bootstrap path did not assign `chat_id` to `chatgpt-handoff` or `direct-task self_handoff` before the first visible response.
- `kind: self_handoff` reused the ChatGPT handoff status chain instead of a Codex self-handoff chain.

## Expected

- Final closeout is Russian, except for technical literal values.
- If no child/subagent sessions ran, closeout says `child/subagent count: 0` and describes actual execution as single-session remediation, not an agent orchestra.
- First ChatGPT handoff response references a stable `chat_id` from `.chatgpt/chat-handoff-index.yaml`.
- Codex self-handoff uses the same repo counter and records `kind: self_handoff`.

## Classification

Reusable factory-template defect. The fix belongs in scenario rules, executable bootstrap, validators, docs and dashboard/register artifacts.

## Remediation

- Add `allocation_policy` to chat handoff index.
- Make validator enforce shared counter policy and separate `self_handoff` status chain.
- Make bootstrap allocate `chat_id` for `chatgpt-handoff` and `direct-task` before rendering handoff/self-handoff artifacts.
- Make handoff response validator require stable chat identity fields.
- Update repo docs and scenario rules for Russian closeout and actual child/subagent count wording.
