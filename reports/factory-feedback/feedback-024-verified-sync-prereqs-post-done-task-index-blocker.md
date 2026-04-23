# Factory Feedback: post-done verified-sync blocker needs clearer deterministic path

## Исходный bug report
`reports/bugs/bug-024-verified-sync-prereqs-post-done-task-index-blocker.md`

## Почему это проблема фабрики
В closeout-контуре canonical sync должен быть предсказуем для оператора. Когда `VALIDATE_VERIFIED_SYNC_PREREQS.sh` hard-blocks post-done non-lightweight diff без заранее очевидного минимального recovery path, это ухудшает UX и вынуждает обходить canonical flow через прямой commit/push.

## Где проявилось
- `template-repo/scripts/validate-verified-sync-prereqs.py`
- `template-repo/scripts/factory_automation_common.py`
- `VERIFIED_SYNC.sh`

## Повторяемый паттерн
- stage уже `done`;
- diff не lightweight;
- task-index не обновлён;
- verified sync блокируется на prereqs;
- оператор завершает через manual git path.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- closeout/sync policy
- verified-sync validator UX
- release-hardening operational path

## Как проверить исправление
1. Смоделировать post-done non-lightweight diff без обновлённого task-index.
2. Запустить `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`.
3. Убедиться, что оператор получает либо:
   - более ясный deterministic recovery path, либо
   - менее хрупкий canonical sync gate при явном commit/push intent.
4. Проверить, что guardrails против stale metadata не деградируют.

## Статус
зафиксировано
