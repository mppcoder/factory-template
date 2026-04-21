# Strategy For ChatGPT Project Sources

## Model

`factory-template` использует hybrid-модель:

- direct hot-set для ежедневной работы в ChatGPT Project;
- cold/reference remainder archive без дублей hot-set;
- canonical archive pack как полный steady-work snapshot и reference bundle;
- phase-specific archive packs только как operator override.

## Canonical Daily Profile

Постоянным набором для ChatGPT Project считается:

- `core-hot-15/`

Это direct Sources profile, где всё, что нужно загружать в Sources, лежит в одной flat-подпапке `upload-to-sources/`:

1. `template-repo/scenario-pack/00-master-router.md`
2. `template-repo/scenario-pack/01-global-rules.md`
3. `template-repo/scenario-pack/02-decision-policy.md`
4. `template-repo/scenario-pack/03-stage-gates.md`
5. `template-repo/scenario-pack/15-handoff-to-codex.md`
6. `template-repo/scenario-pack/16-done-closeout.md`
7. `factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md`
8. `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md`
9. `factory_template_only_pack/03-mode-routing-factory-template.md`
10. `factory_template_only_pack/07-AGENTS-factory-template.md`
11. `CURRENT_FUNCTIONAL_STATE.md`
12. `VERSION.md`
13. `template-repo/change-classes.yaml`
14. `template-repo/policy-presets.yaml`
15. `template-repo/project-presets.yaml`

При загрузке в ChatGPT Project открывайте только `core-hot-15/upload-to-sources/`.
Если когда-нибудь появится конфликт одинаковых базовых имён, export применит deterministic naming strategy вместо silent overwrite.

## Cold / Reference Remainder Archive

Для hybrid-загрузки без дублей используйте отдельный archive remainder:

- `core-cold-5.tar.gz`

Он содержит только cold/reference слой:

- `README.md`
- `CHANGELOG.md`
- `TEST_REPORT.md`
- `CONTROLLED_FIXES_AUDIT_2026-04-19.md`
- `meta-template-project/RELEASE_NOTES.md`

Этот архив также лежит внутри `core-hot-15/upload-to-sources/`, чтобы весь daily upload набор был собран в одном месте.

## Canonical Archive

Canonical archive pack остаётся:

- `sources-pack-core-20.tar.gz`

Он не заменяет direct profile и нужен как:

- полный steady-work snapshot;
- резервный reference bundle;
- полный контрольный снимок состава, из которого выводятся и hot-set, и cold remainder;
- `manifest.json` как служебный файл archive pack

## Recommended Workflow

1. Запустить `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`.
2. Если нужен Codex-managed Google Drive folder contour, запустить `bash EXPORT_AND_SYNC_FACTORY_TEMPLATE_SOURCES_TO_GDRIVE.sh`.
3. Для ежедневной работы открыть `_sources-export/factory-template/core-hot-15/upload-to-sources/`.
4. Загрузить в ChatGPT Project все файлы из этой подпапки.
5. Archive `sources-pack-core-20.tar.gz` сохранить как canonical snapshot и reference bundle.
6. При release/bugfix-фазе при необходимости использовать phase-specific archive override, но не держать его как второй постоянный набор Sources.

## Google Drive Sync Boundary

Google Drive contour теперь готовит hot export и connector sync request/report в `_sources-export/factory-template/_sync-reports/`.

Канонический path:

- `bash EXPORT_AND_SYNC_FACTORY_TEMPLATE_SOURCES_TO_GDRIVE.sh`

Минимальные env-переменные:

- `GOOGLE_DRIVE_FOLDER_URL`
- `GOOGLE_DRIVE_DELETE_STALE=0|1`
- `GOOGLE_DRIVE_DRY_RUN=0|1`
- `GOOGLE_DRIVE_SUPPORTS_ALL_DRIVES=0|1`

Для `factory-template` canonical config лежит в root `.chatgpt/google-drive-sources.yaml`.
Для развёрнутого боевого проекта template теперь несёт свой `template-repo/template/.chatgpt/google-drive-sources.yaml`, чтобы `GOOGLE_DRIVE_FOLDER_URL` можно было заменить на dedicated folder конкретного проекта.
`template-repo/template/.env.example` остаётся optional override-слоем поверх YAML.

Это не означает:

- автоматический refresh `factory-template` ChatGPT Project Sources;
- auto-reindex внутри ChatGPT Project;
- что repo-shell сам вызывает Drive mutations без Codex connector boundary.

Для `delete stale` используйте dedicated folder. Если папка shared или в ней есть посторонние файлы, сначала зафиксируйте это в completion package и не удаляйте такие файлы молча.

## Single Source Of Truth

Составы archive pack и direct profile не поддерживаются вручную в двух местах.

Они строятся из одного declarative manifest:

- `packaging/sources/sources-profiles.yaml`
