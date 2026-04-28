# Ранбук для Codex: путь с существующим repo

## Маршрут

Supported transitional presets:

- `brownfield-with-repo-modernization`;
- `brownfield-with-repo-integration`;
- `brownfield-with-repo-audit`.

Target preset: `greenfield-product`.
Target lifecycle: `greenfield-converted`.

## Аудит и принятие

1. Прочитай master router и brownfield route files.
2. Materialize repo-first core без перезаписи product code.
3. Заполни evidence:
   - `brownfield/system-inventory.md`;
   - `brownfield/repo-audit.md`;
   - `brownfield/as-is-architecture.md`;
   - `brownfield/gap-register.md`;
   - `brownfield/change-map.md`;
   - `brownfield/risks-and-constraints.md`;
   - `.chatgpt/reality-check.md`;
   - `.chatgpt/conflict-report.md`.
4. Защити project-owned zones.
5. Нормализуй только safe structural drift.

## Конверсия

Conversion считается завершенным только когда:

- `.chatgpt/project-profile.yaml` содержит `project_preset: greenfield-product`;
- recommended mode стал `greenfield`;
- `.chatgpt/stage-state.yaml` фиксирует `lifecycle_state: greenfield-converted`;
- brownfield evidence архивировано или явно referenced как history;
- validators green.

Если conversion невозможна, создай explicit `brownfield/conversion-blocker.md` или `.chatgpt/conversion-blocker.md`.
