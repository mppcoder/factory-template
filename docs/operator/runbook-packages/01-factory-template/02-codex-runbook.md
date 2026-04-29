# Ранбук для Codex: factory-template

Этот runbook начинается только после `FT-170`: пользователь уже вставил один handoff в remote Codex context. Пользователь больше не выполняет clone/setup/verify вручную, если remote shell доступен.

## Подтверждение маршрута

Codex сначала выводит route receipt:

- `launch_source`: `chatgpt-handoff` или `direct-task`.
- `project_profile`: `factory-template as greenfield-product + factory-producer-owned layer`.
- `selected_scenario`: маршрут из handoff после `template-repo/scenario-pack/00-master-router.md`.
- `pipeline_stage`: текущий stage из handoff.
- `handoff_allowed`: `yes`.
- `defect_capture_path`: `required` или `not-required`.
- Язык ответа Codex: русский. Отвечай пользователю по-русски.

Для `chatgpt-handoff` не называй receipt self-handoff. Для `direct-task` сначала покажи visible self-handoff.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Пользователь нужен только для external UI, secret entry, billing/account action, required approval, Codex sign in blocker или отсутствующего доступа. Не проси пользователя вручную выполнять install/clone/bootstrap/verify, если remote shell доступен.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

### CX-000. Определить contour и remote shell

Определи, где запущен Codex:

- `codex-app-remote-ssh`: Codex app remote thread выполняет команды на VPS.
- `vscode-remote-ssh-codex-extension`: Codex extension работает в VS Code Remote SSH context.
- `unknown`: если evidence недостаточно, продолжай remote shell checks и не утверждай contour.

Выполни:

```bash
set -euo pipefail
whoami
pwd
uname -a
lsb_release -a || cat /etc/os-release
```

Ожидается remote Ubuntu 24.04 VPS. Если это локальный Windows/macOS context или нет shell access, остановись с blocker `remote-codex-context-not-ready` и попроси пользователя вернуться к `FT-170`/`FT-180`.

### CX-010. Установить baseline packages на VPS

```bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git curl ca-certificates gnupg unzip jq build-essential python3 python3-venv python3-pip pipx
```

Если пользователь не `root`, используй `sudo` и явно проверь `sudo -n true`.

### CX-020. Установить Node.js, corepack и pnpm по repo-approved strategy

```bash
set -euo pipefail
if ! command -v node >/dev/null 2>&1; then
  apt-get install -y nodejs npm
fi
node --version
npm --version
if command -v corepack >/dev/null 2>&1; then
  corepack enable
  corepack prepare pnpm@latest --activate || true
else
  npm i -g corepack pnpm
fi
pnpm --version || npm i -g pnpm
```

Если repo позже содержит `.node-version`, `.nvmrc`, `packageManager` или другой более точный strategy, следуй repo source-of-truth и зафиксируй это в closeout.

### CX-030. Установить GitHub CLI при необходимости verified sync

```bash
set -euo pipefail
if ! command -v gh >/dev/null 2>&1; then
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  mkdir -p /etc/apt/sources.list.d
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list
  apt-get update
  apt-get install -y gh
fi
gh --version
gh auth status || true
```

Если push требует auth и `gh auth status` не green, зафиксируй blocker `github-auth-required`. Secret/token вводит только пользователь в официальный `gh auth login` flow.

### CX-040. Установить Codex CLI на remote host, если contour требует

```bash
set -euo pipefail
if ! command -v codex >/dev/null 2>&1; then
  npm i -g @openai/codex
fi
codex --version
```

Если `codex` требует interactive sign in, зафиксируй blocker `codex-remote-sign-in-required`. Не перекладывай на пользователя clone/setup/verify.

### CX-050. Создать `/projects` и clone/sync repo

```bash
set -euo pipefail
mkdir -p /projects
cd /projects
if [ ! -d factory-template/.git ]; then
  git clone https://github.com/mppcoder/factory-template.git factory-template
fi
cd /projects/factory-template
git status --short --branch
git remote -v
```

