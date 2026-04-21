# Bug Report: internal prepare commands leaking into user instructions

## Слой
`factory-template`

## Симптом
После завершения internal repo work completion package мог отправлять пользователя запускать:
- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- `bash GENERATE_BOUNDARY_ACTIONS.sh`
- другие внутренние prepare/export команды

вместо того чтобы Codex сам выполнил эти шаги внутри repo и выдал пользователю только реальные внешние boundary actions.

## Почему это дефект
- Внутренние repo-операции принадлежат Codex, а не пользователю.
- Пользователь должен делать только внешние шаги: ChatGPT Project UI, GitHub UI, ручные загрузки, ввод секретов и другие manual actions вне IDE/SSH automation.
- Если completion package просит пользователя собирать export artifacts вручную, фабрика размывает границу между internal repo follow-up и external boundary action.

## Ожидаемое поведение
- Codex сам выполняет `export refresh`, `boundary-actions generation`, `manifest/archive refresh` и другую внутреннюю подготовку артефактов.
- В `## Инструкция пользователю` попадают только уже готовые пути, архивы, delete-before-replace правила и внешний upload/replace/review flow.

## Root Cause
Канонический source-update completion package требовал перечислять `Команды/скрипты для repo-level sync`, но не фиксировал достаточно жёстко, что внутренние prepare-команды должны выполняться Codex до финального ответа.

## Remediation
- Явно зафиксировать это правило в router, decision policy, handoff rules, done-closeout, runbook и AGENTS.
- Обновить boundary-actions template и codex-task-pack generation/validation так, чтобы generated guidance помечал prepare-команды как внутреннюю работу Codex.

## Проверка
- Проверить, что generated `boundary-actions.md` говорит о готовых артефактах, а не требует от пользователя запускать internal prepare-команды.
- Проверить, что validator ловит отсутствие маркера о выполнении prepare-команд Codex внутри repo.
