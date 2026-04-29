# Ранбук для Codex: greenfield-product

Этот runbook начинается после `GF-010`: пользователь сообщил название проекта и optional идею. ChatGPT Project UI остается внешним действием пользователя, но GitHub/VPS/repo/bootstrap/verify/sync делает Codex.

## Подтверждение маршрута

- Project preset: `greenfield-product`.
- Recommended mode: `greenfield`.
- Lifecycle: `greenfield-active`.
- Default scenario route: `00-master-router.md -> 04-discovery-new-project.md -> 05-clarify-scope.md -> 06-user-spec-generation.md`.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь выбирает название проекта, сообщает его Codex, создает ChatGPT Project в UI и вставляет готовую repo-first инструкцию. Пользователь не создает GitHub repo, не clone-ит repo, не добавляет `origin`, не делает first push, не запускает launcher/wizard/verify.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Дай route receipt или self-handoff по `launch_source`.
2. Прочитай `template-repo/scenario-pack/00-master-router.md` и route files.
3. Нормализуй project slug и repo name из `<PROJECT_NAME>` по правилам factory-template.
4. Проверь GitHub write path через доступный `gh`/connector.
5. Если write path доступен, создай GitHub repo сам; если нет, documented blocker `github-write-permission-required`.
6. Создай project root на VPS: `/projects/<project-slug>`.
7. Запусти `python3 template-repo/scripts/first-project-wizard.py` или repo-native launcher/wizard path.
8. Materialize repo-first core: `.chatgpt`, `AGENTS.md`, scenario-pack, dashboard, project-knowledge и базовые project docs.
9. Добавь `origin`, сделай initial commit/push и проверь remote.
10. Создай/обнови `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
11. Запусти bootstrap/setup по generated repo rules.
12. Запусти validators и `bash scripts/verify-all.sh quick`.
13. Выполни verified sync при green verify и доступном `origin`.
14. Подготовь готовый repo-first instruction text для вставки пользователем в ChatGPT Project.

## Блокеры

Пользователь привлекается только если есть реальный blocker:

- Codex/GitHub connector/`gh` не имеет write permission;
- требуется ручной security approval;
- GitHub UI требует действие, недоступное через tools;
- нужно ввести secret;
- нужно подтвердить платное/опасное внешнее действие;
- нужно создать или изменить ChatGPT Project, потому что это внешний UI.

## Готовый текст для ChatGPT Project

Финал Codex должен включить один готовый блок инструкции для пользователя. В нем должны быть:

- GitHub repo URL, созданный Codex;
- project root на VPS;
- `SCENARIO_PACK_PATH=template-repo/scenario-pack`;
- первое обязательное чтение `template-repo/scenario-pack/00-master-router.md`;
- language contract: `Язык ответа Codex: русский. Отвечай пользователю по-русски.`;
- указание, что repo-first source-of-truth находится в созданном repo.

## Финал

Финальное состояние: `greenfield-product` / `greenfield-active`.
Финал должен назвать repo URL, project root, verify result, commit hash / push status и готовый instruction text либо documented blocker.
