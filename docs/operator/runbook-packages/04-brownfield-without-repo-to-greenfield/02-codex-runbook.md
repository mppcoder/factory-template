# Ранбук для Codex: путь без repo

## Подтверждение маршрута

- Entry preset: `brownfield-without-repo`.
- Start lifecycle: `brownfield-without-repo-intake`.
- Intermediate lifecycle: `brownfield-without-repo-reconstruction`.
- Then: with-repo audit/adoption.
- Final target: `greenfield-product` / `greenfield-converted`.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь предоставляет external materials, approvals и secrets decisions. Codex выполняет intake/reconstruction/adoption/conversion внутри target project root.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

1. Прочитай master router и brownfield scenarios.
2. Проверь, что `/projects/<project-slug>/_incoming/` находится внутри target root.
3. Убедись, что temporary/reconstructed/helper repo не является sibling в `/projects`.
4. Зафиксируй evidence:
   - `brownfield/system-inventory.md`;
   - `brownfield/as-is-architecture.md`;
   - `brownfield/gap-register.md`;
   - `.chatgpt/evidence-register.md`;
   - `.chatgpt/reality-check.md`.
5. Зафиксируй software/runtime baseline, если incoming materials или recovered system связаны с VPS:
   - selected Ubuntu LTS release / provider image id если доступен;
   - OS image release отдельно от later package update state;
   - kernel, package manager sources и `unattended-upgrades`;
   - Docker/Compose, Node/Python, GitHub Actions, base Docker images/tags/digests, lockfiles и critical runtime dependencies.
6. Создай `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml` и `reports/software-updates/README.md`; policy `manual-approved-upgrade`, auto-install без approval запрещен.
7. Составь:
   - `brownfield/reverse-engineering-plan.md`;
   - `brownfield/reverse-engineering-summary.md`;
   - `brownfield/decision-log.md`.
8. Реконструируй canonical repo только внутри target root, например `/projects/<project-slug>/reconstructed-repo`.
9. После reconstruction перейди к with-repo adoption cycle.
10. Выполни conversion в `greenfield-product` / `greenfield-converted` или создай explicit documented blocker.
11. Transitional materials после conversion должны быть archived/renamed/moved out of active path.
12. Запусти validators, `python3 scripts/validate-software-update-governance.py .` и verified sync при доступности.

Ubuntu LTS migration всегда оформляется как отдельный migration/upgrade project, а не silent maintenance step.

## Правило завершения

Done наступает только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
