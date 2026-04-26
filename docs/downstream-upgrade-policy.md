# Политика downstream upgrade

Эта политика описывает, как downstream/battle repos получают обновления из `factory-template`.

## Источник истины

- `factory-template` остается каноническим source для шаблона.
- Корневой downstream `AGENTS.md` является materialized clone из `template-repo/AGENTS.md`.
- Downstream-операторы используют `workspace-packs/factory-ops/export-template-patch.sh`, чтобы собрать preview bundle перед любым apply-шагом.

## Уровни синхронизации

Контракт синхронизации задан в `workspace-packs/factory-ops/factory-sync-manifest.yaml`.

| Уровень | Значение | Поведение apply |
| --- | --- | --- |
| `safe-generated` | Сгенерированные файлы, принадлежащие шаблону: scenario pack, task blocks, examples, feedback starters, work templates. | `apply-template-patch.sh --apply-safe-zones` может копировать generated files и записывает rollback metadata до overwrite. |
| `safe-clone` | Materialized clone files, например downstream root `AGENTS.md` из `template-repo/AGENTS.md`. | Controlled apply разрешен, потому что clone объявлен template-owned. |
| `advisory-review` | Справочные docs, `.codex` guidance и `project-knowledge`. | Только preview/diff/merge guidance; автоматическая перезапись запрещена. |
| `manual-project-owned` | Проектная lifecycle work: `greenfield`, `brownfield`, `work`. | Только сигнал влияния; patch/generation для automatic apply не создается. |

## Metadata bundle / metadata пакета

Каждый export пишет:

- `bundle-metadata.json`: bundle schema, template version, contract version, tier counts с учетом режима и количество generated safe-files.
- `preview-changes.json`: tier, target, status, preview mode, safety reason, operator action и флаг генерации для apply по каждому файлу.
- `safe-changed-files.txt`: точные generated targets, которые safe apply может копировать.
- `patch-summary.md`: человекочитаемое operator summary.

Статический source для bundle schema: `workspace-packs/factory-ops/sync-bundle-version.json`.

## Операторский flow

```bash
bash workspace-packs/factory-ops/export-template-patch.sh <factory-root> <downstream-root> --dry-run
bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --check
bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot
python3 workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md
```

Используйте `--with-project-snapshot`, если человек редактировал файлы в той же upgrade-сессии.

`--dry-run` собирает обычный preview bundle и materializes только safe-generated/safe-clone candidates в `generated-files/`.
`--advisory` собирает review-only bundle: diff/preview сохраняются, но generated files для apply не создаются.

## Rollback flow / поток отката

```bash
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --check
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot
```

`--rollback` восстанавливает только tracked generated files из safe-tier. `--rollback --restore-project-snapshot` восстанавливает полный snapshot, созданный во время apply, и является более безопасным путем для смешанных manual-сессий.

## Правила безопасности

- Изменения `advisory-review` и `manual-project-owned` не должны копироваться через `apply-template-patch.sh`.
- `project-knowledge` по умолчанию является `advisory-review`: используйте diff/merge guidance и переносите только то, что соответствует локальному project intent.
- `work-templates` являются `safe-generated`, но live project work под `work/` является `manual-project-owned` и защищен от автоматической перезаписи.
- Отсутствующие optional safe zones сообщаются как `optional-missing-project`, а не как hard failure.
- Перед ручным копированием из advisory-review patches проверьте локальный project intent и текущее состояние работы.
- Если safe apply неожиданно перезаписал локальные edits, сначала зафиксируйте bug report и только потом делайте remediation.
