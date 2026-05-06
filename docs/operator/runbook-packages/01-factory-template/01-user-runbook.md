# Пользовательский ранбук: factory-template

Стартовая точка для новичка: `FT-000`.
Цель: довести пользователя от состояния "есть только Windows PC и браузер" до состояния "remote Codex context готов, можно вставить один большой handoff". После `FT-170` пользовательский ранбук останавливается: дальше Codex сам делает clone/setup/verify/dashboard/sync по `02-codex-runbook.md`.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешние действия: аккаунты, подписки, GitHub/ChatGPT/Codex sign in, Timeweb Cloud, VPS, SSH key, SSH config и выбор рабочего Codex contour.
Для Ubuntu/VPS пользователь выбирает исходный OS image, но обновление ОС, runtime stack или критичных зависимостей не выполняется автоматически: Codex после takeover фиксирует baseline, проверяет `unattended-upgrades`, готовит watchlist/readiness и запрашивает approval только через отдельный upgrade proposal.

Default-decision layer для setup использует recommendation-first режим:

- `default_decision_mode`: `global-defaults`, `confirm-each-default` или `manual`;
- `accepted_defaults`: список принятых setup defaults;
- `overridden_defaults`: список замененных setup defaults;
- `default_source_basis`: `repo-policy`, `official-docs`, `best-practice`, `project-scale` или `user-override`;
- `uncertainty_notes`: где нужна later review или fresh check;
- `decisions_requiring_user_confirmation`: платные, security, secret-related или destructive confirmations.
- Timeweb Ubuntu 24.04 VPS как recommended default для beginner path;
- SSH key `ed25519` как recommended default;
- project root `/projects/factory-template` как repo-policy default;
- `vscode-remote-ssh-codex-extension` как beginner-friendly default contour;
- `codex-app-remote-ssh` как alternate/fallback, если уже настроен.

Каждый default можно заменить своим вариантом; defaults accepted or overridden должны быть зафиксированы перед takeover. Платные, security, secret-related и destructive decisions требуют explicit user confirmation и не автопринимаются.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После takeover пользователь вставляет один handoff, а Codex сам проверяет VPS, ставит пакеты, создает `/projects/factory-template`, клонирует `mppcoder/factory-template`, запускает setup/bootstrap, `verify-all.sh quick`, чинит drift, обновляет dashboard и делает verified sync при доступном `origin`.

## Плейсхолдеры

- `<VPS_IP>`: публичный IPv4 адрес из Timeweb Cloud Dashboard -> карточка VPS.
- `<GITHUB_USER>`: GitHub login из профиля `https://github.com/<GITHUB_USER>`.
- `<server-hostname>`: hostname VPS после входа по SSH.
- `<handoff block>`: один цельный текст из ChatGPT Project, без ссылки на файл и без разбиения на несколько сообщений.
- `Codex takeover point`: момент `FT-170`, когда remote `Codex extension / Codex chat` или Codex app thread уже может выполнять команды на VPS.

## Шаги

### FT-000. Стартовое состояние

- Окно: Windows PC / Browser.
- Делает: Пользователь.
- Зачем: Зафиксировать, что repo-команды еще не нужны.
- Что нужно до начала: Windows PC, браузер, интернет, права устанавливать программы.
- Где взять значения: Значения пока не нужны.
- Команды для копирования:

```text
Старт: есть Windows PC, браузер и интернет.
Иду по ранбуку с FT-000 до FT-170.
После FT-170 Codex делает clone/setup/verify сам.
```

- Куда вставить: Можно вставить в заметки; в терминал не вставлять.
- Ожидаемый результат: Понятна граница: пользователь готовит доступ, Codex автоматизирует repo work.
- Если ошибка: Если нет прав установки программ, используйте Windows account с правами администратора.
- Evidence: Пользователь может открыть браузер и Windows PowerShell.
- Следующий шаг: `FT-010`.

### FT-010. Оформить или проверить ChatGPT plan с Codex access

