# Проверка: greenfield-product

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

User readiness до takeover:

- пользователь выбрал `<PROJECT_NAME>`;
- пользователь сообщил Codex название и optional идею;
- factory-template установлен и verified;
- remote Codex context открыт;
- Codex может выполнить remote shell command.
- пользователь создал ChatGPT Project в UI;
- пользователь вставил готовую repo-first инструкцию, подготовленную Codex.

Codex automation после takeover:

- Codex нормализовал project slug/repo name;
- Codex создал GitHub repo или documented blocker;
- Codex добавил `origin`, сделал initial commit/push или documented blocker;
- `/projects/<project-slug>` создан;
- wizard/launcher выполнен Codex;
- repo-first core materialized;
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
