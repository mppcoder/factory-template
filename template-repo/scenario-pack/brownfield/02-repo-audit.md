# Аудит репозитория (repo)

Используй default-decision layer из `00-brownfield-entry.md`.

Проверьте:
- структуру репозитория;
- основные ветки;
- расположение критичных файлов;
- расхождения между документацией и кодом.

Recommended default: keep existing repo as canonical root, do not overwrite product-owned code, выполнить evidence-first audit before remediation, затем conversion в `greenfield-product` или documented blocker. Если пользователь переопределяет root/branch/scope, запиши это в `overridden_defaults`.

## Правило фиксации gap / defect
Любой gap, найденный в reverse engineering или brownfield-анализе, должен стать bug report или structured defect report до remediation planning.
