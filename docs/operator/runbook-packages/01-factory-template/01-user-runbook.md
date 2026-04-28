# Пользовательский ранбук: factory-template

Этот файл ведет новичка от состояния "есть только Windows PC и браузер" до состояния "Codex работает в remote context на VPS и может сам продолжить установку". После takeover point пользователь больше не устанавливает пакеты, не клонирует repo и не запускает verify вручную: это делает Codex по `02-codex-runbook.md`.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только действия, где нужен внешний UI, учетная запись, SSH-доступ, секрет или ручной sign in.

Плейсхолдеры:

- `<WINDOWS_USER>`: имя папки пользователя Windows, например `Ivan`.
- `<GITHUB_USER>`: login GitHub из `https://github.com/<GITHUB_USER>`.
- `<VPS_IP>`: публичный IPv4 адрес сервера в Timeweb Cloud.
- `<VPS_USER>`: обычно `root`, если при создании VPS не выбран отдельный пользователь.
- `<SSH_KEY_NAME>`: `factory-template-vps`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
Начинается после шагов `FT-300` или `FT-400`, когда remote Codex thread/extension может выполнять команды на VPS. Дальше пользователь вставляет один большой handoff в Codex, а Codex сам проверяет VPS, ставит tools, клонирует `mppcoder/factory-template`, запускает bootstrap/verify, чинит drift, обновляет dashboard и делает verified sync.

## Варианты Codex setup

- `codex-app-remote-ssh`: Codex app подключается к `factory-vps` и открывает remote folder на VPS.
- `vscode-remote-ssh-codex-extension`: VS Code подключается к `factory-vps`, а `Codex extension / Codex chat` работает внутри VS Code Remote SSH window.

Выберите один вариант. Если сомневаетесь, используйте `vscode-remote-ssh-codex-extension`: он проще проверяется через встроенный remote terminal.

### FT-000. Стартовое состояние

- Окно: Windows PC / Browser.
- Делает: Пользователь.
- Зачем: Зафиксировать исходную точку и не начинать с repo-команд, пока нет доступа.
- Что нужно до начала: Компьютер с Windows 10/11, браузер, интернет, права устанавливать программы.
- Где взять значения: Пока значения не нужны.
- Команды для копирования:

```text
Старт: есть Windows PC, браузер и интернет.
Цель user-runbook: довести Codex до remote VPS context.
```

- Куда вставить: Можно никуда не вставлять; это контрольная заметка.
- Ожидаемый результат: Вы понимаете, что все repo-команды начнутся только после takeover point.
- Если ошибка: Если нет прав устанавливать программы, используйте учетную запись Windows с правами администратора.
- Следующий шаг: `FT-010`.

### FT-010. Оформить или проверить ChatGPT plan с Codex access

- Окно: Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex CLI, IDE extension и app должны иметь доступ через ChatGPT account или API key.
- Что нужно до начала: Аккаунт ChatGPT.
- Где взять значения: Текущий plan виден в ChatGPT account settings.
- Команды для копирования:

```text
Проверить:
- ChatGPT account открыт.
- Plan дает доступ к Codex.
- Я могу открыть Codex client и пройти sign in.
```

- Куда вставить: Не вставлять; сверить в ChatGPT web UI.
- Ожидаемый результат: В настройках аккаунта виден plan с Codex access; Codex sign in доступен.
- Если ошибка: Если Codex недоступен, проверьте plan/region/workspace controls в ChatGPT settings.
- Следующий шаг: `FT-020`.

### FT-020. Создать или проверить GitHub account

- Окно: Browser GitHub.
- Делает: Пользователь.
- Зачем: `factory-template` хранится в GitHub repo, а ChatGPT/Codex должны уметь читать или клонировать его.
- Что нужно до начала: Email и браузер.
- Где взять значения: `<GITHUB_USER>` виден в правом верхнем меню GitHub или в profile URL.
- Команды для копирования:

```text
GitHub checklist:
- Login: <GITHUB_USER>
- Email подтвержден.
- Я могу открыть https://github.com/mppcoder/factory-template
```

