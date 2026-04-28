# Закрытие: путь без repo

## Критерии завершения

- Brownfield without repo не остался финальным состоянием.
- Canonical repo существует внутри target project root.
- With-repo adoption/conversion выполнен или documented blocker создан.
- Active project preset: `greenfield-product`.
- Lifecycle state: `greenfield-converted`.
- `_incoming/`, `reconstructed-repo/`, helper workspaces и intermediate materials archived/renamed/moved так, чтобы active greenfield root был понятен.

## Если нужен пользователь

Пользователь нужен только для внешних материалов, approvals, secrets, real GitHub/release/runtime UI или blocker decision.
Если таких действий нет, closeout пишет: `Внешних действий не требуется.`
