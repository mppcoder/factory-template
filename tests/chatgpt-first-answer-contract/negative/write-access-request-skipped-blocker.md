# Негативный fixture: write-access-request-skipped-blocker

repo_local_allocator: unavailable_in_chatgpt_connector_context
write_action: not_exposed
write_access_request_possible: true
write_auth_blocker: write action not exposed

## Название чата для копирования
```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

## Карточка проекта
🏭 factory-template | phase: test | gates: blocked

Route Receipt

Assistant returned the exact allocator blocker after seeing a possible write-access request path, but skipped `write_access_request_attempted`.
