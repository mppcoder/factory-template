# Workspace pack: VS Code + Codex dogfood bootstrap

Этот пакет нужен для старта из одного окна VS Code по схеме:
- сначала один bootstrap hub;
- затем переход на отдельные окна по проектам.

## Что внутри
- multi-root workspace только для project roots и project-local подпапок
- рекомендуемые VS Code settings/tasks
- пример глобального Codex config
- инструкция по раскладке окон

## Рекомендуемый порядок
1. Открыть `bootstrap-hub.code-workspace`.
2. Поднять `factory-template`.
3. Для brownfield dogfood создать отдельный project root, например `dogfood-brownfield-project`.
4. Внутри него использовать project-local папки, например `_incoming`, `evidence/`, `reconstructed-repo/`.
5. После старта работ открывать отдельные окна для `factory-template` и для нужных project roots.
6. Если появляется reconstructed repo, он должен жить внутри соответствующего project root, а не соседом верхнего уровня в `/projects`.

## Canonical VPS layout
- `/projects` содержит только project roots;
- `_incoming` допускается только как `/projects/<project-root>/_incoming/`;
- brownfield temporary, intermediate и reconstructed repo допускаются только внутри своего project root.
