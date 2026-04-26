# Сводка безопасного downstream upgrade

- Сгенерировано (UTC): `2026-04-26T06:09:05+00:00`
- Корень factory: `/projects/factory-template`
- Корень downstream project: `/tmp/tmp.ZxXwae37z9/work/russian-summary-fixture`
- Версия template: `2.5.0`
- Версия sync contract: `3`
- Вердикт: `patch-ready`

## Снимок drift

- Sync zones / зоны синхронизации: `ok=10` / `drift=2` / `missing=0` / `total=12`
- Materialized files / materialized-файлы: `ok=1` / `issues=0` / `total=1`

## Предпросмотр по уровням

| Уровень | Пункты manifest | Пункты preview | Сгенерировано для apply | Можно применять |
| --- | ---: | ---: | ---: | --- |
| `safe-generated` | `6` | `4` | `3` | `True` |
| `safe-clone` | `1` | `0` | `0` | `True` |
| `advisory-review` | `3` | `1` | `0` | `False` |
| `manual-project-owned` | `3` | `1` | `0` | `False` |

## Что изменится

Безопасное применение переносит только сгенерированные файлы из уровней `safe-generated` и `safe-clone`:
- `.chatgpt/examples/done-report.example.md` из `template-repo/template/.chatgpt/examples/done-report.example.md`
- `tasks/codex/codex-task-mandatory-bug-capture.block.md` из `template-repo/template/tasks/codex/codex-task-mandatory-bug-capture.block.md`
- `work-templates/user-spec.md.template` из `template-repo/template/work-templates/user-spec.md.template`

Файлы `advisory-review` содержат только подсказки для patch/diff и требуют ручного merge:
- `project-knowledge/project.md` статус=`drift`

Файлы `manual-project-owned` являются только сигналом влияния и никогда не генерируются для apply:
- `work/_task-template.md` статус=`drift`

## Почему уровни безопасные или ручные

- `safe-generated`: apply_eligible=`True`; причина: Переиспользуемые файлы, принадлежащие шаблону, можно безопасно регенерировать при наличии rollback metadata.; действие оператора: применить через --apply-safe-zones после просмотра preview.
- `advisory-review`: apply_eligible=`False`; причина: Эти файлы могут содержать downstream choices или project knowledge; автоматическая перезапись для них небезопасна.; действие оператора: проверить patch-summary.md и вручную смержить только то, что совпадает с project intent.
- `manual-project-owned`: apply_eligible=`False`; причина: Эти зоны представляют живую проектную работу, а не сгенерированное содержимое, принадлежащее шаблону.; действие оператора: использовать только как сигнал влияния; project-owned work обновлять вручную.

### Элементы preview

- `[safe-generated]` `bootstrap` статус=`optional-missing-project` generated=`False` mode=`--dry-run`
- `[safe-generated]` `.chatgpt/examples/done-report.example.md` статус=`drift` generated=`True` mode=`--dry-run`
- `[safe-generated]` `tasks/codex/codex-task-mandatory-bug-capture.block.md` статус=`drift` generated=`True` mode=`--dry-run`
- `[safe-generated]` `work-templates/user-spec.md.template` статус=`drift` generated=`True` mode=`--dry-run`
- `[advisory-review]` `project-knowledge/project.md` статус=`drift` generated=`False` mode=`--dry-run`
- `[manual-project-owned]` `work/_task-template.md` статус=`drift` generated=`False` mode=`--dry-run`

## Снимок upgrade bundle

- Путь bundle: `/tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export`
- Измененных файлов в bundle: `3`
- Безопасных generated targets: `3`
- Сгенерированных файлов для materialize: `3`
- Rollback state присутствует: `True`
- Файлов под rollback tracking: `3`

### Измененные файлы

- `template-repo/template/.chatgpt/examples/done-report.example.md`
- `template-repo/template/tasks/codex/codex-task-mandatory-bug-capture.block.md`
- `template-repo/template/work-templates/user-spec.md.template`

### Сгенерированные файлы для безопасного применения

- `.chatgpt/examples/done-report.example.md`
- `tasks/codex/codex-task-mandatory-bug-capture.block.md`
- `work-templates/user-spec.md.template`

## Как откатить

- Rollback metadata обязательна и записывается до копирования безопасных сгенерированных файлов.
- `--rollback` восстанавливает отслеживаемые сгенерированные файлы или удаляет файлы, которых не было до apply.
- `--rollback --restore-project-snapshot` восстанавливает полный project snapshot, если apply запускался с `--with-project-snapshot`.

## Что пользователь должен проверить

- `project-knowledge/project.md` (`advisory-review`): проверить patch-summary.md и вручную смержить только то, что совпадает с project intent.
- `work/_task-template.md` (`manual-project-owned`): использовать только как сигнал влияния; project-owned work обновлять вручную.

## Канонические команды оператора

1. Подготовить или обновить bundle (dry-run):
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh /projects/factory-template /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture --dry-run
```
2. Проверить bundle перед apply:
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --check
```
3. Применить safe zones:
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --apply-safe-zones
```
4. Применить safe zones с full-project snapshot (optional, но безопаснее для смешанных ручных сессий):
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --apply-safe-zones --with-project-snapshot
```
5. Проверить rollback state:
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --check
```
6. Откатить safe-zone materialization при необходимости:
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --rollback
```
7. Откатить и восстановить полный project snapshot, если использовался snapshot mode:
```bash
/projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /tmp/tmp.ZxXwae37z9/work/russian-summary-fixture/_factory-sync-export --rollback --restore-project-snapshot
```

## Заметки по безопасности UX

- `--dry-run` и `--check` работают только на чтение.
- `--apply-safe-zones` создает rollback metadata до overwrite generated targets.
- `rollback-template-patch.sh --rollback` восстанавливает прежнее содержимое или удаляет файл, если до apply его не было.
- Optional snapshot mode добавляет путь полного восстановления project для ручных изменений вне generated safe-zones.
- Refresh ChatGPT Project Sources не входит в default downstream sync path, кроме legacy/hybrid проектов, где repo-first instructions все еще дублируются вне repo.