- Окно: Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex app, IDE extension или CLI должны быть доступны через ChatGPT account или официальный auth flow.
- Что нужно до начала: Email/phone для ChatGPT account.
- Где взять значения: ChatGPT -> account menu -> Settings / Plan.
- Команды для копирования:

```text
Проверить в ChatGPT:
- account открыт;
- plan/workspace дает доступ к Codex;
- sign in в Codex client доступен.
```

- Куда вставить: Не вставлять; выполнить в Browser ChatGPT.
- Ожидаемый результат: ChatGPT account активен, Codex access виден или Codex sign in открывается.
- Если ошибка: Если Codex не виден, проверьте plan, workspace controls и доступность Codex в вашем регионе/account.
- Evidence: Скриншот или текстовый статус plan без секретов.
- Следующий шаг: `FT-020`.

### FT-020. Создать или проверить GitHub account

- Окно: Browser GitHub.
- Делает: Пользователь.
- Зачем: Repo `mppcoder/factory-template` читается из GitHub, а sync требует GitHub identity.
- Что нужно до начала: Email для GitHub.
- Где взять значения: `<GITHUB_USER>` взять в GitHub profile menu или из profile URL.
- Команды для копирования:

```text
GitHub checklist:
- login: <GITHUB_USER>
- email подтвержден;
- открывается https://github.com/mppcoder/factory-template
```

- Куда вставить: Не вставлять; проверить в Browser GitHub.
- Ожидаемый результат: GitHub account открыт, repo page доступна.
- Если ошибка: Если repo не открывается, проверьте login, организацию и права доступа.
- Evidence: `<GITHUB_USER>` и факт, что repo page открывается; токены не копировать.
- Следующий шаг: `FT-030`.

### FT-030. Подключить GitHub account к ChatGPT Project или connector

- Окно: Browser ChatGPT / Browser GitHub OAuth.
- Делает: Пользователь.
- Зачем: ChatGPT Project должен читать repo-first source и готовить handoff из GitHub repo.
- Что нужно до начала: `FT-010`, `FT-020`.
- Где взять значения: GitHub OAuth выбирает account `<GITHUB_USER>`; repo path `mppcoder/factory-template`.
- Команды для копирования:

```text
ChatGPT -> Settings -> Apps/Connectors -> GitHub -> Connect.
Разрешить доступ к mppcoder/factory-template.
Проверить, что ChatGPT может найти repo:mppcoder/factory-template.
```

- Куда вставить: Не вставлять; пройти UI в Browser ChatGPT и GitHub OAuth.
- Ожидаемый результат: GitHub connector подключен, ChatGPT видит repo.
- Если ошибка: Если connector недоступен, зафиксируйте это как external blocker; если repo не виден, проверьте scope GitHub app.
- Evidence: ChatGPT/GitHub connector показывает connected state.
- Следующий шаг: `FT-040`.

### FT-040. Установить VS Code

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: Default contour для новичка: `vscode-remote-ssh-codex-extension`.
- Что нужно до начала: Windows PC с правами установки.
- Где взять значения: Package id фиксирован: `Microsoft.VisualStudioCode`.
- Команды для копирования:

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
Successfully installed
```

- Если ошибка: Если `winget` отсутствует, скачайте VS Code с `https://code.visualstudio.com/`; если Windows просит подтверждение, подтвердите установку.
- Evidence: VS Code запускается из Start menu.
- Следующий шаг: `FT-050`.

### FT-050. Установить VS Code extensions

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: Remote SSH, GitHub и Codex IDE extension нужны для remote takeover.
- Что нужно до начала: `FT-040`.
- Где взять значения: Extension IDs ниже; если Codex extension ID изменился, найти `Codex` или `OpenAI` в VS Code Extensions.
- Команды для копирования:

```powershell
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension github.vscode-pull-request-github
code --install-extension openai.chatgpt
code --install-extension redhat.vscode-yaml
code --install-extension yzhang.markdown-all-in-one
code --install-extension ms-azuretools.vscode-docker
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
Extension '...' was successfully installed.
```

