# Текущее функциональное состояние шаблона

## Что шаблон генерирует
- README, VERSION, CHANGELOG, CURRENT_FUNCTIONAL_STATE
- `.chatgpt` с state, presets и defect-flow
- greenfield и brownfield каркас
- reports и tasks для defect-aware работы

## Какие режимы поддерживаются
- greenfield
- brownfield

## Что делает launcher
- создает working project
- применяет presets
- подставляет версию фабрики и project origin
- создает начальный versioning layer
- добавляет release decision template и reusable sync/release scripts
- копирует executable routing contract: `codex-routing.yaml`, router scripts и named Codex profiles
- подготавливает generated project к launch-time self-handoff и routing verification
- direct-task contour теперь включает отдельный visible response artifact для стартового self-handoff
- smoke и pre-release layer теперь прикрывают наличие этого visible direct-task response artifact

## Что еще описано на уровне фабрики
- единая визуальная архитектура шаблона и подробные workflows по запуску, развёртыванию и downstream-update contour

## Ограничения
- содержательное наполнение versioning файлов после генерации выполняется пользователем или сценариями
- matrix runner и bugflow требуют рабочей оболочки bash/pyyaml
- auto GitHub Release publication в generated project зависит от доступности и авторизации `gh`
- выбор `task_class` пока делается по эвристике keyword matching, а не по semantic classifier