Если repo уже существует, не перетирай user changes. Если clone private/auth fails, попробуй `gh repo clone mppcoder/factory-template factory-template` только после successful `gh auth status`; иначе blocker.

### CX-060. Прочитать repo rules

```bash
set -euo pipefail
cd /projects/factory-template
sed -n '1,240p' AGENTS.md
sed -n '1,240p' template-repo/scenario-pack/00-master-router.md
```

Если router отправляет в другие repo files, прочитай их до реализации.

### CX-070. Запустить setup/bootstrap discovery

```bash
set -euo pipefail
cd /projects/factory-template
find . -maxdepth 3 -type f \( -name 'README.md' -o -name 'package.json' -o -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'Makefile' -o -name 'setup.sh' -o -name 'bootstrap*.sh' \) | sort
```

Если найден repo-approved setup/bootstrap script, запусти его. Если явного bootstrap нет, не придумывай heavy setup; переходи к validators.

### CX-080. Запустить быструю проверку

```bash
set -euo pipefail
cd /projects/factory-template
bash template-repo/scripts/verify-all.sh quick
```

Если verify failed: пройти defect-capture -> remediation -> verify again. Для нового defect создать report в `reports/bugs/`, классифицировать layer и исправить repo-owned drift.

### CX-085. Зафиксировать controlled software update baseline

Codex выполняет report-only шаги и не устанавливает обновления без approval:

```bash
set -euo pipefail
cd /projects/factory-template
lsb_release -a || cat /etc/os-release
uname -a
apt-cache policy | sed -n '1,120p'
systemctl is-enabled unattended-upgrades || true
systemctl status unattended-upgrades --no-pager || true
systemctl list-timers 'apt*' --no-pager || true
docker --version || true
docker compose version || true
node --version || true
python3 --version || true
python3 template-repo/scripts/render-software-update-readiness.py --root . --output reports/software-updates/readiness-latest.md
python3 template-repo/scripts/validate-software-update-governance.py .
```

Source artifacts для generated и template-owned baseline:

- `.chatgpt/software-inventory.yaml`;
- `.chatgpt/software-update-watchlist.yaml`;
- `.chatgpt/software-update-readiness.yaml`;
- `reports/software-updates/README.md`.

Обязательно различай:

- selected Ubuntu LTS release / VPS image release;
- provider image id, если доступен;
- later package update state;
- `unattended-upgrades` installed/enabled state;
- package manager sources;
- Docker/Compose, Node/Python, GitHub Actions, base Docker images/tags/digests, lockfiles и critical runtime dependencies.

Default policy: `manual-approved-upgrade`; auto-install без approval запрещен. Переход на новую Ubuntu LTS — отдельный migration/upgrade project, а не silent maintenance step.

### CX-090. Обновить dashboard/readout

Обнови dashboard/readout только внутри repo-owned artifacts:

- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`;
- relevant `.chatgpt` readout files, если route требует;
- `CURRENT_FUNCTIONAL_STATE.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`, если change release-facing;
- `docs/template-architecture-and-event-workflows.md`, если workflow wording изменился.

Dashboard должен фиксировать `current_step`, `active_contour`, `takeover_ready`, `checklist_path`, blockers и next action для runbook packages.
Dashboard также должен фиксировать `software_update_governance`: baseline status, auto-update policy, last update intelligence check, findings count, upgrade proposal status, next safe action, fallback и blockers.

### CX-100. Выполнить verified sync

```bash
set -euo pipefail
cd /projects/factory-template
git status --short --branch
git diff --check
```

Если verify green и `origin` доступен, выполни canonical verified sync:

```bash
bash VERIFIED_SYNC.sh
```

Если sync невозможен, зафиксируй blocker: auth, protected branch, remote drift, dirty unrelated changes или missing origin.

### CX-110. Финал Codex

Финал должен назвать:

- contour: `codex-app-remote-ssh`, `vscode-remote-ssh-codex-extension` или `unknown`;
- verify result;
- commit hash / push status или blocker;
- `git status --short --branch`;
- внешний next step только если есть real external blocker.
