# Проверка: путь без repo

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

User readiness до takeover:

- target root и `_incoming` определены;
- incoming materials загружены или blocker documented;
- remote Codex context открыт в `/projects/<project-slug>`;
- Codex может выполнить remote root check.

Codex automation после takeover:

- inventory/evidence создан;
- reconstruction выполнена внутри target root;
- with-repo conversion выполнена или documented blocker;
- validators green;
- sync clean или blocker documented.

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
