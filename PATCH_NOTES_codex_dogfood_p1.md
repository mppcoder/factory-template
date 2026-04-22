# Patch notes: codex-dogfood-p1

Этот патч не ломает core сценарий `factory-v2.4.0`, а расширяет его для вашей схемы работы:
- старт из одного окна VS Code + Codex;
- переход на отдельные окна по проектам;
- brownfield-first dogfood цикл;
- session-specific `.codex` specialization и подагенты для разных типов работы внутри Codex.

## Уточнение по routing
Этот патч сам по себе не гарантирует task-based auto-switch внутри уже открытой сессии.
Надежный выбор profile/model/reasoning должен происходить только на новом task launch через launcher/router layer.

## Главное ограничение
`brownfield without repo` всё ещё должен стартовать как facts-first / audit-first контур. Патч не делает вид, что исходный repo уже существует.
