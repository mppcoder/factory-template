# Проверка: путь с существующим repo

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

User readiness до takeover:

- existing repo URL и target root зафиксированы;
- default decision mode selected;
- defaults accepted or overridden: keep existing repo as canonical root, do not overwrite product-owned code, evidence-first audit before remediation;
- custom overrides captured;
- GitHub access/approval boundary известен;
- risky migration/protected branch/security decisions требуют explicit user confirmation и не автопринимаются;
- remote Codex context открыт;
- Codex может выполнить remote shell/repo check.

Codex automation после takeover:

- audit evidence создан;
- conversion выполнена в `greenfield-product` / `greenfield-converted` или documented blocker;
- validators green;
- sync clean или blocker documented.

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
