# Release Note Template

## Release

- Версия: 2.4.2
- Дата: 2026-04-20
- Статус: published

## Что вошло

- repo-first instruction mode добавлен как канонический режим для ChatGPT Project
- export/reference packs переведены в вспомогательный слой, а не основной daily workflow
- release-facing docs и bundle metadata синхронизированы под `factory-v2.4.2`

## Что изменилось в template/runtime/policy layer

- launcher и generated versioning layer переведены на `2.4.2`
- export/validation layer выровнены под declarative pack profiles
- release checklist, release notes и boundary guidance отражают repo-first workflow
- verified sync и release publication остаются раздельными контурами

## Что проверено

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh && bash PRE_RELEASE_AUDIT.sh`

## Что важно для downstream

- для steady-state работы использовать GitHub repo как source of truth, а `sources-pack-core-20.tar.gz` держать как reference/export bundle
- для release-facing прохода использовать `sources-pack-release-20.tar.gz`
- generated projects теперь получают фабричную версию `2.4.2`
- verified sync после green verify может выполняться автоматически, но auto release требует отдельного `release-decision.yaml`

## Риски и ограничения

- quality validation остаётся эвристической, а не семантической
- phase detection по-прежнему rule-based и зависит от changed paths и document signals

## Внешние шаги для пользователя

- при `decision=release` проверить, доступна ли автоматическая публикация через `gh`
- если runtime перешел в fallback, использовать release report и затем синхронизировать GitHub tag/release вручную
- прикрепить к GitHub Release архив `factory-v2.4.2.zip`
- обновить repo-first инструкцию в ChatGPT Project, если поменялись repo/path/обязательные правила чтения сценариев

## Go / No-Go

- Решение: Go
- Комментарий: release-facing слой синхронизирован, verify-контур пройден, bundle собирается корректно
