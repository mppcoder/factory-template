# Factory Feedback: VS Code Codex extension needs UI-first handoff by default

## Исходный bug report
`reports/bugs/bug-018-vscode-codex-manual-ui-default-gap.md`

## Почему это проблема фабрики
Фабрика уже различала advisory/policy layer и executable routing layer, но user-facing completion/handoff слой подавал launcher-first path как обязательный default даже там, где реальный UX VS Code Codex extension естественно строится вокруг manual picker selection в новом окне/чате. Это reusable defect не поведения пользователя, а самого шаблонного default UX.

## Где проявилось
`factory-template`, scenario-pack, routing spec, launcher helpers, generated `.chatgpt` handoff/completion artifacts и source-facing docs для Codex/VS Code Codex extension.

## Повторяемый паттерн
- profile/model/reasoning уже выбраны и зафиксированы в routing artifacts;
- user работает через окно VS Code Codex extension;
- template все равно заставляет идти в terminal и запускать launcher как default;
- UX становится тяжелее, чем ручной выбор model/reasoning в UI;
- пользователь путается между `новый чат + вставка handoff` и `new task launch через executable launcher`;
- live session auto-switch по-прежнему не гарантирован, но именно это distinction шаблон показывал неудачно.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- scenario-pack и routing guidance
- `codex-routing.yaml`
- bootstrap / launcher / routing renderers
- validators для handoff/completion response
- generated `.chatgpt` artifacts
- source-facing docs/runbooks/templates

## Как проверить исправление
1. Сгенерировать `.chatgpt/handoff-response.md` и убедиться, что первым default path идет `manual-ui`, а launch command вынесен в optional strict section.
2. Проверить, что `.chatgpt/task-launch.yaml` и normalized handoff содержат `apply_mode: manual-ui` и `strict_launch_mode: optional`.
3. Проверить, что handoff docs прямо различают:
   `новый чат + вставка handoff`
   `new task launch через executable launcher`
4. Проверить, что source-facing docs больше не подают terminal launcher как обязательный default для интерактивного VS Code Codex extension workflow.
5. Проверить, что docs и validators по-прежнему прямо говорят: уже открытая live session не является надежным auto-switch mechanism.

## Статус
зафиксировано