- Если ошибка: Если `code` не найден, откройте VS Code -> Command Palette -> `Shell Command: Install 'code' command in PATH`; если Codex extension не находится, установить через Extensions UI.
- Evidence: VS Code Extensions view показывает Remote - SSH, GitHub Pull Requests and Issues, Codex/OpenAI extension, YAML, Markdown All in One.
- Следующий шаг: `FT-060`.

### FT-060. Установить Codex app на ПК

- Окно: Browser / Codex app.
- Делает: Пользователь.
- Зачем: Fallback contour `codex-app-remote-ssh`.
- Что нужно до начала: `FT-010`.
- Где взять значения: Официальная Codex app page: `https://developers.openai.com/codex/app`.
- Команды для копирования:

```text
Codex app checklist:
- открыть официальную Codex app page;
- скачать Codex app для Windows, если доступна;
- установить app;
- выполнить sign in через ChatGPT account.
```

- Куда вставить: Не вставлять; выполнить в Browser и Codex app.
- Ожидаемый результат: Codex app открывается и показывает signed-in account.
- Если ошибка: Если Codex app недоступен на ПК, используйте default contour `vscode-remote-ssh-codex-extension`.
- Evidence: Codex app открыт или зафиксирован fallback на VS Code contour.
- Следующий шаг: `FT-070`.

### FT-070. Установить Codex CLI локально, если нужен локальный test contour

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: Локальный CLI не обязателен для remote takeover, но помогает проверить auth/fallback.
- Что нужно до начала: `FT-010`; возможность установить Node.js LTS.
- Где взять значения: Codex CLI package: `@openai/codex`.
- Команды для копирования:

```powershell
winget install --id OpenJS.NodeJS.LTS -e
npm i -g @openai/codex
codex --version
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
codex <version>
```

- Если ошибка: Если `npm` не найден после установки Node.js, закройте и снова откройте PowerShell.
- Evidence: Вывод `codex --version` или решение пропустить local test contour.
- Следующий шаг: `FT-080`.

### FT-080. Войти в Codex через ChatGPT account или API key

- Окно: Codex app / VS Code Codex sidebar / Windows PowerShell.
- Делает: Пользователь.
- Зачем: Codex должен быть авторизован до remote takeover.
- Что нужно до начала: `FT-010`, установленный Codex client.
- Где взять значения: ChatGPT account используется в официальном sign-in flow; API key вводить только в официальный prompt, не в repo и не в handoff.
- Команды для копирования:

```powershell
codex
```

- Куда вставить: Windows PowerShell, если установлен Codex CLI; для app/extension нажать Sign in в UI.
- Ожидаемый результат: Открывается auth flow, после входа Codex показывает signed-in state или prompt.
- Если ошибка: Если sign in не появляется, выполните `codex logout`, затем снова `codex`; если используете extension/app, перезапустите client.
- Evidence: Codex client показывает signed-in state; секреты не сохранять.
- Следующий шаг: `FT-090`.

### FT-090. Создать Timeweb Cloud account

- Окно: Timeweb Cloud в браузере.
- Делает: Пользователь.
- Зачем: VPS нужен как remote host для Codex.
- Что нужно до начала: Email/phone/payment method по правилам Timeweb.
- Где взять значения: Timeweb Cloud Dashboard после регистрации.
- Команды для копирования:

```text
Timeweb checklist:
- account создан;
- email/phone/billing подтверждены;
- Cloud Dashboard открывается.
```

- Куда вставить: Не вставлять; выполнить в Timeweb Cloud UI.
- Ожидаемый результат: Timeweb Cloud Dashboard доступен.
- Если ошибка: Если billing/account не подтвержден, остановитесь: VPS создать нельзя.
- Evidence: Dashboard открыт, без платежных данных в handoff.
- Следующий шаг: `FT-100`.

### FT-100. Создать VPS Ubuntu 24.04 в Timeweb

- Окно: Timeweb Cloud.
- Делает: Пользователь.
- Зачем: Создать remote machine для Codex.
- Что нужно до начала: `FT-090`.
- Где взять значения: `<VPS_IP>` появится в карточке VPS; username для этого runbook: `root`.
- Команды для копирования:

```text
VPS settings:
- OS: Ubuntu 24.04
- User: root
- SSH key access: включить
- Public IP: <VPS_IP>
- Local SSH alias будет: factory-vps
```

- Куда вставить: Не вставлять; выбрать значения в Timeweb Cloud UI.
- Ожидаемый результат: VPS создан, status running, публичный `<VPS_IP>` виден в Dashboard.
- Если ошибка: Если VPS доступен только по password, добавьте SSH key на `FT-120` или через Timeweb console.
- Evidence: `<VPS_IP>` записан в заметки; password/secrets не копировать.
- Следующий шаг: `FT-110`.

### FT-110. Создать SSH-ключ на ПК в Windows PowerShell

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: SSH key позволит подключаться к VPS без пароля.
- Что нужно до начала: Windows OpenSSH Client установлен; обычно есть в Windows 10/11.
- Где взять значения: Key path фиксирован: `$env:USERPROFILE\.ssh\factory_timeweb_ed25519`.
- Команды для копирования:

```powershell
$KEY="$env:USERPROFILE\.ssh\factory_timeweb_ed25519"
ssh-keygen -t ed25519 -C "factory-template-timeweb-vps" -f $KEY
Get-Content "$KEY.pub"
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
ssh-ed25519 AAAA... factory-template-timeweb-vps
```

- Если ошибка: Если `.ssh` folder отсутствует, выполните `New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh"` и повторите; если key уже существует, не перезаписывайте без осознанного решения.
- Evidence: Public key строка `ssh-ed25519 ... factory-template-timeweb-vps` скопирована для `FT-120`.
- Следующий шаг: `FT-120`.

### FT-120. Добавить public SSH key в Timeweb

- Окно: Timeweb Cloud / Windows PowerShell.
- Делает: Пользователь.
- Зачем: VPS должен доверять public key с вашего ПК.
- Что нужно до начала: `FT-100`, `FT-110`.
- Где взять значения: Public key взять из вывода `Get-Content "$KEY.pub"`.
- Команды для копирования:

```powershell
$KEY="$env:USERPROFILE\.ssh\factory_timeweb_ed25519"
Get-Content "$KEY.pub"
```

- Куда вставить: Команды вставить в Windows PowerShell; затем всю строку `ssh-ed25519 ...` вставить в Timeweb Cloud -> SSH-ключи / Server access -> Add key.
- Ожидаемый результат: В Timeweb Cloud есть SSH key `factory-template-timeweb-vps`, привязанный к VPS.
- Если ошибка: Если key добавлен после создания VPS и не применяется, используйте Timeweb server settings или console, затем reboot по требованию UI.
- Evidence: Timeweb Cloud показывает добавленный SSH key; private key не копировать.
- Следующий шаг: `FT-130`.

### FT-130. Настроить SSH config на ПК

- Окно: Windows PowerShell / Notepad.
- Делает: Пользователь.
- Зачем: VS Code Remote SSH и Codex app будут подключаться по alias `factory-vps`.
- Что нужно до начала: `FT-100`, `FT-120`, значение `<VPS_IP>`.
- Где взять значения: `<VPS_IP>` взять в Timeweb Cloud Dashboard -> карточка VPS.
- Команды для копирования:

```powershell
notepad $env:USERPROFILE\.ssh\config
```

```sshconfig
Host factory-vps
    HostName <VPS_IP>
    User root
    IdentityFile ~/.ssh/factory_timeweb_ed25519
    IdentitiesOnly yes
```

- Куда вставить: Первую команду вставить в Windows PowerShell. Второй блок вставить в Notepad, заменить `<VPS_IP>` на реальный IP, сохранить файл.
- Ожидаемый результат: `%USERPROFILE%\.ssh\config` содержит host `factory-vps`.
- Если ошибка: Если Notepad предлагает создать файл, нажмите Yes; если SSH config уже содержит `Host factory-vps`, обновите existing block вместо дублирования.
- Evidence: В config есть `Host factory-vps`, `User root`, `IdentityFile ~/.ssh/factory_timeweb_ed25519`.
- Следующий шаг: `FT-140`.

