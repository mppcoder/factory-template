# Проверка: factory-template

## Проверка готовности пользователя до takeover

Пользовательская готовность считается достаточной, если выполнены все пункты:

- `ssh factory-vps` в Windows PowerShell открывает prompt:

```text
root@<server-hostname>:~#
```

- Один Codex contour работает:
  - `vscode-remote-ssh-codex-extension`: VS Code Remote SSH connected к `factory-vps`, открыт remote terminal, Codex sidebar signed in, новый Codex chat/window открыт в remote window.
  - `codex-app-remote-ssh`: Codex app connection `factory-vps` enabled, remote thread может выполнить команду на VPS.
- Codex может выполнить remote command:

```bash
whoami
pwd
uname -a
lsb_release -a || cat /etc/os-release
```

Ожидаемый результат: `root`, remote path `/projects` или `/root`, Ubuntu 24.04.

## Проверка автоматизации Codex после takeover

Codex automation считается green, если выполнены все пункты:

- baseline packages установлены:

```bash
git --version
curl --version
python3 --version
jq --version
```

- Node/corepack/pnpm или repo-approved equivalent доступны:

```bash
node --version
npm --version
pnpm --version || true
```

- repo cloned/opened:

```bash
cd /projects/factory-template
git status --short --branch
git remote -v
```

- quick verify green:

```bash
bash template-repo/scripts/verify-all.sh quick
```

- dashboard renders/validates:

```bash
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
```

- sync status clean или blocker documented:

```bash
git status --short --branch
```

## Проверка package layer из factory-template root

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
python3 template-repo/scripts/validate-codex-routing.py .
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
python3 template-repo/scripts/validate-brownfield-transition.py .
python3 template-repo/scripts/validate-greenfield-conversion.py .
```

## Быстрая проверка

```bash
bash template-repo/scripts/verify-all.sh quick
```
