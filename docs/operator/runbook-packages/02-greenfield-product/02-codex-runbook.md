# Ранбук для Codex: greenfield-product

## Подтверждение маршрута

- Project preset: `greenfield-product`.
- Recommended mode: `greenfield`.
- Lifecycle: `greenfield-active`.
- Default scenario route: `00-master-router.md -> 04-discovery-new-project.md -> 05-clarify-scope.md -> 06-user-spec-generation.md`.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Не проси пользователя вручную создавать project files, запускать wizard, clone, verify или push, если remote shell и GitHub write path доступны. Пользователь нужен только для external UI, secrets, approvals или отсутствующего доступа.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Прочитай `template-repo/scenario-pack/00-master-router.md`.
2. Проверь `.chatgpt/project-profile.yaml` и `.chatgpt/stage-state.yaml`, если project root уже materialized.
3. Если задача пришла как direct task, сначала покажи self-handoff.
4. Если задача пришла как ChatGPT handoff, дай route receipt и исполняй исходный handoff.
5. Создай или обнови `/projects/<project-slug>` как canonical root.
6. Запусти `python3 template-repo/scripts/first-project-wizard.py` или repo-native equivalent для scaffold/materialization.
7. Создай/обнови `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
8. Поддерживай project-owned product code отдельно от template-owned safe/generated zones.
9. Для больших задач используй parent handoff и repo-native orchestration; user actions переносить в final closeout.
10. Запусти verify и, если доступно, verified sync.

## Финал

Финальное состояние боевого проекта остается `greenfield-product`.
Brownfield artifacts не должны появляться, если проект не проходит adoption/conversion path.
