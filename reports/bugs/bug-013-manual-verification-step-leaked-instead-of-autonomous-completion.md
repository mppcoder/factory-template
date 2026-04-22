# Отчет о дефекте

## Идентификатор
bug-013-manual-verification-step-leaked-instead-of-autonomous-completion

## Краткий заголовок
После already-completed remediation assistant предложил пользователю ручной verification step вместо того, чтобы закончить automation autonomously and report the result.

## Где найдено
Repo: `factory-template`, reusable completion / boundary / operator-load discipline:

- final response after successful remediation
- separation between internal repo work and external user steps
- automation-first closeout behavior

## Шаги воспроизведения
1. Выполнить remediation внутри `factory-template`, где нужные проверки и sync assistant может сделать сам.
2. Дойти до состояния, когда internal repo work уже выполнен или может быть завершен без участия пользователя.
3. В финальном ответе предложить пользователю вручную запустить verification команды "если хотите перепроверить".
4. Не ограничиться уже выполненным internal verification и не завершить ответ просто итогом.

## Ожидаемое поведение
- Если assistant уже может сам выполнить verification и sync внутри repo, он не должен перекладывать это на пользователя.
- Финальный ответ должен сообщать итог уже выполненной автоматизации, а не предлагать ручную проверку как normal next step.
- `## Инструкция пользователю` должна использоваться только для реальных внешних границ, а не для внутренней repo-проверки, которую assistant обязан сделать сам.

## Фактическое поведение
- После исправления root-level routing/config issue assistant предложил пользователю вручную прогнать verification команды.
- Эти команды относились к внутренней repo-проверке и могли быть выполнены самим assistant без участия пользователя.
- Пользователь справедливо указал на это как на нарушение automation-first поведения.

## Evidence
- [PROJECT] Финальный ответ после root-level fix содержал блок с ручными командами:
  - `python3 template-repo/scripts/create-codex-task-pack.py .`
  - `python3 template-repo/scripts/validate-codex-task-pack.py .`
  - `python3 template-repo/scripts/validate-codex-routing.py .`
- [PROJECT] Следующий пользовательский сигнал: "Почему ты мне предлагаешь руками сделать то что должен автоматом сделать сам?"
- [PROJECT] Эти проверки assistant затем действительно выполнил самостоятельно и завершил change без реальной внешней границы.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, потому что это reusable process failure в source-of-truth repo: internal verification leaked into user guidance instead of staying inside autonomous completion.

## Статус
зафиксировано
