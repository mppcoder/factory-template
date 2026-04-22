# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
quick

## Task class evidence
- keyword hit: docs
- keyword hit: найти

## Selected profile
quick

## Selected model
gpt-5.4-mini

## Selected reasoning effort
low

## Selected plan mode reasoning
medium

## Project profile
unknown-project-profile

## Selected scenario
00-master-router.md

## Pipeline stage
done

## Artifacts to update
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

## Handoff allowed
yes (forbidden)

## Defect capture path
not-required-by-text-signal

## Launch boundary rule
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Executable launch command
`codex --profile quick`

## Task payload
# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно внедрить каноническое правило хранения repo-папок на VPS.
- В `/projects` должны лежать только project roots.
- `_incoming` допускается только внутри project root.
- brownfield temporary, intermediate и reconstructed repo должны жить только внутри `/projects/<project-root>/...`.

## Что должен сделать исполнитель
- Найти repo-файлы, где допускается плоская раскладка под `/projects`.
- Обновить scenario-pack, runbooks, examples, workspace/bootstrap docs и boundary templates.
- Исправить scripts/templates, если они обещают или генерируют плоский layout.
- Подготовить completion package по обновлению factory sources и downstream контуров.

## Ограничения
- Не вводить отдельную плоскую зону для brownfield temp repos.
- Сохранить совместимость внутреннего нейминга подпапок, если верхнеуровневое правило `/projects` соблюдено.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.