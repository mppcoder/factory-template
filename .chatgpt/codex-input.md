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