- Куда вставить: Не вставлять; сверить в GitHub UI.
- Ожидаемый результат: Открывается GitHub account и repo page.
- Если ошибка: Если repo не открывается, проверьте login или доступ к организации/репозиторию.
- Следующий шаг: `FT-030`.

### FT-030. Подключить GitHub account к ChatGPT Project или connector

- Окно: Browser ChatGPT / Settings / Apps.
- Делает: Пользователь.
- Зачем: ChatGPT Project должен читать GitHub repo и готовить repo-first handoff.
- Что нужно до начала: `FT-010`, `FT-020`.
- Где взять значения: GitHub account выбирается в OAuth screen; repo name: `mppcoder/factory-template`.
- Команды для копирования:

```text
Подключить GitHub к ChatGPT:
1. ChatGPT -> Settings -> Apps.
2. Найти GitHub.
3. Connect.
4. Разрешить доступ к repo mppcoder/factory-template.
5. Проверить поиск repo:mppcoder/factory-template.
```

- Куда вставить: Не вставлять; выполнить в Browser ChatGPT и GitHub OAuth windows.
- Ожидаемый результат: ChatGPT может найти или открыть `mppcoder/factory-template`.
- Если ошибка: Если GitHub app не виден, проверьте доступность connector для вашего plan/workspace; если repo не индексируется, выполните поиск по `repo:mppcoder/factory-template`.
- Следующий шаг: `FT-040`.

### FT-040. Установить VS Code

