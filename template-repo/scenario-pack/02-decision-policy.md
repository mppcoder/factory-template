# Политика принятия решений

## Шаг 1. Проверка повторного использования
Сначала проверь, нет ли уже похожего решения в проекте.

## Шаг 2. Проверка реальности
Затем проверь текущее состояние проекта, документацию и реальные кейсы.

## Шаг 3. Выявление конфликтов
Проверь, не ломает ли новое решение уже известные workaround'ы и ограничения.

## Шаг 4. Формирование вывода
Только после шагов 1–3 можно предлагать решение и готовить handoff.

Если обязательные gate'ы и артефакты уже достаточны для handoff, результатом шага 4 должен быть не только вывод, но и нормализованный handoff в Codex в том же ответе.

Если handoff policy = `required`, ответ без готового handoff считается незавершенным.

Если handoff policy = `optional`, но данных уже достаточно для безопасного handoff, по умолчанию тоже выдай handoff сразу, если нет явной причины его отложить.

После формирования вывода обязательно классифицируй remaining next step в один из режимов:
- `internal follow-up pending`
- `external boundary pending`
- `mixed follow-up`
- `fully done`

`internal follow-up pending` означает, что remaining work еще выполняется внутри repo и остается Codex-eligible. В этом случае user-only closeout запрещен, а результат шага 4 обязан содержать inline handoff в Codex.

`external boundary pending` означает, что remaining work действительно находится вне repo и требует действия в UI, загрузки, секрета или другого manual шага вне IDE/SSH. В этом случае допустим closeout без handoff, но с обязательным блоком `## Инструкция пользователю`.

`mixed follow-up` означает, что сначала остаются внутренние repo-задачи, а после них возможен внешний шаг. В этом случае сначала выдай inline handoff в Codex на внутреннюю часть, а затем добавь блок `## Инструкция пользователю` только для внешней границы.

К `internal follow-up pending` по умолчанию относятся release-followup и closeout-sync задачи внутри repo:
- release notes / release-facing changelog entries;
- source-pack / curated sources refresh;
- export / manifests refresh;
- closeout artifact sync;
- verify-summary / done-summary / release-facing consistency pass;
- release bundle preparation.

Если по итогам шага 4 нужен следующий шаг пользователя, внешний шаг, загрузка артефактов, действие в GitHub UI, действие в ChatGPT Project UI, risky confirmation, возврат после verify/release decision или ожидание следующего артефакта, сформулируй этот шаг в обязательном финальном блоке `## Инструкция пользователю`.

## Классификация дефекта
Каждый найденный defect должен быть отнесен к одному из слоев:
- `project-only`
- `factory-template`
- `shared/unknown`

Если есть `factory-template` или `shared/unknown`, нужно подготовить factory feedback.
