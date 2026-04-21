# Политика обработки дефектов

## Главное правило
Любой обнаруженный дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или повторяемый process failure должен быть зафиксирован как структурированный bug report до исправления или одновременно с ним.

## Silent fixes запрещены
Нельзя молча исправлять найденный дефект без артефакта фиксации.

## Обязательные шаги
1. Воспроизвести проблему или зафиксировать наблюдение.
2. Собрать evidence.
3. Создать или обновить bug report.
4. Классифицировать слой дефекта:
   - `project-only`
   - `factory-template`
   - `shared/unknown`
5. Если нужен дополнительный анализ, подготовить ChatGPT handoff bug note.
6. Если дефект reusable или есть подозрение на factory issue, создать factory feedback.
7. Только после этого переходить к fix / remediation / handoff в Codex.

## Правило remediation handoff
Если после defect-capture обязательные gate'ы уже закрыты, артефакты достаточны и задача достаточно определена, remediation-ответ должен содержать готовый inline handoff в Codex в том же ответе.

Если после remediation, verify или push остается внутренний release-followup / closeout-sync / release-facing consistency work внутри repo, это тоже считается handoff-worthy внутренним этапом. В таком случае нельзя завершать ответ user-only closeout'ом.
