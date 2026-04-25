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
- для интерактивной работы в VS Code Codex extension используйте `manual-ui (default)`: откройте новый чат/окно Codex, вручную выберите model/reasoning в picker и затем вставьте handoff;
- launcher-first path через `./scripts/launch-codex-task.sh` остается optional strict mode для automation, reproducibility и shell-driven launch;
- новый чат + вставка handoff и новый task launch через launcher — не одно и то же;
- уже открытая live session не является надежным auto-switch механизмом;
- если виден sticky last-used state, закройте текущую сессию, откройте новую и при необходимости используйте strict launch path.

## Model availability auto-check

Executable model mapping хранится в `codex-model-routing.yaml`: task class выбирает `selected_profile`, а profile выбирает `selected_model`, `selected_reasoning_effort` и `selected_plan_mode_reasoning_effort`. `codex-routing.yaml` продолжает описывать общий routing contract и task-class keywords; resolver объединяет оба файла перед генерацией `.chatgpt/task-launch.yaml`.

Live Codex catalog проверяется отдельно:

```bash
python3 scripts/check-codex-model-catalog.py .
python3 scripts/check-codex-model-catalog.py . --json
python3 scripts/check-codex-model-catalog.py . --write-proposal
```

Если `codex debug models` недоступен, checker и validator должны честно предупредить и не продвигать mapping автоматически. `--apply-safe` разрешает только безопасное обновление snapshot metadata catalog; смена model для существующего profile остается proposal-only и требует ручного review.

Troubleshooting:
- new model appears in live Codex catalog but not in routing file: run `scripts/check-codex-model-catalog.py --write-proposal`, review `reports/model-routing/model-routing-proposal.md`, then update `codex-model-routing.yaml` and named profiles intentionally;
- configured model disappears: treat selected_model as repo-configured only until live validation passes; in strict automation run validator with `--strict`;
- reasoning level unsupported: update profile reasoning or model choice before producing a confident handoff;
- VS Code picker keeps a sticky model: open a new chat/window and manually verify picker state;
- user pasted handoff into already-open session: mark it non-canonical fallback, because advisory text does not switch model/profile/reasoning.

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
