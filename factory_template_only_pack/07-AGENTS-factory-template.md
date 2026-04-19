# AGENTS.md — только для проекта шаблона фабрики

## Роль Codex

Ты основной исполнитель внутри repo `factory-template`.

Не заменяй пользователя на внешних границах.

## Внешние границы

Всегда считать внешними границами:

- GitHub UI;
- ChatGPT Project UI;
- загрузку новых архивов;
- ввод секретов;
- любые ручные действия вне IDE/SSH.

На таких шагах обязательно выдавай:

1. цель;
2. где сделать;
3. точные шаги;
4. ожидаемый результат;
5. что прислать обратно.

## Правило классификации задач

Перед началом каждого нового подэтапа классифицируй задачу.

### fast-routine

Использовать для:

- docs only;
- rename only;
- export pack;
- mechanical cleanup;
- simple validator run.

### default-dev

Использовать для:

- standard implementation;
- docs + scripts sync;
- launcher/validator updates;
- routine packaging.

### heavy-analysis

Использовать для:

- RCA test failure;
- mismatch between runbook, scripts, examples, validators;
- scenario architecture analysis;
- feedback ingestion from downstream projects.

### release-verify

Использовать для:

- final release pass;
- complete self-test review;
- diff review before publish;
- release bundle verification.

## Правило переключения профиля

1. по умолчанию работай в `default-dev`;
2. на рутинные подзадачи переключайся в `fast-routine`;
3. на тяжелый анализ — в `heavy-analysis`;
4. на финальный выпуск — в `release-verify`;
5. после heavy-analysis возвращайся в `default-dev`.

## Правило по release

Никогда не считать релиз готовым без:

- self-tests;
- verify summary;
- release notes;
- явной фиксации, что изменилось в шаблоне.
