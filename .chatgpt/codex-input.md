# Codex handoff input

## Контекст
- Repo: `factory-template`
- Проведен генеральный audit проекта на целостность, полноту и соответствие.
- Главный реальный defect найден в `template-repo/scripts/check-dod.py`: validator наследовал `origin` родительского git repo для nested example fixtures и выдавал false positive по `verified-sync-report`.

## Что должен сделать исполнитель
- Зафиксировать reusable defect и factory feedback.
- Исправить `check-dod.py`, чтобы remote-проверка срабатывала только когда проверяемый путь сам является git repo root.
- Подтвердить исправление полным suite:
  - `EXAMPLES_TEST.sh`
  - `MATRIX_TEST.sh`
  - `SMOKE_TEST.sh`
  - `VALIDATE_FACTORY_TEMPLATE_OPS.sh`
  - `PRE_RELEASE_AUDIT.sh`

## Ограничения
- Не маскировать проблему под правку example fixtures.
- Не ослаблять verified-sync guard для реальных рабочих repo.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
