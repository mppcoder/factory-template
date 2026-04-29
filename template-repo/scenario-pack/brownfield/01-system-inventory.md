# Инвентаризация системы

Используй default-decision layer из `00-brownfield-entry.md`. Инвентаризация не должна начинаться с blank expert-only списка, если safe defaults уже известны.

Соберите:
- репозитории;
- окружения;
- ключевые сервисы;
- внешние интеграции;
- конфиги и критичные переменные.

Default для inventory: сначала evidence register и sanitized inventory, затем любые remediation decisions. Secrets, production dumps, security/privacy/legal data и destructive cleanup требуют explicit user confirmation и не silently default.

## Правило фиксации gap / defect
Любой gap, найденный в reverse engineering или brownfield-анализе, должен стать bug report или structured defect report до remediation planning.
