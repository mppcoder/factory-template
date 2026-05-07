# Factory feedback 056: ChatGPT connector runtime allocation enforcement

Дата: 2026-05-07

Reusable defect: advisory first-answer allocation rules are not enough when ChatGPT cannot execute the repo-local allocator but can write through the GitHub connector.

Factory rule:
- connector fallback must use a connector-safe reservation patch;
- append one item and bump `next_chat_number`;
- include canonical `status_chain`;
- confirm fetch/readback before showing `FT-CH-....`;
- exact allocator blocker is allowed only after a real write or confirm blocker.

Evidence:
- `reports/bugs/2026-05-07-chat-title-allocation-runtime-enforcement-gap.md`
- `tests/chatgpt-first-answer-contract/positive/connector-safe-reservation-patch.md`
