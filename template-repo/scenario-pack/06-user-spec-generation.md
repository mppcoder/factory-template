# Формирование пользовательской спецификации (user spec)

Подготовь понятный человеку документ о том, **что** должно быть сделано и **зачем**.

## Решения по умолчанию в спецификации

В пользовательской спецификации явно отрази:

- `default_decision_mode`;
- какие defaults приняты;
- какие defaults переопределены пользователем;
- какие recommendations основаны на `repo-policy`, `official-docs`, `best-practice`, `project-scale` или `user-override`;
- где есть `uncertainty_notes` / `requires fresh check`;
- какие decisions действительно требуют explicit user confirmation.

Не скрывай forced defaults. Если решение рискованное, платное, destructive, security/privacy/legal или связано с secrets, не записывай его как accepted default без явного подтверждения пользователя.

## Подсказка
Не уходи в реализацию. Здесь нужен бизнесовый и продуктовый уровень описания.
