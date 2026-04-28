# Ранбук для Codex: путь без repo

## Маршрут

- Entry preset: `brownfield-without-repo`.
- Start lifecycle: `brownfield-without-repo-intake`.
- Intermediate lifecycle: `brownfield-without-repo-reconstruction`.
- Then: with-repo audit/adoption.
- Final target: `greenfield-product` / `greenfield-converted`.

## Прием и реконструкция

1. Прочитай master router и brownfield scenarios.
2. Создай/проверь `/projects/<project-slug>/_incoming/`.
3. Зафиксируй evidence:
   - `brownfield/system-inventory.md`;
   - `brownfield/as-is-architecture.md`;
   - `brownfield/gap-register.md`;
   - `.chatgpt/evidence-register.md`;
   - `.chatgpt/reality-check.md`.
4. Составь:
   - `brownfield/reverse-engineering-plan.md`;
   - `brownfield/reverse-engineering-summary.md`;
   - `brownfield/decision-log.md`.
5. Реконструируй canonical repo только внутри target root.

## Принятие и конверсия

После reconstruction перейди к with-repo adoption cycle.
Done наступает только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.

Transitional materials после conversion должны быть архивированы, переименованы или перенесены из active root view, чтобы operator не путал их с active greenfield source.
