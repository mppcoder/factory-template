# Factory ops — дополнительный operational слой

Этот пакет не входит в обязательное ядро фабрики.
Он нужен для эксплуатационной дисциплины вокруг шаблона:
- проверка drift между фабрикой и working project;
- сбор advisory patch bundle для обратной синхронизации;
- детектор признаков factory issue;
- optional git hooks.

Дополнительно пакет теперь materializes repo-first instruction contour для downstream repos:
- source-of-truth хранится в `template-repo/AGENTS.md`;
- root `AGENTS.md` downstream repo синхронизируется как materialized clone через `export-template-patch.sh` + `apply-template-patch.sh --apply-safe-zones`;
- `check-template-drift.py` ловит отсутствие root clone и drift/manual edits относительно template source.

Новые operational helpers для безопасного upgrade UX:
- `upgrade-report.py` генерирует human-readable отчёт по dry-run/apply/rollback;
- `apply-template-patch.sh --apply-safe-zones` теперь сохраняет rollback state и backup перед materialized overwrite;
- `apply-template-patch.sh --apply-safe-zones --with-project-snapshot` дополнительно сохраняет full-project snapshot для расширенного rollback;
- `rollback-template-patch.sh --check|--rollback` откатывает materialized safe-зоны по сохраненному state;
- `rollback-template-patch.sh --rollback --restore-project-snapshot` восстанавливает full-project snapshot (если он был создан на apply-шаге);
- `check-template-drift.py --format human` дает readable drift summary без ручного чтения raw JSON.
