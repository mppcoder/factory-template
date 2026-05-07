# Factory Feedback: allow codex as task slug word in chat titles

## Исходный bug report
`reports/bugs/2026-05-07-chat-title-codex-slug-false-positive.md`

## Почему это проблема фабрики
The reusable ChatGPT title validator blocked a valid factory-level task about ChatGPT/Codex indexes. Any downstream or template task using `codex` as a domain word in the slug would hit the same allocator false positive.

## Где проявилось
`template-repo/scripts/validate-chat-handoff-index.py` and `template-repo/scripts/allocate-chat-handoff-id.py`.

## Повторяемый паттерн
Status-token validation must distinguish actual lifecycle/status labels from canonical slug words. `codex` is a domain term in this factory, not a title status.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- ChatGPT handoff index validator;
- ChatGPT handoff allocator;
- lifecycle dashboard operator docs;
- project lifecycle smoke tests.

## Как проверить исправление
Run:

```bash
python3 template-repo/scripts/allocate-chat-handoff-id.py \
  --index /tmp/chat-handoff-index.yaml \
  --project-code FT \
  --kind handoff \
  --description "per project unique chatgpt codex indexes"
```

Expected result: allocator writes `FT-CH-.... per-project-unique-chatgpt-codex-indexes`; validation still rejects explicit status/kind title tokens such as `HO OPEN`.
