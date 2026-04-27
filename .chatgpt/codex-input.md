CODEX HANDOFF — DOWNSTREAM MULTI-CYCLE SYNC PROOF

launch_source: chatgpt-handoff
task_class: downstream-sync-validation
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
project_profile: factory-template
selected_scenario: post-2.5/downstream-multi-cycle-sync
pipeline_stage: audit → evidence → remediation-if-needed
handoff_allowed: true
defect_capture_path: reports/bugs/YYYY-MM-DD-downstream-multi-cycle-sync-gap.md

Язык ответа Codex: русский.

ЦЕЛЬ: Доказать, что downstream sync v3 выдерживает несколько циклов: initial template sync, manual project-owned edits, advisory review, safe-generated update, safe-clone update, rollback, brownfield transition → greenfield conversion.

АРТЕФАКТЫ ОБНОВИТЬ:
- docs/downstream-upgrade-policy.md
- reports/release/downstream-multi-cycle-sync-report.md
- factory/producer/extensions/workspace-packs/factory-ops/*
- MATRIX_TEST.sh
- TEST_REPORT.md
- CURRENT_FUNCTIONAL_STATE.md

ЗАДАЧИ:
1. Создать synthetic downstream fixture для multi-cycle sync.
2. В цикле 1 применить safe-generated/safe-clone.
3. В цикле 2 сделать manual project-owned edits.
4. В цикле 3 обновить template-owned files и проверить project-owned не перезаписан, advisory-review не применён автоматически, rollback metadata корректна.
5. В цикле 4 проверить rollback.
6. В отдельном сценарии проверить brownfield converted_greenfield.
7. Обновить report и TEST_REPORT.

Дополнительно учесть Stage 5: проверить production VPS field pilot docs/scripts/reports как template-owned/safe или advisory зоны без перезаписи project-owned runtime env/secrets: deploy/.env, .factory-runtime/, field-pilot reports, backup/rollback transcripts и real VPS approval boundary.

КРИТЕРИИ ПРИЕМКИ:
- Multi-cycle sync report есть и честен.
- Project-owned изменения защищены.
- Advisory-review требует ручного review.
- Rollback работает после нескольких циклов.
- Brownfield history сохраняется после conversion.
- bash template-repo/scripts/verify-all.sh ci проходит.

COMPLETION PACKAGE:
В финале указать downstream/battle repo sync commands, что safe to apply, что review-only, что manual-only, требуется ли ChatGPT Project Sources fallback, и Реестр внешних действий по контурам: factory-template ChatGPT Project, downstream repo sync, downstream ChatGPT Project, real VPS/user approval, secrets/manual boundary.
