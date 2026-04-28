# Ранбук для Codex: greenfield-product

## Подтверждение маршрута

- Project preset: `greenfield-product`.
- Recommended mode: `greenfield`.
- Lifecycle: `greenfield-active`.
- Default scenario route: `00-master-router.md -> 04-discovery-new-project.md -> 05-clarify-scope.md -> 06-user-spec-generation.md`.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь предоставляет naming, GitHub access, ChatGPT Project, secrets/approvals. Codex выполняет repo/project work сам.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Дай route receipt или self-handoff по `launch_source`.
2. Прочитай `template-repo/scenario-pack/00-master-router.md` и route files.
3. Создай или открой `/projects/<project-slug>` как canonical root.
4. Запусти `python3 template-repo/scripts/first-project-wizard.py` или repo-native equivalent.
5. Materialize repo-first core и `.chatgpt` dashboard.
6. Создай/обнови `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
7. Создай/подключи GitHub repo через доступный `gh`/connector write path; если доступа нет, documented blocker.
8. Запусти generated project validators и `bash scripts/verify-all.sh quick`.
9. Выполни verified sync при green verify и доступном `origin`.

## Финал

Финальное состояние: `greenfield-product` / `greenfield-active`.
Brownfield artifacts не должны появляться, если проект не проходит adoption/conversion path.
