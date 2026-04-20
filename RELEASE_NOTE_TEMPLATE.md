# Release Note Template

## Release

- Версия: 2.4.1
- Дата: 2026-04-20
- Статус: published

## Что вошло

- бывший `Unreleased` оформлен как официальный patch-релиз `2.4.1`
- в релиз вошли ops-policy, phase detection и curated Sources packs
- release-facing docs и bundle metadata синхронизированы под `factory-v2.4.1`

## Что изменилось в template/runtime/policy layer

- launcher и generated versioning layer переведены на `2.4.1`
- policy-driven сценарии и release/boundary docs выровнены под текущий patch-релиз
- release checklist, release notes и registry history больше не расходятся с реальным состоянием repo

## Что проверено

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh && bash PRE_RELEASE_AUDIT.sh`

## Что важно для downstream

- для steady-state работы использовать `sources-pack-core-20.tar.gz`
- для release-facing прохода использовать `sources-pack-release-20.tar.gz`
- generated projects теперь получают фабричную версию `2.4.1`

## Риски и ограничения

- quality validation остаётся эвристической, а не семантической
- phase detection по-прежнему rule-based и зависит от changed paths и document signals

## Внешние шаги для пользователя

- GitHub repo и tag синхронизировать с новым релизом `v2.4.1`
- прикрепить к GitHub Release архив `factory-v2.4.1.zip`
- загрузить нужный curated Sources pack в ChatGPT Project

## Go / No-Go

- Решение: Go
- Комментарий: release-facing слой синхронизирован, verify-контур пройден, bundle собирается корректно
