task_class: build
selected_scenario: 12-bug-analysis.md + 14-docs-normalization.md + 15-handoff-to-codex.md
pipeline_stage: remediation
artifacts_to_update:
  - docs/releases/2.5-roadmap.md
  - docs/releases/2.5-success-metrics.md
  - CURRENT_FUNCTIONAL_STATE.md
  - README.md
  - RELEASE_CHECKLIST.md
  - PRE_RELEASE_AUDIT.sh
  - template-repo/scripts/verify-all.sh
  - docs/releases/release-scorecard.yaml
  - template-repo/scripts/validate-release-scorecard.py
  - TEST_REPORT.md
  - reports/bugs/2026-04-25-release-truth-drift.md
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation -> verification

HANDOFF: FT-2.5.1-release-truth

Objective:
Свести в единый источник истины состояние релиза 2.5+, устранить drift между roadmap/current-state/README, добавить machine-readable release scorecard и включить его в pre-release/CI gates.

Scope:
- Синхронизировать docs/releases/2.5-roadmap.md, CURRENT_FUNCTIONAL_STATE.md, README.md, RELEASE_CHECKLIST.md.
- Создать единый файл release-scorecard.yaml или release-scorecard.json.
- Добавить в PRE_RELEASE_AUDIT.sh и verify-all.sh проверку согласованности release state.
- Обновить TEST_REPORT.md template/source-of-truth strategy так, чтобы статус релиза не зависел только от вручную обновляемого markdown.

Acceptance criteria:
- roadmap/current-state/README описывают одну и ту же стадию релиза без противоречий
- release-scorecard существует и заполняется однозначно
- PRE_RELEASE_AUDIT.sh падает при несогласованности release документов
- verify-all.sh ci включает проверку release-scorecard
- добавлен короткий human-readable раздел “How to read release truth”

Defect capture path:
reports/bugs/YYYY-MM-DD-release-truth-drift.md
