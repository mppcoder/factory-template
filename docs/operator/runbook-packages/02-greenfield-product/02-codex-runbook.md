# Ранбук для Codex: greenfield-product

## Маршрут

- Project preset: `greenfield-product`.
- Recommended mode: `greenfield`.
- Lifecycle: `greenfield-active`.
- Default scenario route: `00-master-router.md -> 04-discovery-new-project.md -> 05-clarify-scope.md -> 06-user-spec-generation.md`.

## Старт

1. Прочитай `template-repo/scenario-pack/00-master-router.md`.
2. Проверь `.chatgpt/project-profile.yaml` и `.chatgpt/stage-state.yaml`.
3. Если задача пришла как direct task, сначала покажи self-handoff.
4. Если задача пришла как ChatGPT handoff, дай route receipt и исполняй исходный handoff.

## Реализация

- Создай/обнови `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
- Поддерживай project-owned product code отдельно от template-owned safe/generated zones.
- Для больших задач используй parent handoff и repo-native orchestration; user actions переносить в final closeout.

## Финал

Финальное состояние боевого проекта остается `greenfield-product`.
Brownfield artifacts не должны появляться, если проект не проходит adoption/conversion path.
