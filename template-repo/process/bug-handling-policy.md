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
5. Определить, укладывается ли remediation в текущий scope или нужен отдельный task boundary.
6. Выполнить self-handoff для этого defect.
7. Если нужен дополнительный анализ, подготовить ChatGPT handoff bug note или research-ready bug prompt.
8. Если дефект reusable или есть подозрение на factory issue, создать factory feedback.
9. Только после этого переходить к fix / remediation / handoff в Codex.

## Правило incidental defect
Если defect найден incidental во время выполнения другой задачи и не исправляется в том же scope:
- bug report обязателен;
- self-handoff обязателен;
- если новый route отличается по profile/model/reasoning, канонический путь — новый task launch через явный launch command;
- продолжение в текущей live-сессии допускается только как явно помеченный fallback;
- нельзя делать вид, что advisory rules автоматически переключили уже открытую сессию;
- если без исследования remediation ненадежен, вместо фикса подготовь ChatGPT-ready deep research prompt.

## Правило remediation handoff
Если после defect-capture обязательные gate'ы уже закрыты, артефакты достаточны и задача достаточно определена, remediation-ответ должен содержать готовый inline handoff в Codex в том же ответе.

Если после remediation, verify или push остается внутренний release-followup / closeout-sync / release-facing consistency work внутри repo, это тоже считается handoff-worthy внутренним этапом. В таком случае нельзя завершать ответ user-only closeout'ом.
