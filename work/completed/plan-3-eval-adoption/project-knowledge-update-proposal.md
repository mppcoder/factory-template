# Project Knowledge update proposal: plan-3-eval-adoption

## Status

- status: required
- justification: В decisions.md есть follow_up или устойчивые решения, которые нужно рассмотреть для переноса.

## Proposed updates

- `project-knowledge/deployment.md`: перенести устойчивый вывод из decisions.md после человеческой проверки формулировки.
- `project-knowledge/patterns.md`: перенести устойчивый вывод из decisions.md после человеческой проверки формулировки.

## Source decisions

- - Записывайте только решения, которые помогут будущему участнику понять, почему работа сделана именно так.
- - Если задача отклонилась от user-spec, укажите связанный `DEV-*` и `US-*`.
- - Если решение стало устойчивым правилом проекта, перенесите вывод в `project-knowledge/`.
- - Для feature-execution-lite фиксируйте wave, review rounds и boundary: internal work, external user action или runtime backlog.
- - 2026-04-27 — Wave 1 closed: Artifact Eval expansion uses the existing repo-native harness rather than adding a new evaluator.
- - execution_wave: 1
- - review_rounds: 1
- - boundary: internal work completed; no runtime proof claimed.

## Follow-up candidates

- P3-S5 should prepare pre/post deploy QA boundaries without mutating real VPS unless separately approved.
