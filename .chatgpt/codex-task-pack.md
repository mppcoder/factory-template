# Task pack для Codex

## Идентификатор изменения
chg-20260423-021

## Заголовок
Default factory-template ChatGPT Project to no unless instruction contract changed

## Класс изменения
small-fix

## Режим выполнения
codex-led

## Источник запуска
chatgpt-handoff

## Класс задачи
deep

## Выбранный профиль
deep

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
high

## Выбранное reasoning effort для plan mode
high

## Статус model catalog
available

## Примечание по live availability
selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check

## Режим применения
manual-ui

## Строгий режим запуска
optional

## Ручной UI по умолчанию
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=high` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Язык ответа Codex
Русский. Codex должен отвечать пользователю по-русски; английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Опциональная команда строгого запуска
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Прямая команда Codex за launcher
codex --profile deep

## Профиль проекта
unknown-project-profile

## Выбранный сценарий
00-master-router.md

## Этап pipeline
done

## Разрешение handoff
yes (forbidden)

## Маршрут defect-capture
not-required-by-text-signal

## Приоритет правил repo
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Входные данные handoff
audit: проверить repo на остаточный английский человекочитаемый слой

## Обязательное правило фиксации дефектов
Если в ходе анализа, реализации, тестирования, reverse engineering или verification обнаружен дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure, его нельзя silently patch.

Нужно:
1. создать или обновить bug report в `reports/bugs/`;
2. собрать evidence и шаги воспроизведения;
3. указать слой дефекта: `project-only`, `factory-template` или `shared/unknown`;
4. определить, исправляется ли дефект в текущем scope или требует отдельного task boundary;
5. выполнить self-handoff для нового defect;
6. при необходимости подготовить ChatGPT handoff bug note или deep-research prompt;
7. если проблема reusable — создать или обновить factory feedback в `reports/factory-feedback/` или `meta-feedback/`;
8. только после этого или одновременно с этим делать fix.
