# Factory Feedback 054: Codex first answer needs request number and project card

Date: 2026-05-06

## Learning

The `FT-CX` Codex work identity is not enough if it only appears inside a large handoff block. Operators need the Codex request number and compact project card at the top of the first substantive Codex direct-task response, before route receipt or remediation.

## Template Change

- Direct-task Codex responses start with `Номер запроса Codex` and `Карточка проекта`.
- `FT-CX-....` comes only from `.chatgpt/codex-work-index.yaml`; if the write is not confirmed, Codex shows the exact codex-work allocator blocker.
- The project card comes from the repo dashboard renderer and cannot be replaced by free-form prose.
- The Codex execution card includes a `request:` line so status readouts expose the current `FT-CX` / `FT-CH` identity.
