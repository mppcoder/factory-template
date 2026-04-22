# Factory Feedback: executable task routing and direct self-handoff are missing

## Исходный bug report
`reports/bugs/bug-010-task-routing-stuck-on-static-profile.md`

## Почему это проблема фабрики
Фабрика обещает task-based routing и сценарную дисциплину для Codex, но фактически оставляет выбор модели/режима в advisory слое. Из-за этого downstream-пользователь получает ложное ожидание автоматического переключения внутри одной сессии, а direct task flow без ChatGPT Project не воспроизводит тот же handoff standard.

## Где проявилось
`factory-template`, routing/handoff contour, direct Codex task flow и ChatGPT Project repo-first handoff flow.

## Повторяемый паттерн
- docs/policy обещают routing;
- executable launch boundary не реализован;
- static config/profile принимается за "умный автосвитч";
- direct task bypasses normalized self-handoff and defect-capture discipline.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- scenario-pack
- launcher/router
- template `.codex` layer
- `.chatgpt` / codex-task-pack artifacts
- validators
- runbooks / user guidance

## Как проверить исправление
1. На новой задаче router выбирает named profile и логирует task class / profile / model / reasoning / launch source.
2. В старой сессии docs больше не обещают mid-session auto-switch.
3. ChatGPT handoff и direct task используют один vocabulary и один набор normalized handoff fields.
4. Direct task сначала формирует self-handoff и defect-capture path, а не начинает remediation напрямую.
