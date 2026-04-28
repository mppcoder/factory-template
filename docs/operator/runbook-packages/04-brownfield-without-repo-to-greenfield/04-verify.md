# Проверка: путь без repo

Intake/reconstruction gate:

```bash
python3 scripts/validate-brownfield-transition.py . --without-repo
```

With-repo adoption gate:

```bash
python3 scripts/validate-brownfield-transition.py . --with-repo
```

Conversion gate:

```bash
python3 scripts/validate-greenfield-conversion.py . --require-converted
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```

Package layer verify из factory-template root:

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
```
