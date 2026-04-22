# Release Note Template

Этот файл больше не является опубликованным release notes source.
Канонические notes для текущего релиза находятся в `RELEASE_NOTES.md`.
Используйте этот файл только как черновой шаблон для подготовки следующего релиза.

## Draft Fields

- Версия: `X.Y.Z`
- Дата: `YYYY-MM-DD`
- Статус: `draft|published`

## Что вошло

- краткое описание цели релиза;
- список ключевых functional / architecture / workflow / release-layer изменений;
- что важно для downstream;
- какие команды проверки использовались;
- какие ограничения или manual fallback остаются.

## Минимальная структура

1. О чём этот релиз
2. Что вошло
3. Что изменилось в template/runtime/policy layer
4. Что важно для downstream
5. Что проверено
6. Риски и ограничения
7. Внешние шаги для пользователя
8. Go / No-Go

## Публикация

- Для `release-decision.yaml` в поле `notes_source` используйте `RELEASE_NOTES.md`.
- Не дублируйте опубликованные notes в этом файле после выпуска релиза.
