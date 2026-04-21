# Передача в Codex (handoff)

Перед handoff проверь:
- готов ли `codex-input.md`;
- заполнен ли `evidence-register.md`;
- закрыт ли `codex_handoff_allowed` в `stage-state.yaml`;
- валиден ли `task-index.yaml`.

## Обязательное правило inline handoff
Если handoff уже допустим и задача достаточно определена, handoff нужно выдать в том же ответе. Нельзя останавливаться на аналитике, если change-class требует handoff или если optional handoff уже безопасно нормализуется.

Post-remediation follow-up handoff тоже является нормальным и обязательным handoff case, если remaining work еще остается внутренней Codex-eligible работой repo.

Допустимые типы такого handoff включают:
- `release-followup`
- `closeout-sync`
- `release-facing-consistency`
- `source-pack-refresh`
- `export-refresh`

Допустимые причины отложить handoff:
- обязательные gate'ы еще не закрыты;
- не хватает обязательных артефактов;
- задача остается реально неоднозначной;
- нужен выбор архитектурной развилки.

## Минимальная структура handoff-блока
Готовый handoff в Codex должен как минимум содержать:
- цель изменения;
- границы scope и что не делать;
- список обязательных артефактов и файлов для обновления;
- verify expectations;
- риски и ограничения;
- указание, нужен ли defect/factory feedback follow-up.

## После handoff
Если remaining work еще внутренний и Codex-eligible, handoff должен быть выдан раньше любого user footer.

Сразу после handoff, если дальше нужен внешний шаг пользователя, возврат в ChatGPT Project, внешнее действие или ожидание внешнего артефакта, добавь финальный раздел `## Инструкция пользователю`.