- Окно: Browser / Windows installer.
- Делает: Пользователь.
- Зачем: Для default contour `vscode-remote-ssh-codex-extension`.
- Что нужно до начала: Windows PC с правами установки.
- Где взять значения: Официальный сайт: `https://code.visualstudio.com/`.
- Команды для копирования:

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
Successfully installed
```

- Если ошибка: Если `winget` недоступен, скачайте installer с сайта VS Code; если Windows спрашивает разрешение, подтвердите установку.
- Следующий шаг: `FT-050`.

### FT-050. Установить VS Code extensions

- Окно: Windows PowerShell / VS Code.
- Делает: Пользователь.
- Зачем: Remote SSH, GitHub integration, Codex IDE extension, YAML и Markdown нужны для комфортной работы.
- Что нужно до начала: `FT-040`.
- Где взять значения: Extension IDs используются в командах ниже.
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

- Если ошибка: Если `code` не найден, откройте VS Code -> Command Palette -> `Shell Command: Install 'code' command in PATH`, затем повторите; если Codex extension ID изменился, найдите `Codex` или `OpenAI` в Extensions UI.
- Следующий шаг: `FT-060`.

### FT-060. Установить Codex app на ПК

- Окно: Browser / Codex app installer.
- Делает: Пользователь.
- Зачем: Для альтернативного contour `codex-app-remote-ssh`.
- Что нужно до начала: ChatGPT account с Codex access.
- Где взять значения: Официальная Codex app page из OpenAI Codex docs.
- Команды для копирования:

```text
Codex app checklist:
- Скачать Codex app для Windows.
- Установить приложение.
- Открыть приложение.
- Sign in через ChatGPT account.
```

- Куда вставить: Не вставлять; выполнить в Browser и Codex app installer.
- Ожидаемый результат: Codex app открывается и показывает signed-in account.
- Если ошибка: Если app не устанавливается, используйте `vscode-remote-ssh-codex-extension` как основной путь.
- Следующий шаг: `FT-070`.

### FT-070. Установить Codex CLI локально, если нужен локальный test contour

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: Локальный CLI не обязателен для VPS takeover, но полезен для проверки sign in и fallback.
- Что нужно до начала: Node/npm на Windows или возможность установить Node.js.
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

- Если ошибка: Закройте и откройте PowerShell после установки Node; если `npm` не найден, переустановите Node.js LTS.
- Следующий шаг: `FT-080`.

### FT-080. Войти в Codex через ChatGPT account или API key

- Окно: Windows PowerShell / Codex app / VS Code Codex sidebar.
- Делает: Пользователь.
- Зачем: Codex должен быть авторизован до remote takeover.
- Что нужно до начала: `FT-010`, один установленный Codex client.
- Где взять значения: ChatGPT account или API key вводится только в официальный sign-in flow; не вставляйте секреты в repo или handoff.
- Команды для копирования:

```powershell
codex
```

- Куда вставить: Windows PowerShell, если установлен локальный CLI. Для app/extension используйте кнопку Sign in.
- Ожидаемый результат: Codex открывает sign-in flow; после входа показывает интерактивный prompt или signed-in state.
- Если ошибка: Если ранее использовался API key mode и sign in не появляется, выполните `codex logout`, затем снова `codex`.
- Следующий шаг: `FT-090`.

### FT-090. Создать Timeweb Cloud account

- Окно: Browser Timeweb Cloud.
- Делает: Пользователь.
- Зачем: VPS нужен как remote machine, где Codex будет разворачивать factory-template.
- Что нужно до начала: Email/телефон/платежный метод по правилам Timeweb.
- Где взять значения: Аккаунт создается в Timeweb Cloud dashboard.
- Команды для копирования:

```text
Timeweb checklist:
- Account создан.
- Billing/phone/email подтверждены.
- Cloud dashboard открывается.
```

- Куда вставить: Не вставлять; выполнить в Timeweb Cloud UI.
- Ожидаемый результат: Вы видите Timeweb Cloud dashboard.
- Если ошибка: Если account или платеж не подтверждается, остановитесь: без VPS takeover невозможен.
- Следующий шаг: `FT-100`.

### FT-100. Создать VPS Ubuntu 24.04 в Timeweb

- Окно: Timeweb Cloud.
- Делает: Пользователь.
- Зачем: Создать remote host для Codex.
- Что нужно до начала: `FT-090`.
- Где взять значения: `<VPS_IP>` появится в карточке сервера после создания; `<VPS_USER>` обычно `root`.
- Команды для копирования:

```text
VPS choices:
- OS: Ubuntu 24.04
- SSH access: enabled
- SSH key: добавить на шаге FT-120 или выбрать уже добавленный key
- Host alias для локального ПК: factory-vps
```

- Куда вставить: Не вставлять; выбрать значения в Timeweb Cloud UI при создании сервера.
- Ожидаемый результат: Сервер создан, status `running`, публичный IP виден в dashboard.
- Если ошибка: Если UI предлагает только password access, включите SSH key access или добавьте ключ после создания через server settings.
- Следующий шаг: `FT-110`.

### FT-110. Создать SSH-ключ на ПК в Windows PowerShell

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: SSH key позволит безопасно подключаться к VPS без вставки пароля в Codex.
- Что нужно до начала: Windows OpenSSH Client. В Windows 10/11 обычно уже установлен.
- Где взять значения: `<SSH_KEY_NAME>` используйте `factory-template-vps`.
- Команды для копирования:

```powershell
ssh -V
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh"
ssh-keygen -t ed25519 -a 100 -f "$env:USERPROFILE\.ssh\factory-template-vps" -C "factory-template-vps"
Get-Content "$env:USERPROFILE\.ssh\factory-template-vps.pub"
```

- Куда вставить: Windows PowerShell. На вопрос passphrase можно нажать Enter для пустой passphrase или задать свою; если зададите passphrase, храните ее вне repo.
- Ожидаемый результат:

```text
ssh-ed25519 AAAA... factory-template-vps
```

- Если ошибка: Если `ssh` не найден, Windows Settings -> Optional Features -> Add feature -> OpenSSH Client; если файл уже существует, не перезаписывайте его без причины.
- Следующий шаг: `FT-120`.

### FT-120. Добавить SSH public key в Timeweb/VPS

- Окно: Timeweb Cloud / Server settings / SSH keys.
- Делает: Пользователь.
- Зачем: VPS должен доверять public key с вашего ПК.
- Что нужно до начала: `FT-110`, созданный VPS.
- Где взять значения: Public key скопируйте из вывода `Get-Content "$env:USERPROFILE\.ssh\factory-template-vps.pub"`.
- Команды для копирования:

```powershell
Get-Content "$env:USERPROFILE\.ssh\factory-template-vps.pub"
```

- Куда вставить: Windows PowerShell для вывода ключа; затем скопировать всю строку `ssh-ed25519 ...` в Timeweb Cloud -> SSH keys -> Add key или Server -> Access -> SSH keys.
- Ожидаемый результат: В Timeweb Cloud появляется ключ `factory-template-vps`, сервер привязан к этому ключу.
- Если ошибка: Если ключ добавлен после создания VPS, используйте Timeweb console или server settings, чтобы применить ключ к серверу; если UI требует reboot, выполните reboot из панели.
- Следующий шаг: `FT-130`.

### FT-130. Настроить SSH alias `factory-vps`

- Окно: Windows PowerShell / Notepad.
- Делает: Пользователь.
- Зачем: Codex app и VS Code Remote SSH будут подключаться по одному понятному alias.
- Что нужно до начала: `<VPS_IP>`, `<VPS_USER>`, private key file.
- Где взять значения: `<VPS_IP>` в Timeweb server card; `<VPS_USER>` в server access settings, обычно `root`.
- Команды для копирования:

```powershell
notepad "$env:USERPROFILE\.ssh\config"
```

```sshconfig
Host factory-vps
    HostName <VPS_IP>
    User <VPS_USER>
    IdentityFile ~/.ssh/factory-template-vps
    IdentitiesOnly yes
    ServerAliveInterval 30
