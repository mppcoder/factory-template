# Чеклист: factory-template

Это зеркало `01-user-runbook.md`. Здесь только пользовательские шаги до takeover. Process checks Codex живут в `02-codex-runbook.md` и `04-verify.md`.

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| FT-000 | [ ] | Windows PC / Browser | Пользователь | Зафиксировать старт: есть ПК, браузер и интернет | `Старт: есть Windows PC, браузер и интернет.` | Понятна граница user setup / Codex automation | PowerShell и браузер открываются | FT-010 |
| FT-010 | [ ] | Browser ChatGPT | Пользователь | Проверить ChatGPT plan с Codex access | ChatGPT -> account menu -> Settings / Plan | Codex access/sign in доступен | Plan status без секретов | FT-020 |
| FT-020 | [ ] | Browser GitHub | Пользователь | Создать/проверить GitHub account | Открыть `https://github.com/mppcoder/factory-template` | Repo page доступна | `<GITHUB_USER>` известен | FT-030 |
| FT-030 | [ ] | Browser ChatGPT / GitHub OAuth | Пользователь | Подключить GitHub к ChatGPT Project/connector | ChatGPT -> Settings -> Apps/Connectors -> GitHub -> Connect | ChatGPT видит `repo:mppcoder/factory-template` | Connector connected | FT-040 |
| FT-040 | [ ] | Windows PowerShell | Пользователь | Установить VS Code | `winget install --id Microsoft.VisualStudioCode -e` | VS Code установлен | VS Code запускается | FT-050 |
| FT-050 | [ ] | Windows PowerShell / VS Code | Пользователь | Установить VS Code extensions | `code --install-extension ms-vscode-remote.remote-ssh` и остальные commands из `FT-050` | Extensions установлены | Extensions view показывает нужные extensions | FT-060 |
| FT-060 | [ ] | Browser / Codex app | Пользователь | Установить Codex app на ПК | Официальная Codex app page -> install -> sign in | Codex app signed in или выбран fallback VS Code | App открыт или fallback зафиксирован | FT-070 |
| FT-070 | [ ] | Windows PowerShell | Пользователь | Установить Codex CLI локально, если нужен local test contour | `winget install --id OpenJS.NodeJS.LTS -e`; `npm i -g @openai/codex`; `codex --version` | `codex <version>` или шаг осознанно пропущен | Вывод версии или skip note | FT-080 |
| FT-080 | [ ] | Codex app / VS Code Codex sidebar / PowerShell | Пользователь | Войти в Codex | `codex` или Sign in button | Codex signed in | Signed-in state без секретов | FT-090 |
| FT-090 | [ ] | Timeweb Cloud | Пользователь | Создать Timeweb Cloud account | Timeweb Cloud signup / login | Dashboard доступен | Dashboard открыт | FT-100 |
| FT-100 | [ ] | Timeweb Cloud | Пользователь | Создать VPS Ubuntu 24.04 | OS Ubuntu 24.04, user root, SSH key access, public IP `<VPS_IP>` | VPS running | `<VPS_IP>` записан | FT-110 |
| FT-110 | [ ] | Windows PowerShell | Пользователь | Создать SSH key | `$KEY="$env:USERPROFILE\.ssh\factory_timeweb_ed25519"`; `ssh-keygen -t ed25519 -C "factory-template-timeweb-vps" -f $KEY`; `Get-Content "$KEY.pub"` | Public key `ssh-ed25519 ...` выведен | Public key скопирован | FT-120 |
| FT-120 | [ ] | Timeweb Cloud / Windows PowerShell | Пользователь | Добавить public SSH key в Timeweb/VPS | `Get-Content "$KEY.pub"` -> Timeweb Cloud -> SSH-ключи -> Add key | Key добавлен к VPS | Timeweb показывает key | FT-130 |
| FT-130 | [ ] | Windows PowerShell / Notepad | Пользователь | Настроить SSH config | `notepad $env:USERPROFILE\.ssh\config`; `Host factory-vps ... IdentityFile ~/.ssh/factory_timeweb_ed25519` | Alias `factory-vps` сохранен | Config содержит host block | FT-140 |
| FT-140 | [ ] | Windows PowerShell | Пользователь | Проверить SSH | `ssh factory-vps` | `root@<server-hostname>:~#` | SSH prompt или error text | FT-150A или FT-150B |
| FT-150A | [ ] | Windows PowerShell / Codex app | Пользователь | Настроить Codex App + Remote SSH | `ssh factory-vps "apt-get update && apt-get install -y nodejs npm"`; Codex app -> Settings -> Connections -> `factory-vps` | Codex app remote thread выполняет команды на VPS | `whoami` в app remote thread -> `root` | FT-160 |
| FT-150B | [ ] | VS Code Remote SSH / Codex sidebar | Пользователь | Настроить VS Code Remote SSH + Codex IDE extension | Ctrl+Shift+P -> Remote-SSH: Connect to Host -> `factory-vps`; terminal checks | VS Code SSH window и Codex sidebar работают remote | Status bar SSH + terminal `whoami` | FT-160 |
| FT-160 | [ ] | Codex app / VS Code Remote SSH | Пользователь | Выбрать рабочий Codex contour | Выбрать `vscode-remote-ssh-codex-extension` или `codex-app-remote-ssh` | Один contour выбран | Название contour и remote command result | FT-170 |
| FT-170 | [ ] | Remote Codex chat/thread | Пользователь | Вставить один большой handoff | Новый chat/window -> ручной picker -> вставить `<handoff block>` одним сообщением | Codex начинает automation после приема handoff | Remote shell check | STOP или FT-180 |
| FT-180 | [ ] | Windows PowerShell / VS Code / Codex app | Пользователь | Прислать диагностику, если Codex не стартовал | `ssh factory-vps`; заполнить contour/error/output checklist | Есть screenshot/error text, output SSH, contour A/B | Диагностика без секретов | Вернуться к FT-170 |
