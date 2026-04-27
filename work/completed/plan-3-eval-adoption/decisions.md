# Decisions Log: Plan 3 Artifact Eval Adoption

> generated_at: 2026-04-27T12:21:06+03:00
> feature_id: plan-3-eval-adoption
> Этот файл хранит важные решения, отклонения и проверки после выполнения задач.

## Как пользоваться

- Записывайте только решения, которые помогут будущему участнику понять, почему работа сделана именно так.
- Если задача отклонилась от user-spec, укажите связанный `DEV-*` и `US-*`.
- Если решение стало устойчивым правилом проекта, перенесите вывод в `project-knowledge/`.
- Для feature-execution-lite фиксируйте wave, review rounds и boundary: internal work, external user action или runtime backlog.

## Записи

- 2026-04-27 — Wave 1 closed: Artifact Eval expansion uses the existing repo-native harness rather than adding a new evaluator.
  - execution_wave: 1
  - review_rounds: 1
  - boundary: internal work completed; no runtime proof claimed.
  - evidence: `tests/artifact-eval/specs/*` and `tests/artifact-eval/reports/*`.

- 2026-04-27 — Wave 2 closed: feature-execution-lite adoption remains a repo-level factory workspace.
  - execution_wave: 2
  - review_rounds: 1
  - boundary: `work/features/plan-3-eval-adoption` is valid; `template-repo/work` is not used for this factory change.
  - evidence: `logs/checkpoint.yaml`, task files and closeout validator commands.

- 2026-04-27 — Runtime QA remains out of scope for this feature.
  - execution_wave: final
  - review_rounds: 1
  - boundary: runtime backlog for P3-S5 only; dry-run/report-ready is not production proof.
  - follow_up: P3-S5 should prepare pre/post deploy QA boundaries without mutating real VPS unless separately approved.
