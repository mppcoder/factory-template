# Отчет о дефекте

## Идентификатор
bug-032-chatgpt-handoff-language-contract-gap

## Краткий заголовок
ChatGPT-generated handoff может приходить на английском, хотя repo требует русский человекочитаемый слой.

## Тип дефекта
reusable-process-defect

## Где найдено
- Внешний handoff от ChatGPT в Codex.
- `.chatgpt/codex-input.md`.
- Нормализованные handoff/task-pack artifacts, если они принимают англоязычный input без отдельной диагностики.

## Шаги воспроизведения
1. ChatGPT формирует handoff для `factory-template`.
2. Handoff содержит англоязычные человекочитаемые разделы вроде `Goal`, `Hard constraints`, `Required implementation`, `Verification commands`, `Completion requirements`.
3. Codex принимает этот handoff как task input.
4. Repo validators проверяют структуру и routing, но не останавливают англоязычный upstream handoff как language-contract defect.

## Ожидаемое поведение
- ChatGPT-generated handoff для `factory-template` должен быть русскоязычным в человекочитаемом слое.
- Технические literal values, model IDs, команды, имена файлов, YAML keys и route fields могут оставаться на английском.
- Если входящий handoff содержит англоязычные prose-разделы, validator должен явно указать, что нарушен language contract.

## Фактическое поведение
- Upstream handoff был на английском.
- Codex-side closeout был исправлен, но upstream handoff language не был закрыт отдельным правилом и validator-ом.

## Evidence
- [REAL] Пользовательский сигнал: "а почему хэндоф который сделал чатгпт на английском?"
- [PROJECT] `.chatgpt/codex-input.md` является входным handoff artifact и до исправления не имел language-contract validator.
- [PROJECT] `scenario-pack/15-handoff-to-codex.md` требовал русский язык для handoff, но проверка не была executable.

## Слой дефекта
factory-template

## Классификация failing layer
upstream handoff source / language contract / validator gap

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Решение / статус
fixed
