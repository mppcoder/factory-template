# Проверка: greenfield-product

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

Из factory-template root для проверки package layer:

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
```

Из generated project root после materialization:

```bash
python3 scripts/validate-project-preset.py .
python3 scripts/validate-greenfield-conversion.py .
python3 scripts/validate-codex-routing.py .
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```

Если проект был converted из brownfield, добавьте:

```bash
python3 scripts/validate-greenfield-conversion.py . --require-converted
```
