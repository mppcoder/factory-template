# Onboarding smoke fixtures / fixture'ы onboarding smoke

Этот каталог содержит novice-oriented E2E fixture для проверки beginner-first запуска.

Запуск:

```bash
bash tests/onboarding-smoke/run-novice-e2e.sh
```

Что делает runner:

- выполняет два wizard-сценария:
  - `greenfield-novice` (preset `greenfield-product`);
  - `brownfield-novice` (preset `brownfield-with-repo-modernization`);
- выполняет guided launcher сценарий:
  - `guided-launcher-greenfield` (preset `greenfield-product`);
- проверяет, что preset корректно записан в `.chatgpt/active-scenarios.yaml`;
- прогоняет baseline validators и codex-task-pack validators для каждого созданного проекта;
- формирует отчёт `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`.

Важно:

- проектные директории и логи создаются в `tests/onboarding-smoke/.tmp-run/`;
- runner очищает предыдущий `.tmp-run` при каждом запуске.
