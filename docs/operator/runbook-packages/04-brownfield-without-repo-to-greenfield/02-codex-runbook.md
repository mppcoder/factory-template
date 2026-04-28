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
5. Составь:
   - `brownfield/reverse-engineering-plan.md`;
   - `brownfield/reverse-engineering-summary.md`;
   - `brownfield/decision-log.md`.
6. Реконструируй canonical repo только внутри target root, например `/projects/<project-slug>/reconstructed-repo`.
7. После reconstruction перейди к with-repo adoption cycle.
8. Выполни conversion в `greenfield-product` / `greenfield-converted` или создай explicit documented blocker.
9. Transitional materials после conversion должны быть archived/renamed/moved out of active path.
10. Запусти validators и verified sync при доступности.

## Правило завершения

Done наступает только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
