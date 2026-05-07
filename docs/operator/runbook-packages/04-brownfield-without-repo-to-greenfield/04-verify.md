# Проверка: путь без repo

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

User readiness до takeover:

- target root и `_incoming` определены;
- non-standard VPS folders, если есть, описаны как intake/evidence candidates,
  not active source roots;
- default decision mode selected;
- defaults accepted or overridden: `/projects/<target-slug>/_incoming`, reconstructed/intermediate repos inside target root, evidence inventory -> reconstruction -> with-repo adoption -> conversion;
- custom overrides captured;
- secret/private/destructive decisions требуют explicit user confirmation и не автопринимаются;
- incoming materials загружены или blocker documented;
- remote Codex context открыт в `/projects/<project-slug>`;
- Codex может выполнить remote root check.

Codex automation после takeover:

- inventory/evidence создан;
- reconstruction выполнена внутри target root;
- with-repo conversion выполнена или documented blocker;
- source hardening completed or blocker documented when runtime distribution
  patches exist;
- local prod runtime proof completed or explicit blocker documented when real
  image/target/approvals exist;
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
