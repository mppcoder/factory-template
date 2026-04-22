# Codex workflow для этого проекта

## Базовый режим
- дефолт: `gpt-5.4`, reasoning `medium`
- для тяжёлого brownfield RCA: подагент `brownfield_reviewer`
- для быстрого inventory/evidence: подагент `inventory_explorer`
- для рутинных правок после фиксации плана: подагент `repo_worker`
- для финальной упаковки clean package: подагент `release_packager`

## Когда переключаться из hybrid в codex-led
Переключение допустимо только после того, как:
- собран минимальный evidence pack;
- заполнены `reality-check.md`, `evidence-register.md`, `reverse-engineering-summary.md`;
- определены safe zones и rollback plan;
- handoff в Codex больше не противоречит policy preset.

## Внешние boundary-действия
Эти действия остаются за оператором:
- создание новых GitHub repos;
- подключение репозиториев и app sources в ChatGPT Projects;
- загрузка архивов в `/projects/<project-root>/_incoming/`;
- ввод секретов и работа с внешними UI.
