## Применение в Codex UI

- Apply mode: `manual-ui` (default).
- Откройте новый чат/окно Codex и вручную выберите model/reasoning в picker.
- новый чат + вставка handoff и executable path через launcher — не одно и то же.
- Надежная единица маршрутизации: `new task launch`.
- advisory/handoff text != executable profile switch.
- Advisory/handoff text не переключает profile/model/reasoning в уже открытой сессии.
- Если после manual UI apply проявился sticky last-used state, закройте текущую сессию и запустите новый task launch.

## Строгий launch mode (опционально)

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
```

## Handoff в Codex

```text
CODEX HANDOFF

launch_source: chatgpt-handoff
task_class: feature-hardening
selected_profile: release-hardening
selected_model: gpt-5.2-codex
selected_reasoning_effort: high
project_profile: factory-template
selected_scenario: release-2.5/track-a/foundation-hardening
pipeline_stage: remediation
artifacts_to_update:
  - .github/workflows/ci.yml
  - .github/workflows/release.yml
  - .github/dependabot.yml
  - SECURITY.md
  - CODEOWNERS
  - requirements.txt
  - requirements.lock
  - template-repo/scripts/verify-all.sh
  - TEST_REPORT.md
  - RELEASE_CHECKLIST.md
handoff_allowed: true
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

Objective:
Harden engineering baseline for 2.5 while preserving repo-first and routing/handoff validation semantics.
```
