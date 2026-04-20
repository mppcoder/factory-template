# Общая история изменений фабрики

## 2.4.1
- бывший `Unreleased` оформлен как отдельный patch-релиз
- release-facing docs и checklist доведены до go/no-go состояния
- bundle и GitHub release синхронизированы под `factory-v2.4.1`

## 2.4.0
- финализирован `rc2-smokefix` после полного прогона smoke/examples/matrix на чистом архиве
- `SMOKE_TEST.sh` переведен на детерминированное заполнение артефактов через `tools/fill_smoke_artifacts.py`
- внутреннее имя пакета синхронизировано с финальным release id `factory-v2.4.0`

## 2.4.0-rc2
- выровнены версии и release labels между root/template/meta-template/working examples
- `RELEASE_BUILD.sh` переведен на чтение версии из `VERSION.md`
- `PRE_RELEASE_AUDIT.sh` усилен проверками на version drift и legacy-ссылки

## 2.4.0-rc1-consistency
- добавлен versioning/documentation layer
- синхронизированы project-origin, VERSION, CHANGELOG и CURRENT_FUNCTIONAL_STATE

# История релизов

## 2.3.9
- stabilization-релиз;
- добавлен `PRE_RELEASE_AUDIT.sh`;
- добавлен controlled safe-apply для back-sync;
- scaffold-only examples стали полезнее;
- `MATRIX_TEST.sh` закреплён как главный сводный раннер.
