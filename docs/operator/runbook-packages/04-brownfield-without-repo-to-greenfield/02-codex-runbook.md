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
4. Если пользователь дал non-standard VPS folders без repo, зафиксируй их роли:
   - patched runtime distribution source;
   - overlay/customization source;
   - runtime state / logs / secrets excluded;
   - target active repo must be materialized under `/projects/<project-slug>/reconstructed-repo`.
5. Зафиксируй evidence:
   - `brownfield/system-inventory.md`;
   - `brownfield/as-is-architecture.md`;
   - `brownfield/gap-register.md`;
   - `.chatgpt/evidence-register.md`;
   - `.chatgpt/reality-check.md`.
6. Зафиксируй software/runtime baseline, если incoming materials или recovered system связаны с VPS:
   - selected Ubuntu LTS release / provider image id если доступен;
   - OS image release отдельно от later package update state;
   - kernel, package manager sources и `unattended-upgrades`;
   - Docker/Compose, Node/Python, GitHub Actions, base Docker images/tags/digests, lockfiles и critical runtime dependencies.
7. Создай `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml` и `reports/software-updates/README.md`; policy `manual-approved-upgrade`, auto-install без approval запрещен.
8. Составь:
   - `brownfield/reverse-engineering-plan.md`;
   - `brownfield/reverse-engineering-summary.md`;
   - `brownfield/decision-log.md`.
9. Реконструируй canonical repo только внутри target root, например `/projects/<project-slug>/reconstructed-repo`.
10. После reconstruction перейди к with-repo adoption cycle.
11. Если GitHub write path доступен и owner/name однозначны, Codex создает repo/remote и делает initial sync сам.
12. Выполни conversion в `greenfield-product` / `greenfield-converted` или создай explicit documented blocker.
13. Transitional materials после conversion должны быть archived/renamed/moved out of active path.
14. Если real `APP_IMAGE`, approved target, secrets boundary и deploy/restore/rollback approvals есть, Codex может закрыть local prod runtime proof. Public HTTPS/nginx proof остается отдельным approval boundary.
15. Запусти validators, `python3 scripts/validate-software-update-governance.py .` и verified sync при доступности.

Ubuntu LTS migration всегда оформляется как отдельный migration/upgrade project, а не silent maintenance step.

## Правило завершения

Done наступает только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
