# Ранбук для Codex: greenfield-product

Этот runbook начинается после `GF-050`: Codex получает не голое название проекта, а стартовый handoff, сформированный ChatGPT Project шаблона фабрики после scenario-pack опроса.

## Подтверждение маршрута

- Project preset: `greenfield-product`.
- Recommended mode: `greenfield`.
- Lifecycle: `greenfield-active`.
- Input: ChatGPT-generated handoff from factory-template ChatGPT Project intake.
- Default scenario route: `00-master-router.md -> 04-discovery-new-project.md -> 05-clarify-scope.md -> 06-user-spec-generation.md`.

Codex должен вывести handoff receipt. Если handoff уже содержит ответы опроса, не проводить заново весь пользовательский опрос.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь уже прошел factory-template ChatGPT intake, вставил стартовый handoff в Codex, а позже создаст ChatGPT Project боевого проекта и вставит готовую repo-first instruction. Пользователь не создает GitHub repo, не выбирает slug/repo name вручную, не clone-ит repo, не добавляет `origin`, не делает first push, не создает VPS project root, не запускает launcher/wizard/verify.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Принять ChatGPT-generated handoff и вывести handoff receipt.
2. Проверить, что handoff содержит project name, slug proposal или instructions для slug, project type, readiness state, выбранный Codex contour и boundary: GitHub repo/root/verify/sync делает Codex.
3. Прочитать `template-repo/scenario-pack/00-master-router.md` и route files, если handoff указывает дополнительные сценарии.
4. Нормализовать project slug и repo name по правилам factory-template.
5. Проверить GitHub write path через доступный `gh`/connector.
6. Если write path доступен, создать GitHub repo; если нет, documented blocker `github-write-permission-required`.
7. Создать/подготовить VPS project root: `/projects/<project-slug>`.
8. Запустить `python3 template-repo/scripts/first-project-wizard.py` или repo-native launcher/wizard path.
9. Materialize repo-first core: `.chatgpt`, `AGENTS.md`, scenario-pack, dashboard, project-knowledge и базовые project docs.
10. Добавить `origin`, сделать initial commit/push и проверить remote.
11. Создать/обновить `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
12. Запустить bootstrap/setup по generated repo rules.
13. Запустить validators и `bash scripts/verify-all.sh quick`.
14. Выполнить verified sync при green verify и доступном `origin`.
15. Подготовить готовую repo-first instruction для ChatGPT Project боевого проекта.

## Блокеры

Пользователь привлекается только если есть реальный blocker:

- Codex/GitHub connector/`gh` не имеет write permission;
- требуется ручной security approval;
- GitHub UI требует действие, недоступное через tools;
- нужно ввести secret;
- нужно подтвердить платное/опасное внешнее действие;
- нужно создать или изменить ChatGPT Project, потому что это внешний UI.

## Готовая инструкция для боевого ChatGPT Project

Финал Codex должен включить один готовый блок repo-first instruction для пользователя. В нем должны быть:

- GitHub repo URL, созданный Codex;
- project root на VPS;
- `SCENARIO_PACK_PATH=template-repo/scenario-pack`;
- первое обязательное чтение `template-repo/scenario-pack/00-master-router.md`;
- language contract: `Язык ответа Codex: русский. Отвечай пользователю по-русски.`;
- указание, что repo-first source-of-truth находится в созданном repo.

## Финал

Финальное состояние: `greenfield-product` / `greenfield-active`.
Финал должен назвать repo URL, project root, verify result, commit hash / push status и готовую repo-first instruction либо documented blocker.
