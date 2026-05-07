# Закрытие: путь без repo

## Критерии завершения

- Brownfield without repo не остался финальным состоянием.
- Default-decision state сохранен: mode selected, defaults accepted or overridden, overrides captured, secret/private/destructive confirmations explicit.
- Canonical repo существует внутри target project root.
- With-repo adoption/conversion выполнен или documented blocker создан.
- Non-standard VPS folders больше не являются active source roots.
- Runtime/source patches promoted only through reviewed source-hardening
  decisions.
- Active project preset: `greenfield-product`.
- Lifecycle state: `greenfield-converted`.
- `_incoming/`, `reconstructed-repo/`, helper workspaces и intermediate materials archived/renamed/moved так, чтобы active greenfield root был понятен.
- Если выполнялся runtime proof, его scope явно разделяет local prod runtime
  proof и public HTTPS/reverse-proxy proof.

## Если нужен пользователь

Пользователь нужен только для внешних материалов, approvals, secrets, real GitHub/release/runtime UI или blocker decision.
Если таких действий нет, closeout пишет: `Внешних действий не требуется.`
