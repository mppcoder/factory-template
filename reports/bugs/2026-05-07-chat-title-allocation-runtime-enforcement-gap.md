# Bug: ChatGPT first-answer chat title allocation still fails in runtime

Дата: 2026-05-07

## Симптом
Пользователь повторно сообщает, что в первом substantive ответе нового ChatGPT Project task chat не появляется стабильный `FT-CH-.... <task-slug>`. Вместо этого ассистент либо выводит allocator blocker, либо продолжает анализ без materialized reservation.

## Наблюдения repo-first
- `template-repo/scenario-pack/00-master-router.md` уже содержит строгий контракт первого ответа ChatGPT: перед анализом должен быть materialized allocation или exact allocator blocker.
- `.chatgpt/chat-handoff-index.yaml` уже содержит закрытые defect items `FT-CH-0016`, `FT-CH-0018`, `FT-CH-0020`, но после них появились новые correction/open items `FT-CH-0022`, `FT-CH-0023`, `FT-CH-0024` с тем же классом симптомов.
- `template-repo/scripts/allocate-chat-handoff-id.py` корректно реализует repo-local allocation для executor context, но ChatGPT connector context не может исполнять repo-local python allocator.
- `template-repo/scripts/validate-chatgpt-first-answer-contract.py` проверяет текстовые fixtures и router/docs, но не может принудительно заставить ChatGPT runtime выполнить GitHub connector write до первого substantive ответа.

## Root cause
Это не только дефект документации/router. Корневая проблема — enforcement gap между advisory contract и ChatGPT runtime:

1. Router требует materialized repo reservation.
2. Repo-local allocator существует, но в ChatGPT Project connector context не исполняется.
3. GitHub connector fallback описан, но не представлен как machine-checkable pre-answer bootstrap/playbook с минимальным patch/write protocol.
4. Валидатор проверяет наличие правил и fixtures, но не проверяет фактическое состояние текущего ответа/индекса перед ответом ChatGPT.
5. Поэтому ассистент может прочитать `next_chat_number`, увидеть доступный GitHub connector, но не выполнить materialized update и снова показать blocker/analysis.

## Required remediation
Добавить отдельный machine-checkable ChatGPT pre-answer allocation protocol, который ChatGPT обязан выполнять руками через GitHub connector, если repo-local allocator недоступен:

1. Прочитать `00-master-router.md`.
2. Прочитать `.chatgpt/chat-handoff-index.yaml`.
3. Если repo-local allocator недоступен, но GitHub connector write доступен:
   - вычислить `next_chat_number` только из index;
   - сформировать stable slug;
   - обновить `.chatgpt/chat-handoff-index.yaml`: append item + increment `next_chat_number`;
   - выполнить confirm fetch/readback;
   - только после readback вывести stable title.
4. Если update/write невозможен, вывести exact blocker и причину write blocker в evidence/analysis/handoff.
5. Добавить regression fixture/validator для сценария: connector write path available but assistant outputs blocker.
6. Добавить runbook section: “ChatGPT connector-only reservation procedure”.
7. Обновить dashboard/bug/register closeout после verify.

## Suggested artifacts
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scripts/validate-chatgpt-first-answer-contract.py`
- `tests/chatgpt-first-answer-contract/negative/connector-write-available-silent-blocker.md`
- `docs/operator/factory-template/04-chatgpt-project-sources-factory-template-20-cap.md`
- `.chatgpt/chat-handoff-index.yaml`
- `.chatgpt/handoff-implementation-register.yaml`
- `reports/project-status-card.md`

## Acceptance criteria
- New ChatGPT task chat can no longer validly answer with allocator blocker when GitHub connector write is available and confirmed.
- Validator has an explicit negative fixture for this exact repeated runtime gap.
- Runbook has connector-only reservation procedure with precise append + confirm readback steps.
- Dashboard/handoff register shows this defect as open until Codex verifies and closes it.

## Remediation 2026-05-07
- Router, handoff scenario and operator docs now require a connector-safe reservation patch: append one item and bump `next_chat_number`, with canonical `status_chain` and confirm fetch/readback.
- Added positive regression fixture `tests/chatgpt-first-answer-contract/positive/connector-safe-reservation-patch.md`.
- `validate-chatgpt-first-answer-contract.py` now requires connector-safe reservation wording in router, handoff and docs.
- Related connector-created reservations `FT-CH-0023` and `FT-CH-0024` were normalized to the canonical `chatgpt_handoff -> codex_accepted -> codex_completed` chain.
- Verification target: `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .` and `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`.
