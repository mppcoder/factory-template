# Release Note Template

## Release

- Версия: 2.4.2
- Дата: 2026-04-20
- Статус: published

## Что вошло

- direct Sources profile `core-hot-15` добавлен как официальный daily profile для ChatGPT Project
- в релиз вошла hybrid-модель `direct hot-set + canonical archive`
- release-facing docs и bundle metadata синхронизированы под `factory-v2.4.2`

## Что изменилось в template/runtime/policy layer

- launcher и generated versioning layer переведены на `2.4.2`
- export/validation layer выровнены под declarative Sources profiles
- release checklist, release notes и boundary guidance отражают hybrid-схему Sources
- verified sync и release publication остаются раздельными контурами

## Что проверено

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh && bash PRE_RELEASE_AUDIT.sh`

## Что важно для downstream

- для steady-state работы использовать `sources-pack-core-20.tar.gz`
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
- загрузить нужный curated Sources pack в ChatGPT Project

## Go / No-Go

- Решение: Go
- Комментарий: release-facing слой синхронизирован, verify-контур пройден, bundle собирается корректно
