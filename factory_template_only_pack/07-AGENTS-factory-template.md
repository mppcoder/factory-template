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

Каноническое имя этого финального блока: `Инструкция пользователю`.

Если есть pending user/external step, ответ без финального блока `## Инструкция пользователю` считается неполным.

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
- release bundle verification;
- explicit release decision execution.

## Правило переключения профиля

1. по умолчанию работай в `default-dev`;
2. на рутинные подзадачи переключайся в `fast-routine`;
3. на тяжелый анализ — в `heavy-analysis`;
4. на финальный выпуск — в `release-verify`;
5. после heavy-analysis возвращайся в `default-dev`.

## Правило inline handoff

Если handoff в Codex уже разрешен и задача достаточно определена, выдай готовый handoff в том же ответе.

Если handoff обязателен по change-class, нельзя завершать ответ только аналитикой.

Если handoff опционален, но gate'ы и артефакты уже достаточны и handoff можно безопасно нормализовать, по умолчанию тоже выдай handoff сразу.

## Правило по release

Никогда не считать релиз готовым без:

- self-tests;
- verify summary;
- release notes;
- явной фиксации, что изменилось в шаблоне.

## Правило verified sync

После green verify используйте `VERIFIED_SYNC.sh` как канонический путь commit/push.

Требования:

- без green verify commit/push запрещены;
- при отсутствии diff sync должен завершаться как no-op;
- git-команды выполнять только последовательно;
- fallback push через прямой SSH допустим только как deterministic fallback, а не как silent branch.

## Правило release decision

Используйте отдельный `.chatgpt/release-decision.yaml`.

- `decision=no-release` означает только verified sync без tag/release;
- `decision=release` разрешает `EXECUTE_RELEASE_DECISION.sh`;
- auto release без явного decision запрещен.
