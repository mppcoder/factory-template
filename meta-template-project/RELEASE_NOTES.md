# Журнал изменений

## Unreleased

## 2.4.4
- canonical preset naming переведён на нейтральные factory names с compatibility aliases для legacy preset names
- `openclaw` вынесен из core/release-facing слоя в `optional-domain-packs/openclaw-reference`
- release docs, manifests, examples и closeout artifacts синхронизированы под `factory-v2.4.4`

## 2.4.3
- собран полный release-facing пакет по самому `factory-template`
- добавлен root-level `RELEASE_NOTES.md` как canonical published notes source
- архитектурный reference-doc теперь покрывает функционал, дерево repo и все ключевые workflow от intake до выпуска релиза
- release-facing docs, source/export profiles и closeout artifacts синхронизированы под `factory-v2.4.3`

## 2.4.2
- ChatGPT Project переведён на repo-first режим с обязательным чтением GitHub repo и `00-master-router.md`
- canonical archive `sources-pack-core-20` закреплён как steady-work snapshot, а не как единственный daily upload
- boundary guidance и release docs выровнены под hybrid-модель `direct hot-set + canonical archive`

## 2.4.1
- в отдельный patch-релиз вынесены ops-policy, phase detection и release-facing improvements из бывшего `Unreleased`
- release metadata, bundle name и GitHub tag синхронизированы под `factory-v2.4.1`
- release checklist и release note приведены к финальному go-статусу

## 2.4.0
- `rc2-smokefix` переведен в финальный релиз после полного прохождения smoke/examples/matrix
- метаданные и build output синхронизированы под финальное имя `factory-v2.4.0`
- smoke-fix включен в основной пакет

## 2.4.0-rc2
- выровнены версии и release labels между root, template, meta-template и working examples
- `RELEASE_BUILD.sh` переведен на чтение версии из `VERSION.md`
- `PRE_RELEASE_AUDIT.sh` дополнен проверками version drift и legacy-ссылок

## 2.4.0-rc1-consistency
- добавлен единый versioning/documentation layer для фабрики, шаблона и generated projects
- examples и generated project templates получили `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

## 2.4.0-base
- введен defect-capture layer
- добавлены process-файлы и шаблоны для bug report / factory feedback / ChatGPT handoff

## 2.3.7
- stabilization-релиз
- matrix runner и controlled back-sync
