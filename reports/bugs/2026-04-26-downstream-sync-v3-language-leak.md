# Утечка английского текста в downstream sync v3

## Сводка

`upgrade-report.py` генерирует `UPGRADE_SUMMARY.md` с частично англоязычной человекочитаемой прозой.

## Как воспроизвести

1. Сгенерировать downstream upgrade summary через `factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py`.
2. Открыть `UPGRADE_SUMMARY.md`.
3. Проверить человекочитаемые подписи, пункты списка и шаги оператора.

## Доказательства

Найдены англоязычные фрагменты в активном source-facing артефакте:

- `Generated (UTC)`
- `Factory root`
- `Downstream project root`
- `Safe apply materializes`
- `reason`
- `operator action`
- `Rollback metadata is mandatory`
- `Prepare/refresh bundle`
- `ChatGPT Project Sources refresh is not part...`

## Ожидаемое поведение

Человекочитаемый слой должен быть на русском. Английскими могут оставаться только literal tokens:

- имена файлов;
- CLI-флаги;
- JSON/YAML keys;
- sync tier ids;
- статусы из machine-readable metadata.

## Фактическое поведение

Генератор отчета смешивает русский и английский текст в одном отчете для оператора.

## Классификация слоя

- Слой: factory ops / downstream sync UX.
- Класс дефекта: regression языкового слоя.
- Переиспользуемый factory issue: да, потому что generated downstream operator reports наследуют тот же текст.

## Цель исправления

Перевести человекочитаемые строки `upgrade-report.py` на русский и перегенерировать `UPGRADE_SUMMARY.md`.

## Проверка

- `python3 template-repo/scripts/validate-human-language-layer.py .`
- targeted scan для известных англоязычных фрагментов в `UPGRADE_SUMMARY.md` и `upgrade-report.py`
- `bash template-repo/scripts/verify-all.sh ci`
