# Проверка: factory-template

Проверка подтверждает не только наличие package files, но и beginner zero-to-Codex-ready flow: `USER-ONLY SETUP`, `CODEX-AUTOMATION`, `codex-app-remote-ssh`, `vscode-remote-ssh-codex-extension`, `Codex takeover point`, обязательные `FT-*` шаги и copy-paste step format.

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