```

- Куда вставить: Первую команду вставить в Windows PowerShell. Второй block вставить в Notepad, заменить `<VPS_IP>` и `<VPS_USER>`, сохранить файл.
- Ожидаемый результат: Файл `%USERPROFILE%\.ssh\config` содержит host `factory-vps`.
- Если ошибка: Если Notepad спрашивает создать файл, нажмите Yes; если путь с пробелами ломается, используйте именно команду с кавычками.
- Следующий шаг: `FT-140`.

### FT-140. Проверить `ssh factory-vps`

- Окно: Windows PowerShell.
- Делает: Пользователь.
- Зачем: До Codex setup надо доказать, что Windows PC может войти на VPS.
- Что нужно до начала: `FT-130`.
- Где взять значения: Значения уже в SSH config.
- Команды для копирования:

```powershell
ssh factory-vps "hostname && whoami && lsb_release -a"
```

- Куда вставить: Windows PowerShell.
- Ожидаемый результат:

```text
<server-hostname>
root
Distributor ID: Ubuntu
Description:    Ubuntu 24.04...
```

- Если ошибка: `Permission denied (publickey)` означает, что public key не применен к серверу или выбран не тот private key; `Connection timed out` означает, что IP/firewall/сервер недоступны.
- Следующий шаг: `FT-200`.

### FT-200. Выбрать Codex contour

- Окно: Browser / заметки.
- Делает: Пользователь.
- Зачем: Дальше нужен один remote Codex path.
- Что нужно до начала: `ssh factory-vps` работает.
- Где взять значения: Выберите один ID: `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.
- Команды для копирования:

```text
Выбранный contour: vscode-remote-ssh-codex-extension
Fallback contour: codex-app-remote-ssh
```

- Куда вставить: Можно вставить в заметки или оставить как решение.
- Ожидаемый результат: Вы знаете, по какой ветке идти.
- Если ошибка: Если не уверены, идите на `FT-400`.
- Следующий шаг: `FT-300` для Codex app или `FT-400` для VS Code.

### FT-300. Настроить `codex-app-remote-ssh`

- Окно: Windows PowerShell / VPS terminal / Codex app.
- Делает: Пользователь.
- Зачем: Codex app должен открыть remote connection `factory-vps`.
- Что нужно до начала: `FT-060`, `FT-080`, `FT-140`.
- Где взять значения: SSH alias: `factory-vps`; remote folder до clone можно выбрать `/projects` или `/root`.
- Команды для копирования:

```powershell
ssh factory-vps "apt-get update && apt-get install -y nodejs npm"
ssh factory-vps "npm i -g @openai/codex && codex --version"
notepad "$env:USERPROFILE\.codex\config.toml"
```

