# Ранбук для Codex: путь с существующим repo

## Подтверждение маршрута

Supported transitional presets:

- `brownfield-with-repo-modernization`;
- `brownfield-with-repo-integration`;
- `brownfield-with-repo-audit`.

Target preset: `greenfield-product`.
Target lifecycle: `greenfield-converted`.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь предоставляет external repo access, approvals и secrets. Codex выполняет audit/adoption/conversion внутри repo сам.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Прочитай master router и brownfield route files.
2. Убедись, что existing repo открыт как canonical project root, не sibling helper repo.
3. Materialize repo-first core без перезаписи product code.
4. Заполни evidence:
   - `brownfield/system-inventory.md`;
   - `brownfield/repo-audit.md`;
   - `brownfield/as-is-architecture.md`;
   - `brownfield/gap-register.md`;
   - `brownfield/change-map.md`;
   - `brownfield/risks-and-constraints.md`;
   - `.chatgpt/reality-check.md`;
   - `.chatgpt/conflict-report.md`.
5. Защити project-owned zones и нормализуй только safe structural drift.
6. Выполни conversion:
   - `.chatgpt/project-profile.yaml` содержит `project_preset: greenfield-product`;
   - recommended mode стал `greenfield`;
   - `.chatgpt/stage-state.yaml` фиксирует `lifecycle_state: greenfield-converted`;
   - brownfield evidence архивировано или явно referenced как history.
7. Если conversion невозможна, создай explicit `brownfield/conversion-blocker.md` или `.chatgpt/conversion-blocker.md`.
8. Запусти validators и verified sync при доступности.

## Правило завершения

Conversion считается завершенным только после `greenfield-product` / `greenfield-converted` или explicit documented blocker.
