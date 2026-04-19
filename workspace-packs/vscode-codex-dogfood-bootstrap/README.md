# Workspace pack: VS Code + Codex dogfood bootstrap

Этот пакет нужен для старта из одного окна VS Code по схеме:
- сначала один bootstrap hub;
- затем переход на отдельные окна по проектам.

## Что внутри
- multi-root workspace для `/projects/*`
- рекомендуемые VS Code settings/tasks
- пример глобального Codex config
- инструкция по раскладке окон

## Рекомендуемый порядок
1. Открыть `bootstrap-hub.code-workspace`.
2. Поднять `factory-template`.
3. Создать `dogfood-brownfield-shell`.
4. Создать `brownfield-evidence`.
5. После старта работ открыть отдельные окна для `factory-template`, `dogfood-brownfield-shell`, `brownfield-evidence`.
6. После stabilization добавить окна `reconstructed-brownfield-repo` и `product-greenfield-package`.
