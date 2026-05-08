# Goal-first flow для factory-template

## Что это

`goal first` означает, что новая задача сначала становится явным `goal_contract`, а уже потом идет по обычному repo route.

Контракт должен отвечать на вопросы:
- какой результат нужен;
- как понять, что результат достигнут;
- какие evidence нужны;
- что входит и что не входит в scope;
- какие действия запрещены;
- где бюджет, stop criteria и feedback tools;
- какие proxy signals нельзя считать успехом.

## Команды пользователя

Команды `goal`, `goal:`, `/goal`, `цель`, `цель:` в ChatGPT Project означают goal-first intent.
Это не обещание, что Codex CLI runtime `/goal` доступен или включен.

Если цель достаточно определена, ChatGPT/Codex фиксирует defaults и продолжает route.
Если DoD нельзя безопасно вывести, задается один короткий уточняющий вопрос.

## Codex runtime

`Codex /goal runtime` optional.
Его можно использовать как рабочий candidate только после live validation:

```bash
codex --version
codex features list
```

Если `goals` есть как experimental/off by default, использовать его можно только по явному operator/user выбору.
Already-open session не считается reliable runtime switch.

## Observation policy

Long goal loops нельзя оставлять без наблюдения.
Для длинных задач фиксируйте:
- observation cadence;
- time/token/iteration budget;
- stop criteria;
- done/remaining/blockers summary при остановке.

Останавливайтесь при:
- budget_limited;
- tool_limited;
- quota_wall;
- goal_drift;
- unsafe_action;
- unexpected tool failure.

## Side clarification

Если runtime поддерживает `/side`, используйте его только для уточнений.
Side-channel clarification не меняет active goal, пока пользователь явно это не подтвердил.

## Proxy-signal denylist

Не закрывайте goal только потому, что:
- tests passed alone;
- file exists alone;
- commit exists alone;
- green dashboard alone;
- validator passed alone.

Validator pass является evidence, но closeout сравнивает evidence с DoD.

## Broad tasks

Для broad migration/refactor/architecture используйте `scrappy -> PRD -> clean`.
Не запускайте один большой автономный goal без decomposition.

## Минимальная repo-first ChatGPT Project instruction delta

Добавлять этот delta нужно только если текущий ChatGPT Project instruction contract реально меняется.
Если проект уже читает repo-first router из `mppcoder/factory-template`, отдельное UI-обновление обычно не требуется.

```text
После обязательного repo-first чтения `template-repo/scenario-pack/00-master-router.md` применяй goal-first normalization gate.
Если пользователь начинает с `goal`, `goal:`, `/goal`, `цель`, `цель:` или просит goal-first flow, нормализуй запрос в `goal_contract`.
Считай `/goal` в ChatGPT Project intent постановкой цели, а не гарантией Codex CLI slash command.
Перед implementation/handoff зафиксируй минимум: `normalized_goal`, `definition_of_done`, `evidence_required`, `scope`, `non_goals`, safety/budget boundaries и proxy-signal denylist.
Если DoD нельзя безопасно вывести, задай один короткий уточняющий вопрос.
Если безопасно вывести defaults, назови defaults и продолжай route.
Не отмечай success по proxy signals alone.
Для long autonomous Codex work требуй feedback tools, budget guardrails, stop criteria и observation cadence.
```
