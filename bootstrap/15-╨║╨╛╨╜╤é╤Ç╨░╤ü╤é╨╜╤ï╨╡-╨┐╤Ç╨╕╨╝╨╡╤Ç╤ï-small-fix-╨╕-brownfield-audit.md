# Контрастные примеры: small-fix и brownfield-аudit

Этот файл показывает, как меняется глубина процесса в зависимости от класса изменения.

## Пример 1. Small-fix

Используйте этот профиль, когда изменение:
- маленькое,
- локальное,
- не требует полноценной проектной переработки,
- не затрагивает архитектурные границы.

Ожидаемый минимум:
- заполненный `intake.yaml`;
- краткий `user-spec.md`;
- `reality-check.md` с локальной проверкой текущего состояния;
- `evidence-register.md` минимум с тегами `[PROJECT]` и `[FIX]` или `[DOC]`;
- короткий `task-index.yaml` на 1–2 задачи;
- `verification-report.md`.

## Пример 2. Brownfield-audit

Используйте этот профиль, когда задача — не менять систему сразу, а восстановить реальную картину существующего проекта.

Ожидаемый минимум:
- `intake.yaml`;
- `brownfield/system-inventory.md`;
- `brownfield/repo-audit.md`;
- `brownfield/as-is-architecture.md`;
- `brownfield/gap-register.md`;
- `reality-check.md`;
- `evidence-register.md`;
- `done-report.md`.

## Главный вывод

`small-fix` нужен для быстрого, но контролируемого изменения.
`brownfield-audit` нужен для безопасного восстановления реальности, когда менять систему рано.
