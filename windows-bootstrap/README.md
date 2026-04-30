# Установка с Windows для новичка

Цель: довести пользователя с Windows PC и доступом к VPS до готового repo `/projects/factory-template` без ручной цепочки терминальных команд.

## Самый простой путь

Будущий release package может содержать `FactoryTemplateSetup.exe`. Если exe подписан и опубликован рядом с checksum, скачайте:

- `FactoryTemplateSetup.exe`;
- `FactoryTemplateSetup.exe.sha256`, если он опубликован;
- исходные прозрачные scripts из `windows-bootstrap/`.

Проверьте checksum в PowerShell:

```powershell
Get-FileHash .\FactoryTemplateSetup.exe -Algorithm SHA256
```

Если Windows SmartScreen предупреждает об unsigned exe, не игнорируйте предупреждение вслепую: сверяйте SHA256 с release page и используйте прозрачный PowerShell fallback ниже, если подписи нет.

## Прозрачный MVP-путь сейчас

В текущем repo безопасный исполняемый путь - PowerShell script:

```powershell
pwsh
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\windows-bootstrap\install-windows.ps1
```

Рекомендуемая оболочка - PowerShell 7. Если `pwsh` не установлен, установите или обновите PowerShell:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

После установки откройте PowerShell 7 и снова перейдите в распакованную папку `factory-v2.5.5`.

Script не требует admin rights. Он проверяет `ssh.exe`, `scp.exe`, `ssh-keygen.exe`, `git.exe` и `code.exe`, спрашивает VPS host/IP, username и optional SSH port, предлагает настроить SSH key login без постоянного ввода пароля, проверяет SSH, создает `/projects/factory-template/_incoming`, загружает remote helper script и запускает установку.

Installer показывает значения по умолчанию там, где их безопасно предложить:

- `SSH username`: `root`;
- `SSH port`: `22`;
- `TargetRoot`: `/projects/factory-template`;
- `IncomingDir`: `/projects/factory-template/_incoming`;
- install source: GitHub clone/download;
- fallback archive files: `factory-v2.5.5.zip`, `factory-v2.5.5.manifest.yaml`, `factory-v2.5.5.zip.sha256`.

`VPS host/IP` не имеет безопасного default и должен быть введен пользователем.

## SSH без постоянного ввода пароля

После ввода VPS host/IP, username и port installer спросит:

```text
Set up SSH key login to avoid repeated password prompts? [Y/n]
```

Рекомендуемый ответ - просто нажать `Enter`. Installer:

- проверит, существует ли локальный ключ `%USERPROFILE%\.ssh\factory-template-vps-ed25519`;
- если private key есть, но `.pub` потерян, восстановит public key через `ssh-keygen.exe -y`;
- проверит, работает ли существующий ключ уже сейчас через `ssh -o BatchMode=yes -i ...`;
- если ключ уже пускает на VPS без пароля, пропустит запись в `authorized_keys`;
- если ключа нет или он еще не добавлен на VPS, добавит public key в `~/.ssh/authorized_keys`;
- попросит VPS password один раз только если public key еще нужно добавить на VPS;
- дальше будет использовать ключ через `ssh.exe -i ...` и `scp.exe -i ...`.

Если ответить `n`, установка продолжится, но `ssh/scp` могут спрашивать пароль несколько раз.

## Что делает bootstrapper

- Проверяет локальные Windows prerequisites.
- Помогает проверить SSH доступ к VPS.
- Спрашивает VPS host/IP, SSH username и optional SSH port.
- Создает или использует SSH key `%USERPROFILE%\.ssh\factory-template-vps-ed25519`, проверяет уже работающий key login и добавляет public key в VPS `authorized_keys` только если это еще нужно.
- Создает `/projects/factory-template/_incoming`.
- Рекомендует GitHub clone/download из `mppcoder/factory-template`.
- Поддерживает fallback archive upload для `factory-v2.5.5.zip`, `factory-v2.5.5.manifest.yaml`, `factory-v2.5.5.zip.sha256`.
- Запускает remote verification: `POST_UNZIP_SETUP.sh`, release package validator для archive path, затем `bash template-repo/scripts/verify-all.sh quick`.
- Показывает как открыть VS Code Remote SSH.
- Показывает/копирует Codex prompt и ChatGPT Project Instructions.
- Сохраняет local install log и next-step report в `%TEMP%\FactoryTemplateSetup\`.

## Что пользователь делает сам

- Создает и оплачивает VPS.
- Вводит SSH password один раз для установки public key, если на VPS еще нет passwordless SSH; если существующий ключ уже работает, пароль не нужен.
- Авторизует GitHub, если private access когда-нибудь понадобится.
- Создает ChatGPT Project в browser и вставляет Project Instructions.
- Подтверждает risky external/destructive actions. Bootstrapper не удаляет существующий `/projects/factory-template` без явного подтвержденного пути.

## Источник установки

Recommended:

```text
GitHub clone/download from https://github.com/mppcoder/factory-template
```

Fallback release artifact archive files:

```text
factory-v2.5.5.zip
factory-v2.5.5.manifest.yaml
factory-v2.5.5.zip.sha256
```

Npm install/download path не поддерживается: в repo нет `package.json`, npm packaging contract и publish/install policy.

## Граница exe

`FactoryTemplateSetup.exe` пока не собирается автоматически в Linux CI/dev shell. `windows-bootstrap/build/build-windows-bootstrap.ps1` фиксирует placeholder-free packaging contract: exe можно собрать позже из `install-windows.ps1` через reviewed Windows packaging toolchain и затем подписать. До появления подписанного exe источником правды остается PowerShell script plus transparent source files.
