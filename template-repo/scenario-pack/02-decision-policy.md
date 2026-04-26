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
- brownfield source-candidate map / reconstruction allowlist / reconstruction denylist / change-map;
- closeout artifact sync;
- verify-summary / done-summary / release-facing consistency pass;
- release bundle preparation.

Если такой следующий шаг уже назван, route совместим и он выполняется внутри repo доступными инструментами Codex, нельзя завершать ответ просьбой пользователя "продолжить". Нужно выполнить шаг в текущем task или выдать inline handoff только когда действительно нужен новый task launch.

Если completed change затрагивает downstream-consumed content, после классификации internal/external/mixed follow-up дополнительно классифицируй impact по update contours:
- `impact.factory_sources`
- `impact.downstream_template_sync`
- `impact.downstream_project_sources`
- `impact.manual_archive_required`
- `impact.delete_before_replace`

Для каждого флага нужно явно определить:
- `да`
- `нет`
- `не применяется`

Если хотя бы один contour требует внешнего действия, финальный `## Инструкция пользователю` должен явно включать:
- что изменено;
- какие файлы обновлены в repo;
- какие update contours затронуты;
- какие артефакты/архивы уже готовы;
- что удалить перед заменой;
- пошаговую маршрутизацию по окнам и папкам;
- что прислать обратно после внешнего шага.

Под `уже готовы` понимаются артефакты, которые Codex предварительно собрал сам внутри repo до финального ответа. Пользовательский блок не должен требовать запускать внутренние export/generate команды, если их можно и нужно выполнить в том же change внутри repo.

Если по итогам шага 4 нужен следующий шаг пользователя, внешний шаг, загрузка артефактов, действие в GitHub UI, действие в ChatGPT Project UI, risky confirmation, возврат после verify/release decision или ожидание следующего артефакта, сформулируй этот шаг в обязательном финальном блоке `## Инструкция пользователю`.

## Классификация дефекта
Каждый найденный defect должен быть отнесен к одному из слоев:
- `project-only`
- `factory-template`
- `shared/unknown`

Если есть `factory-template` или `shared/unknown`, нужно подготовить factory feedback.