### FT-140. Проверить SSH

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: До Codex setup нужно доказать, что ПК может войти на VPS.
- Что нужно до начала: `FT-130`.
- Где взять значения: Значения уже сохранены в SSH config.
- Команды для копирования:

```powershell
ssh factory-vps
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
root@<server-hostname>:~#
```

- Если ошибка: `Permission denied (publickey)` означает, что public key не применен к VPS или выбран не тот private key; `Connection timed out` означает неверный `<VPS_IP>`, firewall или stopped VPS.
- Evidence: SSH prompt `root@<server-hostname>:~#` открыт; для выхода можно выполнить `exit`.
- Следующий шаг: `FT-150A` или `FT-150B`.

### FT-150A. Вариант A: настроить Codex App + Remote SSH

- Окно: Windows PowerShell / VPS terminal / Codex app.
- Делает: Пользователь.
- Зачем: Fallback contour: Codex app remote thread выполняет команды на VPS.
- Что нужно до начала: `FT-060`, `FT-080`, `FT-140`.
- Где взять значения: SSH alias `factory-vps`; remote folder до clone: `/projects` или `/root`.
- Команды для копирования:

```powershell
ssh factory-vps "apt-get update && apt-get install -y nodejs npm"
ssh factory-vps "npm i -g @openai/codex && codex --version"
notepad "$env:USERPROFILE\.codex\config.toml"
```

```toml
remote_connections = true
```

- Куда вставить: Первые две команды вставить в Windows PowerShell. Третью команду вставить в Windows PowerShell, затем добавить `remote_connections = true` в config file. После этого открыть Codex app -> Settings -> Connections -> add/enable `factory-vps` -> выбрать remote folder `/projects` или `/root`.
- Ожидаемый результат:

```text
codex <version>
```

Codex app показывает remote connection `factory-vps`, remote thread может выполнить команду на VPS.
- Если ошибка: Если remote host просит sign in, выполните `ssh factory-vps`, затем `codex` на VPS и пройдите sign in; если Codex app не видит connection, перезапустите app после изменения config.
- Evidence: Codex app remote thread выполняет `whoami` на VPS и показывает `root`.
- Следующий шаг: `FT-160`.

### FT-150B. Вариант B: настроить VS Code Remote SSH + Codex IDE extension

- Окно: VS Code / Command Palette / VS Code Remote SSH / VPS terminal / Codex sidebar.
- Делает: Пользователь.
- Зачем: Default contour: Codex IDE extension работает внутри VS Code Remote SSH context.
- Что нужно до начала: `FT-040`, `FT-050`, `FT-080`, `FT-140`.
- Где взять значения: SSH alias `factory-vps`; remote folder до clone: `/projects` или `/root`.
- Команды для копирования:

```text
VS Code UI path:
1. Ctrl+Shift+P.
2. Remote-SSH: Connect to Host.
3. Выбрать factory-vps.
4. Open Folder: /projects или /root.
5. Terminal -> New Terminal.
6. Открыть Codex sidebar.
7. Sign in в Codex extension.
8. Открыть новый Codex chat/window.
```

```bash
whoami
pwd
uname -a
lsb_release -a || cat /etc/os-release
```

- Куда вставить: Первый блок выполнить в VS Code UI. Второй блок вставить в VS Code Remote SSH terminal.
- Ожидаемый результат:

```text
root
/projects
Description:    Ubuntu 24.04...
```

Codex sidebar signed in, новый Codex chat/window открыт в Remote SSH window.
- Если ошибка: Если Remote SSH не подключается, вернитесь к `FT-140`; если Codex открылся в локальном VS Code window, закройте его и откройте внутри Remote SSH window.
- Evidence: VS Code status bar показывает SSH: `factory-vps`, terminal выполняет `whoami`, Codex sidebar signed in.
- Следующий шаг: `FT-160`.

### FT-160. Выбрать рабочий вариант Codex

