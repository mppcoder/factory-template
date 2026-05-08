# Factory Feedback 063: ChatGPT write-access request gate before allocator blocker

## Source

- Chat: `FT-CH-0029 chat-title-write-access-request-gate`
- Bug report: `reports/bugs/2026-05-08-chat-title-write-access-request-gate.md`

## Feedback

The first-answer allocation contract needs an explicit middle gate between "write action not exposed" and the exact allocator blocker. If the platform or connector can request write scope, ChatGPT must initiate the structured GitHub write-access request for `.chatgpt/chat-handoff-index.yaml`, retry connector-safe reservation after grant, and only then return the exact allocator blocker when the request is unavailable, rejected, or the confirmed write/readback fails.

## Why It Matters

Without this gate, the system preserves "do not ask vague GitHub confirmation" but still loses the user-visible path that requests GitHub write access from ChatGPT. That makes the recurring blocker look fixed in policy while the actual UX still falls through.

## Required Factory Change

- Preserve the GitHub write-access request mechanism from ChatGPT.
- Mark structured write-access request as not a conversational confirmation.
- Validate `write_access_request_attempted` or an explicit request unavailable/rejected blocker before accepting the exact allocator blocker.
- Keep dry-run `FT-CH` titles invalid.
