# Контур Artifact Eval Harness

Artifact Eval Harness — optional advanced контур для deterministic desk-eval prompt-like artifacts. Он нужен maintainers factory-template, когда меняются scenario-pack, handoff blocks, runbooks, policy docs, template skills или advanced execution artifacts.

Beginner path не меняется: первый проект, guided launcher и обычный feature flow не требуют artifact eval.

## Что проверяет

Harness проверяет не модельный transcript, а сам reusable artifact:

- есть ли понятный trigger-positive route;
- есть ли trigger-negative / non-trigger границы;
- делает ли guided artifact результат лучше, чем unguided baseline;
- покрыты ли process, outcome и compliance assertions;
- не потеряны ли repo-first, handoff, defect-capture и beginner-path boundaries;
- для `feature-execution-lite` есть ли execution-plan, checkpoint/resume, decisions, task waves и final verification evidence.

После Plan №3 P3-S3 smoke-набор также покрывает routing-critical границы:

- direct task self-handoff;
- normalized Codex handoff response;
- done/closeout external actions ledger;
- downstream sync boundary;
- production VPS proof boundary;
- feature-execution-lite final verification negative cases.

После Plan №4 P4-S3 smoke-набор дополнительно покрывает handoff transcript eval для real ChatGPT->Codex handoff output:

- one copy-paste block, not file references or multiple fragments;
- Russian user-facing response with `Язык ответа Codex: русский`;
- required routing fields from repo handoff contract;
- no file-based handoff;
- no vague continue as a substitute for a concrete task;
- no false auto-switch claims: advisory/policy layer and executable routing layer stay separate;
- `## Инструкция пользователю` only when real external action exists;
- negative fixture: multi-block handoff;
- negative fixture: no next step after internal follow-up remains;
- negative fixture: user-only closeout for repo-internal work.

## Спецификация

Минимальный YAML:

```yaml
schema: artifact-eval/v1
id: master-router-routing
report_date: 2026-04-27
target_artifact: template-repo/scenario-pack/00-master-router.md
artifact_type: scenario-pack
expected_trigger:
  cases:
    - id: direct-task-self-handoff
      prompt: "Codex получил прямую задачу без внешнего handoff"
      expected: "Сначала self-handoff, затем remediation"
      assertions:
        - id: requires-self-handoff
          category: process
          must_contain:
            - "Правило прямой задачи"
non_trigger_cases:
  - id: live-session-is-not-router
    prompt: "Уже открытая live session должна сама сменить profile/model"
    expected: "Artifact не обещает auto-switch"
    assertions:
      - id: no-auto-switch
        category: compliance
        must_contain:
          - "advisory слой сам по себе переключает модель"
        must_not_contain:
          - "уже открытая сессия надежно переключает модель"
expected_output:
  guided: "Ответ фиксирует профиль, сценарий, этап, artifacts и handoff status."
compliance_assertions:
  - id: required-start-fields
    category: compliance
    must_contain:
      - "выбранный профиль проекта"
thresholds:
  min_case_pass_rate: 0.8
  min_assertion_pass_rate: 0.85
  max_false_positive_rate: 0.25
```

Поддерживаемые поля:

- `target_artifact` — путь к проверяемому artifact.
- `artifact_type` — `scenario-pack`, `handoff-block`, `runbook`, `policy-doc`, `prompt-like`, `template-skill`, `advanced-execution`.
- `expected_trigger.cases` — positive trigger/use cases.
- `non_trigger_cases` — соседние negative cases.
- `expected_output.guided` — ожидаемая польза guided artifact.
- `process_assertions`, `outcome_assertions`, `compliance_assertions` — глобальные checks.
- `thresholds` — pass/fail пороги.

Assertions поддерживают `must_contain`, `must_contain_any`, `must_not_contain`, `regex_contains`, `regex_not_contains`.

## Запуск

```bash
python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/master-router.yaml --output /tmp/master-router-eval.md
python3 template-repo/scripts/validate-artifact-eval-report.py /tmp/master-router-eval.md
```

Static sample reports лежат в `tests/artifact-eval/reports/`. Они нужны как example evidence, routing-critical evidence и validator fixtures.

## Порог

Default thresholds:

- `case_pass_rate >= 80%`;
- `assertion_pass_rate >= 80%`;
- `false_positive_rate <= 20%`.

Для routing-critical artifacts лучше указывать `assertion_pass_rate >= 0.85` или выше.

## Связь с skill-tester-lite

`skill-tester-lite` остаётся лёгким ручным skill для create-test-improve loop. Artifact Eval Harness — его machine-readable extension для maintainers, когда нужен durable report и quick-safe smoke.

Из исходного `skill-tester` перенесены только lightweight идеи:

- trigger-positive / trigger-negative cases;
- baseline vs guided comparison;
- process / outcome / compliance assertions;
- pass-rate thresholds;
- compact report.

Не перенесены Claude-specific runners, parallel teams, transcript graders и timing capture.

## Advanced execution target для feature-execution-lite

Для `feature-execution-lite` eval target должен проверять, что docs или templates явно покрывают:

- `logs/execution-plan.md`;
- `logs/checkpoint.yaml`;
- `decisions.md`;
- `tasks/T-xxx.md`;
- wave dependencies;
- review/fix rounds;
- internal / external / runtime boundaries;
- final verification evidence before done/archive.

Это optional advanced contour. Он не должен становиться required step для маленьких first-time задач.
