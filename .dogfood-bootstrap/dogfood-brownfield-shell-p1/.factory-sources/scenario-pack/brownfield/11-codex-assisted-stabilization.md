# Сценарий: codex-assisted stabilization

## Логика
1. Сначала facts-first и audit-only.
2. Затем определить safe zones.
3. Затем сделать минимальный обратимый stabilization fix.
4. Только после этого разрешать Codex более широкий execution contour.

## Обязательные условия для codex-led
- понятен rollback plan;
- есть acceptance criteria;
- изменяемая зона наблюдаема;
- зафиксированы evidence before/after;
- нет притворства, что reconstructed repo уже равен исходному repo.

## Что должен сделать ChatGPT Project перед handoff
- подготовить `codex-input.md` без пустых шаблонных секций;
- явно перечислить boundary actions для пользователя;
- отметить, какие проверки обязан прогнать Codex после правок.
