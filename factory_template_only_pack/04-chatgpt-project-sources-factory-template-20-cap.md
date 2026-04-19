# Sources для ChatGPT Project шаблона фабрики — cap 20 файлов

## Принцип

Для проекта шаблона фабрики используется **операционный hard cap = 20 файлов**.

Даже если интерфейс где-то допускает больше, для шаблона лучше держать компактный curated source-pack из реально существующих файлов repo.

---

## 1. Что держать в постоянных Sources

### Ядро сценариев (6 файлов)

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

### Текущее состояние фабрики (5 файлов)

11. `README.md`
12. `VERSION.md`
13. `CHANGELOG.md`
14. `CURRENT_FUNCTIONAL_STATE.md`
15. `meta-template-project/RELEASE_NOTES.md`

### Политики и automation (3 файла)

16. `template-repo/project-presets.yaml`
17. `template-repo/policy-presets.yaml`
18. `template-repo/change-classes.yaml`

### Активный рабочий набор (2 файла)

19. `CONTROLLED_FIXES_AUDIT_2026-04-19.md`
20. `TEST_REPORT.md`

---

## 2. Что не держать как постоянные Sources

Не держать постоянно:

- большие тестовые логи;
- временные отчеты из `.smoke-test/` и `.matrix-test/`;
- `_sources-export/` и `_factory-sync-export/`;
- артефакты из `_incoming`;
- файлы, которых нет в repo;
- generated project `.chatgpt/*` из случайных тестовых прогонов.

Это должно жить в repo, а в Project Sources нужно держать только load-bearing docs и policy layer.

---

## 3. Правило ротации

Постоянными стараются оставаться слои:

- ядро сценариев;
- operator docs;
- текущее состояние фабрики;
- policy layer.

Меняется только активный рабочий набор.

### В фазе controlled fixes

активный набор:

- `CONTROLLED_FIXES_AUDIT_2026-04-19.md`
- `TEST_REPORT.md`

### В фазе release

активный набор можно заменить на:

- `FACTORY_MANIFEST.yaml`
- `RELEASE_BUILD.sh`

### В фазе deep drift analysis

активный набор можно заменить на:

- конкретный diff/audit report
- один целевой validator или launcher script

---

## 4. Роль Codex

Codex должен готовить для пользователя инструкцию:

- какие 20 файлов держать в Sources сейчас;
- что удалить из Sources;
- что заменить на новую фазу;
- какие файлы реально существуют в repo и являются source of truth.

## 5. Curated Packs

Помимо постоянного core-набора, repo сейчас поддерживает ещё два phase-oriented pack:

- `sources-pack-release-20`
  Включает release-facing слой: `RELEASE_CHECKLIST.md`, `VERIFY_SUMMARY.md`, `RELEASE_NOTE_TEMPLATE.md`, release scripts и manifests.
- `sources-pack-bugfix-20`
  Включает launcher/validator слой и handoff/feedback validators, включая `validate-codex-task-pack.sh` и `VALIDATE_FACTORY_FEEDBACK.sh`.

Эти pack'и проверяются не только по правилу `20 files`, но и по semantic profile внутри `VALIDATE_FACTORY_TEMPLATE_OPS.sh`.

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
