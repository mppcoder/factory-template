# Фикстуры Universal Task Control

Negative fixtures here protect the repo-native `FT-TASK` contracts used by `verify-all quick`.

- `negative/task-registry/*.yaml` must fail `validate-task-registry.py`.
- `negative/codex-handoff/*.md` must fail `validate-codex-task-handoff.py`.

These fixtures are intentionally small and explicit so a reviewer can see which boundary each file covers without reading generated smoke code.
