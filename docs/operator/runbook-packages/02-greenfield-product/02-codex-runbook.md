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
Пользователь уже прошел factory-template ChatGPT intake, вставил стартовый handoff в Codex, а позже создаст ChatGPT Project боевого проекта в UI, откроет Project settings/instructions, вставит готовую repo-first instruction и сохранит настройки. Пользователь не создает GitHub repo, не выбирает slug/repo name вручную, не clone-ит repo, не добавляет `origin`, не делает first push, не создает VPS project root, не запускает launcher/wizard/verify.

Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст. Codex не создает ChatGPT Project, не вставляет instruction и не сохраняет Project settings через browser/desktop UI automation как canonical path для новичка.

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
10. Materialize controlled software update governance artifacts: `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml`, `reports/software-updates/README.md`.
11. Зафиксировать Ubuntu/VPS baseline: selected Ubuntu LTS release, provider image id если доступен, OS image release отдельно от later package update state, kernel, package manager sources, `unattended-upgrades`, Docker/Compose, Node/Python, GitHub Actions, base Docker images/tags/digests, lockfiles и critical runtime dependencies.
12. Проверить `unattended-upgrades`; auto-install без approval запрещен. Записать policy `manual-approved-upgrade` и readiness без выполнения upgrade.
13. Создать watchlist и update readiness; переход на новую Ubuntu LTS оформить только как отдельный migration/upgrade project.
14. Добавить `origin`, сделать initial commit/push и проверить remote.
15. Создать/обновить `greenfield/vision.md`, `greenfield/problem-statement.md`, `greenfield/scope-v1.md`, `greenfield/architecture-options.md`, `greenfield/initial-task-list.md`.
16. Запустить bootstrap/setup по generated repo rules.
17. Запустить validators и `bash scripts/verify-all.sh quick`, включая `python3 scripts/validate-software-update-governance.py .`.
18. Выполнить verified sync при green verify и доступном `origin`.
19. Подготовить готовый текст repo-first instruction для ChatGPT Project боевого проекта.
20. Подготовить пошаговую инструкцию пользователю, куда этот текст вставить в ChatGPT UI: создать Project, открыть Project settings/instructions, вставить текст, сохранить настройки.

## Блокеры

Пользователь привлекается только если есть реальный blocker:

- Codex/GitHub connector/`gh` не имеет write permission;
- требуется ручной security approval;
- GitHub UI требует действие, недоступное через tools;
- нужно ввести secret;
- нужно approve upgrade proposal или OS/runtime migration;
- нужно подтвердить платное/опасное внешнее действие;
- нужно создать или изменить ChatGPT Project, потому что это внешний UI, который выполняет пользователь.

## Готовая инструкция для боевого ChatGPT Project

Финал Codex должен включить один готовый блок repo-first instruction для пользователя. В нем должны быть:

- GitHub repo URL, созданный Codex;
- project root на VPS;
- `SCENARIO_PACK_PATH=template-repo/scenario-pack`;
- первое обязательное чтение `template-repo/scenario-pack/00-master-router.md`;
- language contract: `Язык ответа Codex: русский. Отвечай пользователю по-русски.`;
- указание, что repo-first source-of-truth находится в созданном repo.

После блока instruction финал Codex должен дать короткую UI-инструкцию пользователю:

```text
1. В ChatGPT создать Project боевого проекта.
2. Открыть Project settings/instructions.
3. Вставить готовую repo-first instruction из этого ответа.
4. Сохранить настройки.
```

## Финал

Финальное состояние: `greenfield-product` / `greenfield-active`.
Финал должен назвать repo URL, project root, verify result, commit hash / push status, готовую repo-first instruction и пошаговую инструкцию пользователю для ChatGPT Project UI либо documented blocker.
