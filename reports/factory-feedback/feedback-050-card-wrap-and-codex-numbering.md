# Factory Feedback 050: compact cards need soft wrapping and separate Codex IDs

Date: 2026-04-29

## Learning

The compact project card is pasted into ChatGPT answers, so it must be readable in a narrow text viewport. Also, ChatGPT chat identity and Codex remediation identity are different operator concepts and should not share the same numbered namespace.

## Template Change

- `chatgpt-card` output wraps long lifecycle/module/task lines.
- The visual card template avoids extra blank lines.
- ChatGPT chat IDs remain `FT-CH-....`.
- Codex remediation/direct work IDs use `FT-CX-....` in `.chatgpt/codex-work-index.yaml`.
- Direct-task bootstrap writes Codex work identity instead of allocating a ChatGPT chat title.
