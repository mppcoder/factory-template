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
5. Зафиксируй controlled software update baseline:
   - `.chatgpt/software-inventory.yaml`;
   - `.chatgpt/software-update-watchlist.yaml`;
   - `.chatgpt/software-update-readiness.yaml`;
   - `reports/software-updates/README.md`.
6. Для VPS обязательно записать selected Ubuntu LTS release / provider image id если доступен, OS image release отдельно от later package update state, kernel, package manager sources, `unattended-upgrades`, Docker/Compose, Node/Python, GitHub Actions, base Docker images/tags/digests, lockfiles и critical runtime dependencies.
7. Запретить auto-install без approval: policy `manual-approved-upgrade`; update readiness может готовить proposal, но не выполняет upgrade/remediation. Переход на новую Ubuntu LTS — отдельный migration/upgrade project.
8. Защити project-owned zones и нормализуй только safe structural drift.
9. Выполни conversion:
   - `.chatgpt/project-profile.yaml` содержит `project_preset: greenfield-product`;
   - recommended mode стал `greenfield`;
   - `.chatgpt/stage-state.yaml` фиксирует `lifecycle_state: greenfield-converted`;
   - brownfield evidence архивировано или явно referenced как history.
10. Если conversion невозможна, создай explicit `brownfield/conversion-blocker.md` или `.chatgpt/conversion-blocker.md`.
11. Запусти validators, `python3 scripts/validate-software-update-governance.py .` и verified sync при доступности.

## Правило завершения

Conversion считается завершенным только после `greenfield-product` / `greenfield-converted` или explicit documented blocker.
