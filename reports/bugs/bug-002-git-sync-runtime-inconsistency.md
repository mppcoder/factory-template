# Отчет о дефекте

## Идентификатор
bug-002-git-sync-runtime-inconsistency

## Краткий заголовок
В текущем агентном runtime зависимые git-команды могут давать ложные результаты синхронизации с GitHub.

## Где найдено
Repo: `factory-template`, среда агентного исполнения команд в `/projects/factory-template`

## Шаги воспроизведения
1. Настроить `origin` на SSH remote GitHub.
2. Выполнить зависимые git-шаги нестрого последовательно, например рядом с commit/push/fetch или сразу после смены remote.
3. Сравнить ожидаемое поведение с фактическим выводом `git push`.

## Ожидаемое поведение
`git push origin main` должен стабильно использовать SSH remote из `.git/config` и публиковать актуальный локальный commit.

## Фактическое поведение
В отдельных запусках наблюдались ложные или несогласованные результаты:

- `fatal: could not read Username for 'https://github.com': No such device or address`, хотя `origin` уже был настроен на SSH
- `Everything up-to-date`, хотя локальная ветка фактически оставалась `ahead 1`

## Evidence
- [PROJECT] `git remote -v` и `git remote show origin` подтверждали SSH remote `git@github.com:mppcoder/factory-template.git`
- [PROJECT] `.git/config` не содержал `pushurl`, `insteadOf` или других rewrite-настроек
- [PROJECT] прямой push по SSH-URL `git push git@github.com:mppcoder/factory-template.git main` проходил успешно
- [PROJECT] локальная проверка после неуспешных запусков показывала состояние `## main...origin/main [ahead 1]`

## Затронутый слой
shared-unknown

## Нужен ли feedback в фабрику
Да, потому что дефект влияет на рабочий протокол сопровождения шаблона и публикации изменений.

## Временный обход
- выполнять `git add`, `git commit`, `git push`, `git fetch`, `git remote set-url` только последовательно
- при нестабильном `git push origin main` использовать прямой SSH push:
  `git push git@github.com:mppcoder/factory-template.git main`

## Граница ответственности
Предварительный вывод: это похоже не на дефект git-конфига самого repo `factory-template`, а на runtime/tooling issue среды исполнения команд.

## Статус
зафиксировано, workaround есть, окончательно не исправлено
