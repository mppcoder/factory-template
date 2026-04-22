# Task pack для Codex

## Change ID
chg-20260422-003

## Заголовок
Respect explicit reasoning in structured Codex handoff

## Класс изменения
small-fix

## Режим выполнения
single-pass

## Launch source
chatgpt-handoff

## Task class
build

## Selected profile
build

## Selected model
gpt-5.4

## Selected reasoning effort
medium

## Selected plan mode reasoning
medium

## Project profile
unknown-project-profile

## Selected scenario
00-master-router.md

## Pipeline stage
done

## Handoff allowed
yes (forbidden)

## Defect capture path
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Handoff input
# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно устранить bug в executable routing layer.
- Structured handoff мог явно просить `selected_reasoning_effort: high`, но generated `.chatgpt` artifacts фиксировали `medium`.
- Причина: router уважал keyword fallback сильнее, чем explicit handoff routing fields.

## Что должен сделать исполнитель
- Зафиксировать bug report и factory feedback для reusable routing defect.
- Обновить `template-repo/scripts/codex_task_router.py`, чтобы он читал structured handoff поля и подбирал совместимый executable profile по model/reasoning.
- Сохранить keyword fallback только как запасной путь, а не как override поверх explicit handoff.
- Подтвердить reproduce path до и после исправления.

## Ограничения
- Не делать вид, что уже открытая сессия auto-switches reasoning без нового launch boundary.
- Если requested profile из handoff не существует в routing spec, нужно подобрать совместимый executable profile и явно зафиксировать это в reasons.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.

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
