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

## Ограничения
- содержательное наполнение versioning файлов после генерации выполняется пользователем или сценариями
- matrix runner и bugflow требуют рабочей оболочки bash/pyyaml
