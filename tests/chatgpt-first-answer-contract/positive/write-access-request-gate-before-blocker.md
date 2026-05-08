# Позитивный fixture: write-access-request-gate-before-blocker

repo_local_allocator: unavailable_in_chatgpt_connector_context
write_action: not_exposed
write_access_request_possible: true
GitHub write-access request gate: structured write-access request is not a conversational confirmation.
write_access_request_attempted: true
write_access_request_result: rejected
allocator_blocker_reason: request unavailable/rejected

## Название чата для копирования
```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

## Карточка проекта
🏭 factory-template | phase: test | gates: blocked

Route Receipt

The assistant made a structured write-access request for `.chatgpt/chat-handoff-index.yaml`; the request unavailable/rejected result was explicit. After rejection, ChatGPT prepared a Codex retro-materialization handoff with `launch_source: chatgpt-handoff` so Codex can retro-materialize ChatGPT reservation before remediation.