- Окно: Codex app / VS Code Remote SSH.
- Делает: Пользователь.
- Зачем: Для takeover нужен один рабочий contour, не оба сразу.
- Что нужно до начала: Выполнен `FT-150A` или `FT-150B`.
- Где взять значения: Выбранный contour по факту успешной remote команды.
- Команды для копирования:

```text
Выбранный contour:
- vscode-remote-ssh-codex-extension, если VS Code Remote SSH terminal и Codex sidebar работают.
- codex-app-remote-ssh, если Codex app remote thread выполняет команды на VPS.
```

- Куда вставить: Можно вставить в заметки или оставить как контрольный список.
- Ожидаемый результат: Один contour выбран как рабочий; default для новичка `vscode-remote-ssh-codex-extension`.
- Если ошибка: Если ни один contour не выполняет remote command, перейти к `FT-180`.
- Evidence: Название выбранного contour и результат remote command.
- Следующий шаг: `FT-170`.

### FT-170. Точка передачи Codex

- Окно: Codex app remote thread или VS Code Remote SSH Codex chat/window.
- Делает: Пользователь.
- Зачем: Передать работу Codex; после этого пользователь не сопровождает clone/setup/verify руками.
- Что нужно до начала: `FT-160`; remote Codex context может выполнять команды на VPS.
- Где взять значения: `<handoff block>` взять из Browser ChatGPT Project. Он должен содержать `Язык ответа Codex: русский`.
- Команды для копирования:

```text
Проверить перед вставкой:
- открыт новый Codex chat/window;
- выбран model/reasoning в picker, если picker доступен;
- context remote: factory-vps;
- REMOTE_CONTEXT_MARKER подтвержден: whoami/pwd/uname/lsb_release выполняются на VPS;
- do not paste into local Codex: локальный Windows/macOS Codex не считается takeover;
- handoff вставляется одним цельным блоком;
- после вставки Codex делает clone/setup/verify сам.
- no hidden second shell step: после handoff пользователь не запускает clone/setup/verify руками.

Вставить:
<handoff block>
```

- Куда вставить: В Codex app remote thread или VS Code Remote SSH Codex chat/window.
- Ожидаемый результат: Codex отвечает route receipt по-русски и начинает `02-codex-runbook.md`: проверяет VPS, ставит packages, clone-ит repo, запускает verify и sync.
- Если ошибка: Если Codex отвечает из локального context, остановить и открыть remote chat/window заново; если handoff разбился на несколько сообщений, создать новый chat/window и вставить одним блоком.
- Evidence: Codex вывел route receipt и remote shell check.
- Следующий шаг: `STOP` для пользователя; если Codex не стартовал, `FT-180`.

### FT-180. Что прислать обратно, если Codex не стартовал

- Окно: Windows PowerShell / VS Code Remote SSH / Codex app.
- Делает: Пользователь.
- Зачем: Дать минимальную диагностику без секретов, чтобы починить setup.
- Что нужно до начала: Попытка `FT-170` не удалась.
- Где взять значения: Error text из Codex/VS Code/SSH; выбранный contour из `FT-160`.
- Команды для копирования:

```powershell
ssh factory-vps
```

```text
Диагностика для отправки:
- выбранный contour: codex-app-remote-ssh или vscode-remote-ssh-codex-extension
- что видно в Codex: <error text или screenshot без секретов>
- вывод ssh factory-vps: <успешный prompt или ошибка>
- где открыт Codex: local window или remote factory-vps window
```

- Куда вставить: Первую команду вставить в Windows PowerShell. Второй блок заполнить и отправить в ChatGPT/Codex support thread без токенов, паролей и private key.
- Ожидаемый результат: Есть достаточная диагностика: screenshot/error text, output `ssh factory-vps`, выбранный contour A/B.
- Если ошибка: Если `ssh factory-vps` тоже не работает, вернуться к `FT-130` и `FT-140`.
- Evidence: Error text/screenshot без секретов и результат `ssh factory-vps`.
- Следующий шаг: Исправить setup по диагностике, затем вернуться к `FT-170`.
