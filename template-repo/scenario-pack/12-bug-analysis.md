# Анализ бага

## Обязательный порядок шагов
1. Воспроизвести проблему.
2. Собрать evidence.
3. Создать bug report.
4. Классифицировать слой дефекта.
5. Определить, исправляется ли defect в текущем scope или требует отдельной задачи.
6. Выполнить self-handoff для defect как для отдельного task boundary.
7. Если нужен deep research, подготовить ChatGPT research-ready bug report/prompt вместо слабой remediation попытки.
8. При необходимости подготовить ChatGPT handoff bug note.
9. Если defect reusable — подготовить factory feedback.
10. Создать Codex fix task или явно отложить его через новый handoff.
11. Провести verification.
12. Если defect reusable — подготовить sync back в фабрику.

## Incidental defect rule
Если defect найден по пути исполнения другой основной задачи:
- нельзя считать его автоматически включенным в уже открытый live route;
- bug report обязан явно отметить, что defect incidental, fixed-in-scope или unresolved;
- self-handoff обязан определить, допустимо ли remediation продолжать в текущем scope, или нужен отдельный task launch;
- если route совпадает с текущим, можно продолжать в том же chat только после явного self-handoff;
- если route меняется по profile/model/reasoning, канонический путь — новый task launch / новая Codex chat-сессия через явный launch command и copy-paste handoff;
- продолжение в текущем chat допускается только как fallback с явной пометкой, что auto-switch в уже открытой сессии ненадежен.

## Канонический маршрут defect-flow
1. reproduce
2. collect evidence
3. create bug report
4. classify defect layer
5. decide current-scope vs separate-task
6. run self-handoff for the defect
7. if deep research needed create ChatGPT research-ready bug report/prompt
8. if reusable create factory feedback
9. if needed create ChatGPT bug handoff
10. create Codex task
11. verify
12. sync reusable change back
