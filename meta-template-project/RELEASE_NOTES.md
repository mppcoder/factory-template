# Журнал изменений

## Unreleased
- зафиксирован release-followup для factory-template defect remediation из `a9b05c0`
- reusable process gap закрыт: inline Codex handoff теперь обязателен при допустимом handoff и достаточной определенности задачи
- reusable process gap закрыт: финальный блок `Инструкция пользователю` теперь обязателен при любом pending user/external step
- reusable process gap закрыт: internal repo follow-up после remediation/push больше не должен ошибочно уходить в user-only closeout
- reusable process hardening добавил source-update completion package для factory Sources, downstream repo sync и battle ChatGPT Project Sources
- downstream process behavior обновлен без изменения release semantics: автопубликация релиза не добавлена, release discipline сохранена
- добавлен separate contour для auto commit/push после successful verify и отдельный release executor после явного release decision

## 2.4.2
- добавлен declarative direct Sources profile `core-hot-15` для ежедневной работы в ChatGPT Project
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
