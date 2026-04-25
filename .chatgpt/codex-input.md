task_class: build
selected_profile: build
project_profile: factory-template
selected_scenario: 15-handoff-to-codex.md -> 14-docs-normalization.md -> implementation/remediation
pipeline_stage: implementation
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal; use reports/bugs/YYYY-MM-DD-skill-meta-qa-loop.md only for incidental/regression evidence
artifacts_to_update:
  - template-repo/skills/skill-master-lite/SKILL.md
  - template-repo/skills/skill-tester-lite/SKILL.md
  - template-repo/skills/skill-tester-lite/references/test-design-guide.md
  - template-repo/skills/skill-tester-lite/references/report-template.md
  - docs/skills-quality-loop.md
  - README.md

HANDOFF: FT-2.5.6-skill-meta-qa

Objective:
Добавить в factory-template облегчённый meta-QA цикл для skills и prompt-like artifacts:
создал -> протестировал -> улучшил trigger/usefulness.

Scope:
- Адаптировать идеи skill-master/skill-tester под нужды factory-template.
- Не переносить весь comparison repo; собрать только минимально полезный контур.
- Сделать это опциональным advanced mode, не обязательным слоем для новичка.

Acceptance criteria:
- существует documented optional workflow для тестирования skills/prompt artifacts
- workflow отделён от beginner default path
- есть минимум один пример использования на артефакте factory-template
- docs объясняют value простым языком: "это для улучшения шаблона, а не обязательный шаг новичка"

Model / reasoning effort suggestion:
GPT-5.2 Thinking
Reasoning effort: medium-high

Required roles / skills:
- prompt / skill design
- documentation
- evaluation design
- unspecified: если нужен отдельный evaluator/benchmark owner
