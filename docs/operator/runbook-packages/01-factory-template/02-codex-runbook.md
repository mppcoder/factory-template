# Ранбук для Codex: factory-template

Этот runbook начинается только после `01-user-runbook.md` takeover point: Codex уже работает в remote context на VPS через `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.

## Подтверждение маршрута

- `launch_source`: `chatgpt-handoff` или `direct-task`.
- `project_profile`: `factory-template as greenfield-product + factory-producer-owned layer`.
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md` или более точный route из handoff.
- `apply_mode`: `manual-ui` default.
- `strict_launch_mode`: `optional`.
- Язык ответа Codex: русский. Отвечай пользователю по-русски.

Для `chatgpt-handoff` дай только `handoff receipt` / `route receipt`, не называй его self-handoff. Для `direct-task` сначала покажи visible self-handoff.

## Граница пользовательской настройки

Маркер слоя: `USER-ONLY SETUP`.
Не проси пользователя вручную устанавливать packages, clone-ить repo, запускать bootstrap или verify, если remote shell доступен. Пользователь нужен только для external UI, secret entry, billing/account action, required approval или отсутствующего доступа.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

### CX-000. Проверить remote context

```bash
set -euo pipefail
hostname
whoami
pwd
lsb_release -a
```

Ожидается Ubuntu 24.04 на VPS. Если host локальный Windows/macOS или путь не remote, остановись и попроси пользователя вернуться к `FT-500`.

### CX-010. Подготовить базовые системные пакеты

```bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl gnupg git jq build-essential python3 python3-venv python3-pip nodejs npm openssh-client rsync unzip
```

Если текущий пользователь не `root`, используй `sudo` и проверь, что sudo доступен.

### CX-020. Установить или обновить Codex CLI на VPS

```bash
set -euo pipefail
npm i -g @openai/codex
codex --version
```

Если `codex` требует sign in и интерактивный sign in невозможен внутри текущего tool context, зафиксируй external blocker `codex-remote-sign-in-required` и попроси пользователя выполнить sign in в remote terminal. Не проси его продолжать install/clone вручную.

### CX-030. Установить GitHub CLI, если нужен verified sync

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
```

Если GitHub auth нужен для private repo или push, сначала проверь `gh auth status`. Secret/token вводит только пользователь в официальном `gh auth login` flow.

### CX-040. Создать `/projects` и clone/sync repo

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

Если repo private и HTTPS clone fails, попробуй authenticated `gh repo clone mppcoder/factory-template factory-template` после `gh auth status`. Если auth недоступен, зафиксируй blocker.

### CX-050. Прочитать repo router и route files

```bash
set -euo pipefail
cd /projects/factory-template
sed -n '1,240p' template-repo/scenario-pack/00-master-router.md
```

Если router отправляет в дополнительные repo files, прочитай их до реализации.

### CX-060. Запустить setup/bootstrap discovery

```bash
set -euo pipefail
cd /projects/factory-template
test -f AGENTS.md && sed -n '1,220p' AGENTS.md
find . -maxdepth 3 -type f \( -name 'README.md' -o -name 'package.json' -o -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'Makefile' \) | sort
```

Если repo содержит явный bootstrap script, используй его. Если нет, не выдумывай тяжелый bootstrap; переходи к repo validators.

### CX-070. Целевая проверка

```bash
set -euo pipefail
cd /projects/factory-template
python3 template-repo/scripts/validate-runbook-packages.py .
python3 template-repo/scripts/validate-codex-routing.py .
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
python3 template-repo/scripts/validate-brownfield-transition.py .
python3 template-repo/scripts/validate-greenfield-conversion.py .
```

Если targeted verify fails, исправь drift в repo-owned files и повтори targeted verify.

### CX-080. Быстрая проверка

```bash
set -euo pipefail
cd /projects/factory-template
bash template-repo/scripts/verify-all.sh quick
```

Если quick verify слишком долгий или зависает из-за внешнего runtime, зафиксируй точный blocker и оставь targeted verify evidence.

### CX-090. Обновить dashboard и closeout artifacts

Обнови только релевантные repo artifacts:

- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`;
- defect report в `reports/bugs/`;
- release-facing docs (`CHANGELOG.md`, `RELEASE_NOTES.md`, `CURRENT_FUNCTIONAL_STATE.md`), если change release-facing;
- source/export manifests, если добавлены новые package files.

Dashboard должен показывать phase, gates, blockers и next action для runbook packages.

### CX-100. Проверенная синхронизация

```bash
set -euo pipefail
cd /projects/factory-template
git status --short --branch
git diff --check
```

Если verify green, `origin` доступен, branch не защищен и repo rules разрешают sync, выполни canonical verified sync path. Если sync невозможен, зафиксируй blocker с evidence: auth, protected branch, remote drift, dirty unrelated changes или missing origin.

## Форма handoff после передачи Codex

Пользователь вставляет один цельный handoff. Он не должен быть ссылкой на файл и должен содержать:

```text
Язык ответа Codex: русский. Отвечай пользователю по-русски.
launch_source: chatgpt-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template as greenfield-product + factory-producer-owned layer
selected_scenario: template-repo/scenario-pack/00-master-router.md -> ...
pipeline_stage: ...
handoff_allowed: yes
defect_capture_path: required|not-required
```

Already-open live session не является надежным auto-switch boundary. Надежная executable boundary для strict mode: новый task launch через repo launcher/profile scripts; manual UI default: новый Codex chat/window, ручной picker, один handoff block.
