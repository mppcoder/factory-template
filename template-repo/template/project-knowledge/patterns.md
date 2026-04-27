# Знания: паттерны

Фиксируйте устойчивые проектные паттерны и повторяемые решения.

## Планирование feature

Минимальная цепочка:
1. `user-spec` фиксирует пользовательское намерение через `US-*`.
2. `tech-spec` связывает реализацию с `US-*` через `User Intent Binding`.
3. Любое отклонение фиксируется в `User-Spec Deviations` и не остаётся pending в approved docs.
4. Каждая task имеет acceptance criteria и хотя бы один verification path.
5. После выполнения важные решения попадают в `decisions.md`; только устойчивые выводы переносятся в `project-knowledge/`.
6. Done closeout создает `project-knowledge-update-proposal.md` и `downstream-impact.md`, затем архивирует feature в `work/completed/`.

## Закрытие feature

Используйте `close-feature-workspace.py`, чтобы closeout не зависел от памяти агента. Нормальный результат:
- `done-report.md` объясняет, что закрыто и какие evidence проверены;
- `project-knowledge-update-proposal.md` говорит `required` или `not_required`;
- `downstream-impact.md` фиксирует downstream sync/review effect;
- workspace находится в `work/completed/` или имеет явный `closeout-blocker.md`.
