## Self-handoff для прямой задачи

## Классификация
direct-task

## Выбранный профиль проекта
unknown-project-profile

## Выбранный сценарий
00-master-router.md

## Текущий этап pipeline
done

## Класс задачи
build

## Выбранный профиль
build

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
medium

## Режим применения
manual-ui

## Ручное применение через UI
- Откройте новый чат/окно Codex.
- Вручную выберите model `gpt-5.5` и reasoning `medium` в picker.
- Только после этого продолжайте работу по self-handoff.
- Уже открытая live session не является надежным auto-switch boundary.

## Строгий режим запуска
optional

## Артефакты для обновления
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md
- reports/bugs/
- reports/factory-feedback/

## Разрешение handoff
yes (forbidden)

## Маршрут defect-capture
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Источник запуска
direct-task

## Правило launch boundary
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Правило интерактивного режима по умолчанию
Для интерактивной работы в VS Code Codex extension основной пользовательский путь: открыть новое окно/чат Codex, вручную выбрать model/reasoning в picker и затем вставить handoff.

## Правило executable switch
Строго воспроизводимое executable-переключение в live Codex для этого repo: явный новый task launch через launcher и selected_profile.

## Правило строгого запуска
Launcher-first path остается опциональным строгим режимом для автоматизации, воспроизводимости, запуска из shell и scripted launch.

## Правило fallback для live session
Уже открытая live session не является надежным механизмом автопереключения profile/model/reasoning и допустима только как неканонический fallback.

## Правило ожиданий по модели
selected_model и selected_reasoning_effort фиксируют ожидаемую конфигурацию выбранного executable profile; advisory handoff text сам по себе ничего не переключает.

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Сценарии для строгого запуска
- автоматизация
- воспроизводимость
- запуск из shell
- scripted launch

## Прямая команда Codex за launcher
`codex --profile build`

## Диагностика проблем
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это неканонический путь: route может остаться устаревшим.
- Если нужна строгая воспроизводимость, автоматизация или запуск из shell, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте именованный profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.

## Текст задачи
Исправить два process defects в factory-template: не перекладывать доступный GitHub PR merge на пользователя и обеспечить русский язык человекочитаемых текстов, отчетов, инструкций, closeout и generated guidance; пройти defect-capture, remediation, verify и closeout.

## Следующий шаг
Только после этого блока допустимы remediation / implementation / verification.
