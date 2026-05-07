# Позитивный fixture: connector-safe-reservation-patch

repo_write_path: github_connector_available
repo_local_allocator: unavailable_in_chatgpt_connector_context
connector_update_mode: connector-safe reservation patch
connector_patch_scope: append one item and bump `next_chat_number`
confirm_fetch: materialized_item_present

## Название чата для копирования
```text
FT-CH-1236 connector-safe-reservation-patch
```

## Карточка проекта
🏭 factory-template | phase: test | gates: green

Route Receipt

GitHub connector write path used a connector-safe reservation patch: append one item and bump `next_chat_number`, then confirm fetch verified the materialized item before the stable title was shown.
