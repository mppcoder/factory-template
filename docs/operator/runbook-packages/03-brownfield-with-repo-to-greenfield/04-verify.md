# Проверка: путь с существующим repo

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

До conversion:

```bash
python3 scripts/validate-brownfield-transition.py . --with-repo
```

После conversion:

```bash
python3 scripts/validate-greenfield-conversion.py . --require-converted
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```

Из factory-template root package coverage проверяется так:

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
python3 template-repo/scripts/validate-brownfield-transition.py .
python3 template-repo/scripts/validate-greenfield-conversion.py .
```
