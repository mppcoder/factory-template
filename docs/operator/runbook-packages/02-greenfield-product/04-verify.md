# Проверка: greenfield-product

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

User readiness до takeover:

- project slug и GitHub repo/access определены;
- ChatGPT Project подключен к GitHub;
- remote Codex context открыт;
- Codex может выполнить remote shell command.

Codex automation после takeover:

- `/projects/<project-slug>` создан;
- greenfield docs заполнены;
- dashboard validates;
- generated quick verify green;
- sync clean или blocker documented.

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
