# Sources для ChatGPT Project шаблона фабрики — hybrid hot/cold strategy

## Принцип

Для `factory-template` теперь штатно поддерживается **hybrid-схема**:

- **direct hot-set** для ежедневной работы в ChatGPT Project;
- **cold/reference remainder archive** без дублей hot-set;
- **canonical archive pack** как полный steady-work snapshot и reference bundle.

Даже если интерфейс где-то допускает больше, для шаблона лучше держать небольшой direct hot-set и отдельно хранить архивный bundle как reference.

---

## 1. Что держать в постоянных Sources

Постоянным набором теперь считается не archive pack, а direct profile `core-hot-15`.

### Direct hot-set `core-hot-15` (15 файлов)

Этот export теперь всегда собирается в одну flat-папку без подпапок, чтобы файлы можно было брать и загружать в Sources без ручной навигации по вложенной структуре.

1. `template-repo/scenario-pack/00-master-router.md`
2. `template-repo/scenario-pack/01-global-rules.md`
3. `template-repo/scenario-pack/02-decision-policy.md`
4. `template-repo/scenario-pack/03-stage-gates.md`
5. `template-repo/scenario-pack/15-handoff-to-codex.md`
6. `template-repo/scenario-pack/16-done-closeout.md`

### Операторский слой template-only (4 файла)

7. `factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md`
8. `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md`
9. `factory_template_only_pack/03-mode-routing-factory-template.md`
10. `factory_template_only_pack/07-AGENTS-factory-template.md`
11. `CURRENT_FUNCTIONAL_STATE.md`
12. `VERSION.md`
13. `template-repo/change-classes.yaml`
14. `template-repo/policy-presets.yaml`
15. `template-repo/project-presets.yaml`

---

## 2. Cold / reference remainder archive

Для чистой hybrid-схемы без дублей используется отдельный archive remainder:

- `core-cold-5.tar.gz`

Он содержит только оставшийся cold/reference слой:

- `README.md`
- `CHANGELOG.md`
- `TEST_REPORT.md`
- `CONTROLLED_FIXES_AUDIT_2026-04-19.md`
- `meta-template-project/RELEASE_NOTES.md`

Этот архив не повторяет состав hot-set и для удобства также кладётся прямо в папку `core-hot-15/`, чтобы daily upload набор был собран в одном месте.

---

## 3. Canonical archive pack

Canonical archive pack остаётся:

- `sources-pack-core-20.tar.gz`

Он содержит весь steady-work content set и остается основным reference bundle.

Canonical archive нужен не для постоянной загрузки в Sources, а как:

- полный контрольный снимок steady-work состава;
- reference bundle для сверки и регрессии;
- исходный канонический набор, из которого выводятся hot-set и cold remainder.

---

## 4. Как пользоваться схемой hot + cold

Рекомендуемая схема:

- в Sources проекта загружать напрямую файлы из flat-папки `core-hot-15/`;
- `core-cold-5.tar.gz` брать из той же папки `core-hot-15/` и загружать как отдельный cold/reference archive remainder без дублей;
- `sources-pack-core-20.tar.gz` хранить как canonical archive snapshot и reference bundle;
- cold/reference-файлы использовать при release audit, регрессии и post-mortem;
- phase-specific pack'и не использовать как второй постоянный набор для ежедневной работы.

---

## 5. Archive overrides

Помимо постоянного core-набора, repo сейчас поддерживает ещё два phase-oriented pack:

- `sources-pack-release-20`
  Включает release-facing слой: `RELEASE_CHECKLIST.md`, `VERIFY_SUMMARY.md`, `RELEASE_NOTE_TEMPLATE.md`, release scripts и manifests.
- `sources-pack-bugfix-20`
  Включает launcher/validator слой и handoff/feedback validators, включая `validate-codex-task-pack.sh` и `VALIDATE_FACTORY_FEEDBACK.sh`.

Эти pack'и остаются archive override-профилями и проверяются не только по правилу `20 files`, но и по semantic profile внутри `VALIDATE_FACTORY_TEMPLATE_OPS.sh`.

Текущая рекомендация по фазам:

- `controlled-fixes` -> `sources-pack-core-20.tar.gz`
- `release` -> `sources-pack-release-20.tar.gz`
- `bugfix-drift` -> `sources-pack-bugfix-20.tar.gz`

Эта матрица хранится в `factory-template-ops-policy.yaml` и автоматически попадает в:

- `_sources-export/factory-template/SUMMARY.md`
- `_boundary-actions/factory-template-boundary-actions.md`

Текущую автоопределённую фазу можно посмотреть через:

```bash
bash DETECT_FACTORY_TEMPLATE_PHASE.sh
```

Для `release` этого недостаточно только по changed files:

- detector дополнительно ждёт checked intent markers в `RELEASE_CHECKLIST.md`;
- это снижает риск ложного переключения в release phase из-за обычной правки release docs.

Для `bugfix-drift` действует похожее правило:

- detector ждёт bug/validator changed paths;
- и дополнительно смотрит intent markers внутри `reports/bugs/*.md`.

---

## 6. Источник правды

Состав и archive pack, и direct hot-set берётся из декларативного manifest:

- `packaging/sources/sources-profiles.yaml`

Из него же теперь строится и cold/reference remainder archive.

Пользователь не должен вручную выбирать файлы для постоянной загрузки.
Пользователь также не должен раскладывать hot-set по подпапкам: canonical export для `core-hot-15` уже плоский.
