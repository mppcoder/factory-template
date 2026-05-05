# Bug: ChatGPT title number can be shown without repo reservation

Date: 2026-05-05

## Summary

The first ChatGPT answer contract allowed an `FT-CH-....` title to be treated like a suggested next number instead of a materialized repo reservation. If the handoff was not launched in Codex, the number still looked free in `.chatgpt/chat-handoff-index.yaml` / GitHub state and could be allocated to another chat.

## Evidence

- `00-master-router.md` said the title comes from repo index / allocator, but did not explicitly forbid read-only next-number calculation or dry-run output as a visible title.
- `docs/operator/factory-template/06-project-lifecycle-dashboard.md` said Project Instructions can "propose" a stable title, which made a non-written number sound valid.
- `allocate-chat-handoff-id.py --dry-run` printed the same `ChatGPT title to copy:` label even though it did not write `.chatgpt/chat-handoff-index.yaml`.
- `allocation_policy` did not encode that visible titles require a materialized index item and that unlaunched handoffs keep their number reserved.

## Expected Behavior

- A visible `FT-CH-....` in the first ChatGPT answer means the allocator has already written an item to `.chatgpt/chat-handoff-index.yaml`.
- If repo write is unavailable or not confirmed, ChatGPT must show exactly: `Нужно выделить номер через repo chat-handoff-index / allocator.`
- `--dry-run` may be used only for diagnostics and must clearly say the number is not reserved.
- If the user never launches the handoff in Codex, the repo item remains allocated and must be closed explicitly rather than reused.

## Classification

Reusable factory-template defect in the advisory/policy layer, executable allocator/router layer, validators and operator docs.

## Remediation

- Strengthen `allocation_policy` for materialized visible-title reservations.
- Make validators require the reservation contract.
- Change allocator dry-run output so it cannot be mistaken for a copyable reserved title.
- Update router, handoff scenario and operator Project Instruction snippets to forbid proposed/unwritten `FT-CH` numbers.
