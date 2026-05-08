# Отчет о дефекте

## Идентификатор
bug-039-downstream-closeout-card-used-template-dashboard

## Краткий заголовок
Greenfield/downstream closeout показал карточку `factory-template` вместо карточки созданного проекта.

## Где найдено

Repo: `factory-template`

Слои:
- direct-task closeout;
- project lifecycle dashboard renderer;
- generated `.chatgpt/direct-task-response.md`;
- greenfield/downstream completion evidence.

## Шаги воспроизведения

1. Создать greenfield project через guided launcher.
2. Продолжить downstream work до финального closeout.
3. Сгенерировать финальную карточку командой из generated direct-task completion rule.
4. Получить карточку `factory-template`, хотя scope closeout относится к созданному downstream repo.

## Ожидаемое поведение

- Если closeout относится к `factory-template`, карточка берется из template lifecycle dashboard.
- Если closeout относится к созданному greenfield/downstream project, карточка берется из repo-local downstream dashboard: `.chatgpt/project-lifecycle-dashboard.yaml`.
- Если оба dashboard доступны, repo-local downstream dashboard имеет приоритет для downstream root.

## Фактическое поведение

- Completion rule hardcoded only the factory-template command:
  `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`
- `render_project_card_for_codex_response` tried template dashboard before repo-local generated dashboard.
- Финальный ответ по Health Sync Bridge показал карточку `factory-template`.

## Evidence

- [REAL] Follow-up пользователя: "почему опять остановился? и почему если мы делаем новый проект карточку проекта открываешь шаблона?"
- [PROJECT] `/projects/health-sync-bridge/.chatgpt/project-lifecycle-dashboard.yaml` exists and renders `Health Sync Bridge`.
- [PROJECT] Previous generated completion rule in `.chatgpt/direct-task-response.md` named only the template dashboard command.
- [PROJECT] `template-repo/scripts/codex_task_router.py` candidate order preferred template dashboard before repo-local dashboard.

## Классификация слоя

`factory-template`

## Нужен ли feedback в фабрику

Да. Это reusable process defect in generated closeout instructions and renderer candidate order.

## Исправление

- `render_project_card_for_codex_response` now prefers repo-local generated project renderer/dashboard before template dashboard.
- Direct-task completion rule now explicitly says to use downstream/greenfield repo-local equivalent for downstream closeout.
- Codex task-pack checklist now distinguishes factory-template and downstream project-card commands.
- `validate-codex-routing.py` requires downstream/greenfield closeout card wording.
- `verify-all.sh quick` includes `downstream-project-card-selection-smoke`, which fails if a template card leaks when both dashboards exist.

## Статус

исправлено в `FT-CX-0036 fix-downstream-closeout-card`
