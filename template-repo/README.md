# Шаблонный репозиторий фабрики

Универсальный русскоязычный шаблон рабочего проекта.

## Canonical Entry Modes

Этот шаблон рассчитан на 3 канонических режима:

1. Новый проект с нуля
   Используйте greenfield-путь и профиль `product-dev`.

2. Перевод на шаблон имеющегося проекта без репо
   Используйте brownfield evidence-first путь и профиль `brownfield-dogfood-codex-assisted`.

3. Перевод на шаблон имеющегося проекта с репо
   Используйте brownfield-путь через `legacy-modernization`, `integration-project` или `audit-only`.

Краткая сводка по этим режимам вынесена в root-level `ENTRY_MODES.md`.
Единая визуальная архитектура шаблона и подробные event workflows описаны в root-level `docs/template-architecture-and-event-workflows.md`.

## Repo-First Principle For Generated Projects

Во всех режимах generated project использует один и тот же repo-first принцип:

- сценарии читаются прямо из GitHub repo проекта;
- первое обязательное чтение: `template-repo/scenario-pack/00-master-router.md`;
- entry mode влияет не на набор загружаемых файлов, а на стартовый маршрут и preset/policy.

Для Codex task routing advisory слоя недостаточно:
- `AGENTS`, repo instructions и scenario-pack не переключают модель сами по себе;
- выбор profile/model/reasoning должен происходить на новом task launch через `./scripts/launch-codex-task.sh`.

## AGENTS For Downstream Repos

- [template-repo/AGENTS.md](/projects/factory-template/template-repo/AGENTS.md) является source-of-truth для downstream/battle repos;
- launcher materializes root `AGENTS.md` в созданном проекте через `scripts/sync-agents.py`;
- root `AGENTS.md` downstream repo должен читаться Codex как repo-first instruction;
- ручные правки в downstream clone запрещены и будут перезаписаны штатным sync/update flow;
- если repo-local путь к scenario-pack отличается, в downstream clone разрешено менять только `SCENARIO_PACK_PATH`.

## Правило фиксации дефектов
Любой обнаруженный defect должен быть зафиксирован как bug report до исправления или одновременно с ним. Silent fixes запрещены.


## Связь версий шаблона и фабрики

Этот шаблон соответствует версии фабрики **2.4.3**.
Сведения о текущем функциональном состоянии шаблона находятся в `CURRENT_FUNCTIONAL_STATE.md`, а изменения фиксируются в `CHANGELOG.md`.