```toml
remote_connections = true
```

- Куда вставить: Первые две команды в Windows PowerShell. Третью команду в Windows PowerShell, затем добавить `remote_connections = true` в config file. После этого открыть Codex app -> Settings -> Connections -> add/enable `factory-vps` -> выбрать remote folder `/projects` или `/root`.
- Ожидаемый результат:

```text
codex <version>
```

Codex app показывает connection `factory-vps` и может открыть remote thread.
- Если ошибка: Если remote Codex просит sign in, выполните `ssh factory-vps`, затем `codex` на VPS и пройдите sign in; если app не видит connection, перезапустите Codex app после изменения config.
- Следующий шаг: `FT-500`.

### FT-400. Настроить `vscode-remote-ssh-codex-extension`

- Окно: VS Code / Command Palette / VS Code Remote SSH / VPS terminal / Codex sidebar.
- Делает: Пользователь.
- Зачем: Default path: Codex extension работает в VS Code Remote SSH context, где есть remote terminal.
- Что нужно до начала: `FT-040`, `FT-050`, `FT-080`, `FT-140`.
- Где взять значения: SSH alias: `factory-vps`; remote folder до clone: `/projects` или `/root`.
- Команды для копирования:

```text
VS Code UI steps:
1. Ctrl+Shift+P.
2. Remote-SSH: Connect to Host.
3. Выбрать factory-vps.
4. Открыть remote folder /projects или /root.
5. Terminal -> New Terminal.
6. Открыть Codex sidebar.
7. Sign in в Codex extension.
8. Открыть новый Codex chat/window.
```

```bash
hostname && whoami && pwd && lsb_release -a
```

- Куда вставить: Первый block выполнить в VS Code UI. Второй block вставить в VS Code Remote SSH terminal.
- Ожидаемый результат:

```text
root
/projects
Description:    Ubuntu 24.04...
```

Codex sidebar signed in и новый Codex chat/window открыт именно в Remote SSH window.
- Если ошибка: Если Remote SSH не подключается, вернитесь к `FT-140`; если Codex sidebar открылся в локальном VS Code window, закройте его и откройте внутри Remote SSH window.
- Следующий шаг: `FT-500`.

### FT-500. Codex takeover point: вставить один большой handoff

- Окно: Codex app remote thread или VS Code Remote SSH Codex chat/window.
- Делает: Пользователь.
- Зачем: Передать работу Codex. С этого момента Codex-runbook устанавливает tools, clone-ит repo и запускает verify.
- Что нужно до начала: Remote Codex context может выполнять команды на VPS; в terminal или Codex visible context текущий host показывает Ubuntu 24.04.
- Где взять значения: Handoff готовит Browser ChatGPT Project; он должен содержать `Язык ответа Codex: русский`.
- Команды для копирования:

```text
Перед вставкой handoff проверить:
- Я в Codex app remote thread ИЛИ VS Code Remote SSH Codex chat.
- Remote host: factory-vps.
- Remote shell может выполнить hostname/whoami/pwd.
- Handoff вставляется одним цельным блоком.
- В новом Codex chat/window вручную выбран нужный model/reasoning, если picker доступен.
```

- Куда вставить: В Codex app remote thread или VS Code Remote SSH Codex chat/window.
- Ожидаемый результат: Codex отвечает по-русски route receipt и начинает выполнять `02-codex-runbook.md`.
- Если ошибка: Если Codex отвечает из локального context, остановите его, откройте remote context заново и повторите; если handoff разделился на несколько сообщений, создайте новый chat/window и вставьте одним блоком.
- Следующий шаг: `02-codex-runbook.md`, начиная с `CODEX-AUTOMATION`.

## Что пользователь не делает после takeover

После `FT-500` пользователь не выполняет вручную:

- `apt-get install`;
- clone `mppcoder/factory-template`;
- bootstrap/setup;
- verify;
- dashboard update;
- commit/push или verified sync.

Эти действия принадлежат Codex, если нет external blocker, secret prompt или required approval.
