# Factory feedback 035: user-spec audit should skip placeholder tech-spec

Дата: 2026-04-25
Источник: `reports/bugs/2026-04-25-user-spec-audit-placeholder-tech-spec.md`
Слой: `factory-template`
Статус: fixed in current scope

## Суть

Post-generation audit после `generate-user-spec.py` не должен требовать traceability от placeholder `tech-spec.md`, который создаётся заранее для удобства workspace.

## Устойчивое правило

Validator должен различать:
- placeholder template document с `{{...}}`, который ещё не является рабочим артефактом;
- заполненный рабочий документ, где отсутствие `US-*`, deviation record или verification path является настоящим дефектом.

