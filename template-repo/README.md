# Шаблонный репозиторий фабрики

Универсальный русскоязычный шаблон рабочего проекта.

## Canonical Entry Modes

Этот шаблон рассчитан на 3 канонических режима:

1. Новый проект с нуля
   Используйте greenfield-путь и профиль `greenfield-product`.

2. Перевод на шаблон имеющегося проекта без репо
   Используйте brownfield evidence-first путь и профиль `brownfield-without-repo`.

3. Перевод на шаблон имеющегося проекта с репо
   Используйте brownfield-путь через `brownfield-with-repo-modernization`, `brownfield-with-repo-integration` или `brownfield-with-repo-audit`.

Краткая сводка по этим режимам вынесена в root-level `ENTRY_MODES.md`.
Единая визуальная архитектура шаблона и подробные event workflows описаны в root-level `docs/template-architecture-and-event-workflows.md`.

Legacy aliases старых preset names допускаются только как compatibility input в launcher/scripts и не считаются canonical release-facing naming.

## Repo-First Principle For Generated Projects

Во всех режимах generated project использует один и тот же repo-first принцип:

- сценарии читаются прямо из GitHub repo проекта;
- первое обязательное чтение: `template-repo/scenario-pack/00-master-router.md`;
- entry mode влияет не на набор загружаемых файлов, а на стартовый маршрут и preset/policy.

Для Codex task routing advisory слоя недостаточно:
- `AGENTS`, repo instructions и scenario-pack не переключают модель сами по себе;
- выбор profile/model/reasoning должен происходить на новом task launch через `./scripts/launch-codex-task.sh`.
- если handoff уже подготовлен, сначала выполните launch command, а потом вставляйте handoff в свежий Codex task;
- если виден sticky last-used state, закройте текущую сессию и запустите новый task launch повторно.

## AGENTS For Downstream Repos

- [template-repo/AGENTS.md](/projects/factory-template/template-repo/AGENTS.md) является source-of-truth для downstream/battle repos;
- launcher materializes root `AGENTS.md` в созданном проекте через `scripts/sync-agents.py`;
- root `AGENTS.md` downstream repo должен читаться Codex как repo-first instruction;
- ручные правки в downstream clone запрещены и будут перезаписаны штатным sync/update flow;
- если repo-local путь к scenario-pack отличается, в downstream clone разрешено менять только `SCENARIO_PACK_PATH`.

## Правило фиксации дефектов
Любой обнаруженный defect должен быть зафиксирован как bug report до исправления или одновременно с ним. Silent fixes запрещены.


## Связь версий шаблона и фабрики

Этот шаблон соответствует версии фабрики **2.4.4**.
Сведения о текущем функциональном состоянии шаблона находятся в `CURRENT_FUNCTIONAL_STATE.md`, а изменения фиксируются в `CHANGELOG.md`.
