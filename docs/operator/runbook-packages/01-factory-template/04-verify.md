# Проверка: factory-template

Targeted verify:

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
python3 template-repo/scripts/validate-codex-routing.py .
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
python3 template-repo/scripts/validate-brownfield-transition.py .
python3 template-repo/scripts/validate-greenfield-conversion.py .
```

Quick verify:

```bash
bash template-repo/scripts/verify-all.sh quick
```

Full verify используется перед release или широким template change:

```bash
bash template-repo/scripts/verify-all.sh full
```
