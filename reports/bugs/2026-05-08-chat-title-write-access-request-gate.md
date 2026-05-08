# Bug: ChatGPT write-access request gate skipped before allocator blocker

## Summary

ChatGPT снова показывает exact allocator blocker вместо стабильного `FT-CH-....` title, хотя перед этим должен попытаться сохранить materialized reservation в `.chatgpt/chat-handoff-index.yaml`.

Materialized reservation for this defect: `FT-CH-0029 chat-title-write-access-request-gate`.

## Symptom

Первый ответ ChatGPT снова падает в:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

При этом пользователь явно потребовал не удалять механизм запроса GitHub write-доступа из ChatGPT при присвоении номера.

## Repeated History

Соседние симптомы уже закрывались в `FT-CH-0016`, `FT-CH-0018`, `FT-CH-0020` и `FT-CH-0026`, но текущий UX всё еще может завершиться заглушкой без обязательного structured write-access request gate.

## Root Cause

Правила уже различают no-confirmation и write blocker, но не требуют structured GitHub write-access request gate перед blocker, когда write action not exposed, а platform/connector может запросить write scope.

## User Requirement

Сохранить GitHub write-access request mechanism from ChatGPT для number assignment. Нельзя заменять его Codex-only fallback или свободным conversational confirmation вроде "можно ли использовать GitHub?".

## Expected Behavior

Порядок первого ответа:

1. read router/index;
2. repo-local allocator, если executable;
3. connector write, если exposed;
4. structured write-access request, если needed/possible;
5. retry reservation после grant;
6. exact blocker только если request unavailable/rejected, materialized write failed after request, write action truly absent with no platform request path, write rejected или confirm fetch failed.

## Layer Classification

- Advisory/policy layer: `00-master-router.md`, `15-handoff-to-codex.md`, operator runbooks.
- Executable validation layer: `validate-chatgpt-first-answer-contract.py` and fixtures.
- State layer: `.chatgpt/chat-handoff-index.yaml`, `.chatgpt/handoff-implementation-register.yaml`, dashboard card.

## Remediation Plan

- Add `GitHub write-access request gate` to router/handoff/runbook wording.
- Extend validator markers and fixtures to reject skipped request gate before exact blocker.
- Preserve dry-run title ban and connector-safe materialized reservation requirement.
- Retro-materialize current ChatGPT reservation through Codex because browser ChatGPT had no confirmed repo write action in this environment.
