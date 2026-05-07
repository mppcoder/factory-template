# Task pack для Codex

## Идентификатор изменения
<!-- Укажите change.id -->

## Заголовок
<!-- Короткий заголовок задачи -->

## Класс изменения
<!-- small-fix / feature / refactor / migration / brownfield-audit -->

## Режим выполнения
<!-- manual / hybrid / codex-led -->

## Источник запуска
<!-- chatgpt-handoff / direct-task -->

## Класс задачи
<!-- quick / build / deep / review -->

## Выбранный профиль
<!-- quick / build / deep / review -->

## Выбранная модель
<!-- например gpt-5.4 -->

## Выбранное reasoning effort
<!-- low / medium / high -->

## Выбранное reasoning effort для plan mode
<!-- low / medium / high / xhigh -->

## Статус model catalog
<!-- repo-configured / available / unavailable; live validation comes from codex debug models -->

## Режим применения
<!-- manual-ui -->

## Строгий режим запуска
<!-- optional -->

## Ручной UI по умолчанию
<!-- новый чат/окно, ручной выбор model/reasoning в picker, затем вставка handoff -->

## Язык ответа Codex
Русский. Codex должен отвечать пользователю по-русски; английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Опциональная команда строгого запуска
<!-- launch command only when needed for strict routing -->

## Прямая команда Codex за launcher
<!-- codex --profile <profile> -->

## Профиль проекта
<!-- из .chatgpt/project-profile.yaml -->

## Выбранный сценарий
<!-- активный сценарий -->

## Этап pipeline
<!-- текущий этап -->

## Разрешение handoff
<!-- yes/no + policy -->

## Маршрут defect-capture
<!-- defect path или not-required -->

## Приоритет правил repo
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.

## Базовый prompt contract для GPT-5.5
<!-- Не считать GPT-5.5 drop-in replacement. Начинайте prompt-like task pack с outcome, success criteria, constraints, evidence requirements, output shape и stop rules. Подробную процессность оставляйте только для обязательных repo invariants. -->

## Входные данные handoff
<!-- Сведите сюда ключевой handoff input. Стабильные правила должны идти выше dynamic task fields. Человекочитаемый текст должен быть на русском; technical literal values можно не переводить. -->
