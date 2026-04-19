# Patch notes: codex-dogfood-p1

Этот патч не ломает core сценарий `factory-v2.4.0`, а расширяет его для вашей схемы работы:
- старт из одного окна VS Code + Codex;
- переход на отдельные окна по проектам;
- brownfield-first dogfood цикл;
- автоматическое переключение режимов через подагентов и project-level `.codex` config.

## Главное ограничение
`brownfield without repo` всё ещё должен стартовать как facts-first / audit-first контур. Патч не делает вид, что исходный repo уже существует.
