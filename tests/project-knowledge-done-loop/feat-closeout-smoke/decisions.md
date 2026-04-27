# Decisions Log: Closeout smoke

> feature_id: feat-closeout-smoke

## Записи

### T-001 — Closeout smoke

- status: done
- execution_wave: 1
- review_rounds: 0/3
- boundary: internal_work
- user_intent: US-001
- summary: Closeout должен создавать отдельный Project Knowledge proposal, а не молча терять decisions после archive.
- decision: Feature closeout хранит done-report, project-knowledge-update-proposal и downstream-impact рядом с archived workspace.
- deviations: Нет
- verification:
  - smoke: `validate-project-knowledge-update.py` на archived workspace
  - user: Не требуется
- follow_up: Добавить правило closeout loop в `project-knowledge/patterns.md`.
