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
