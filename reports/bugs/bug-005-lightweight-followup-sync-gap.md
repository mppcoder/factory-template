# Отчет о дефекте

## Идентификатор
bug-005-lightweight-followup-sync-gap

## Краткий заголовок
Verified sync не покрывал low-risk post-verify follow-up cleanup и оставлял такие изменения на ручном commit/push.

## Где найдено
Repo: `factory-template`, reusable automation / operator behavior layer:

- verified sync follow-up behavior
- docs/runbook/AGENTS guidance

## Ожидаемое поведение
- После уже зафиксированного green verify low-risk `.gitignore` и docs/closeout cleanup должны auto sync через тот же canonical verified path.
- Codex не должен спрашивать отдельное подтверждение на commit/push для такого lightweight follow-up.

## Фактическое поведение
- Основной verified sync path работал для полного change cycle.
- Маленькие post-verify cleanup изменения оставались в серой зоне между "verify уже есть" и "новый полноценный change cycle не нужен".
- В результате Codex мог спросить про отдельный commit/push вместо немедленного auto sync.

## Evidence
- [PROJECT] `VERIFIED_SYNC.sh` ранее всегда строил commit message из текущего `task-index`, что было некорректно для follow-up cleanup поверх уже завершенного change.
- [PROJECT] Runbook и AGENTS не фиксировали lightweight follow-up path как каноническое поведение.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что gap найден и закрывается в source-of-truth repo самой фабрики.

## Статус
исправлен
