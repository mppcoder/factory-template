# Bug: compact card spacing, wrapping and Codex numbering overlap

Date: 2026-04-29

## Summary

The compact project card had avoidable blank lines, long lifecycle/module/task lines could exceed a narrow ChatGPT answer window, and Codex remediation work reused the `FT-CH` ChatGPT chat-number namespace.

## Evidence

- `visual-status-card.md.template` inserted blank lines between every card block.
- `render-project-lifecycle-dashboard.py --format chatgpt-card` emitted lifecycle and module chains as single long lines.
- `allocate-chat-handoff-id.py` and `codex_task_router.py` treated `kind: self_handoff` as a ChatGPT `FT-CH-....` allocation.
- Existing direct Codex remediation items were visible as `FT-CH-0005..FT-CH-0009`, which overlaps the user-facing ChatGPT chat title namespace.

## Expected Behavior

- Compact cards should have no extra blank lines.
- Long lines should wrap at readable boundaries before they exceed a typical ChatGPT response pane.
- `FT-CH` should identify ChatGPT task chats only.
- Codex remediation/direct work should use a separate namespace and counter.

## Remediation

- Wrap compact card lifecycle/module chains and active work lines.
- Remove blank lines from the compact card template.
- Add `codex-work-index/v1` with `FT-CX-....` IDs.
- Change direct-task bootstrap and allocation helpers so Codex self-handoff no longer consumes ChatGPT chat numbers.
