# Пользовательская спецификация

## Цель изменения
- Исправить reusable process gap в `factory-template`, из-за которого internal repo follow-up после remediation/push мог ошибочно уходить в user-only closeout.
- Сохранить обязательный footer `Инструкция пользователю` для реальных внешних границ.
- Не менять release semantics и не превращать closeout в automatic release.

## Что должно получиться
- Если remaining work еще выполняется внутри repo и остается Codex-eligible, ответ обязан выдавать inline handoff.
- User-only closeout допустим только для реальных external boundary steps.
- При mixed follow-up сначала идет inline handoff на внутреннюю часть, затем при необходимости отдельный footer для внешней границы.

## Что не входит в объем
- Автопубликация релиза.
- Широкий rewrite всей фазовой модели.
- Ослабление правила обязательного footer для внешних шагов.
