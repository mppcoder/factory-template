# Установка Factory Template на Windows: latest release

Этот файл для нового пользователя. Правильная граница такая:

```text
Пользователь до installer: PowerShell 7 -> скачать latest дистрибутив -> запустить executable path.
Installer: автоматизирует SSH key, подключение к VPS, установку repo и готовит Codex prompt.
Codex: после вставки handoff работает внутри repo на VPS.
```

## Ссылки

- Последний релиз: https://github.com/mppcoder/factory-template/releases/latest
- Репозиторий: https://github.com/mppcoder/factory-template
- Текущий executable path: `windows-bootstrap/install-windows.ps1`
- Исходник executable path: https://github.com/mppcoder/factory-template/blob/main/windows-bootstrap/install-windows.ps1

`FactoryTemplateSetup.exe` пока не является опубликованным signed installer. Сейчас запускаемый путь для Windows - прозрачный PowerShell script `windows-bootstrap/install-windows.ps1` внутри полного release ZIP.

Не скачивайте один `install-windows.ps1` отдельно: рядом с ним нужны `windows-bootstrap/scripts/` и `windows-bootstrap/prompts/`.

Npm install/download не поддерживается.

## Часть 1. До запуска executable path

В этой части не настраиваем SSH руками. SSH key, проверку существующего ключа, добавление public key на VPS и remote install делает installer.

Нужно только:

```text
1. Открыть PowerShell 7.
2. Скачать latest release package.
3. Проверить SHA256.
4. Распаковать package.
5. Запустить windows-bootstrap/install-windows.ps1.
```

Под рукой должен быть IP вашего VPS. SSH username/password могут понадобиться уже внутри installer, когда он начнет автоматическую настройку подключения.

### Шаг 1. Открыть PowerShell 7

Откройте обычный Windows PowerShell и вставьте:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Если Windows пишет, что пакет уже установлен и обновлений нет, это нормально.

Теперь откройте PowerShell 7:

```text
Start -> PowerShell 7
```

Проверьте версию:

```powershell
$PSVersionTable.PSVersion
```

Ожидаемо: major version `7` или выше.

### Шаг 2. Скачать latest release package

Вставьте блок целиком в PowerShell 7. Он скачивает ZIP, manifest и SHA256 для последнего релиза, проверяет checksum, распаковывает package и сохраняет путь к executable file.

```powershell
$ErrorActionPreference = "Stop"

$Repo = "mppcoder/factory-template"
$Api = "https://api.github.com/repos/$Repo/releases/latest"
$Headers = @{ "User-Agent" = "factory-template-windows-installer" }
$Release = Invoke-RestMethod -Uri $Api -Headers $Headers

$ZipAsset = $Release.assets | Where-Object { $_.name -match '^factory-v[0-9].*\.zip$' } | Select-Object -First 1
$ShaAsset = $Release.assets | Where-Object { $_.name -match '^factory-v[0-9].*\.zip\.sha256$' } | Select-Object -First 1
$ManifestAsset = $Release.assets | Where-Object { $_.name -match '^factory-v[0-9].*\.manifest\.yaml$' } | Select-Object -First 1

if (-not $ZipAsset) { throw "Latest release does not contain factory ZIP asset." }
if (-not $ShaAsset) { throw "Latest release does not contain SHA256 asset." }
if (-not $ManifestAsset) { throw "Latest release does not contain manifest asset." }

$WorkDir = Join-Path $HOME "Downloads\FactoryTemplateLatest"
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

$ZipPath = Join-Path $WorkDir $ZipAsset.name
$ShaPath = Join-Path $WorkDir $ShaAsset.name
$ManifestPath = Join-Path $WorkDir $ManifestAsset.name

Write-Host "Latest release: $($Release.tag_name)"
Write-Host "Downloading: $($ZipAsset.name)"
Invoke-WebRequest -Uri $ZipAsset.browser_download_url -OutFile $ZipPath
Invoke-WebRequest -Uri $ShaAsset.browser_download_url -OutFile $ShaPath
Invoke-WebRequest -Uri $ManifestAsset.browser_download_url -OutFile $ManifestPath

$ExpectedSha = ((Get-Content $ShaPath -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualSha = (Get-FileHash $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ExpectedSha -ne $ActualSha) {
    throw "SHA256 mismatch. Expected $ExpectedSha but got $ActualSha"
}

Write-Host "SHA256 OK: $ActualSha"
Expand-Archive -Path $ZipPath -DestinationPath $WorkDir -Force

$Installer = Get-ChildItem -Path $WorkDir -Recurse -Filter "install-windows.ps1" |
    Where-Object { $_.FullName -match '\\windows-bootstrap\\install-windows\.ps1$' } |
    Select-Object -First 1

if (-not $Installer) {
    throw "windows-bootstrap\install-windows.ps1 not found after unzip."
}

$InstallerInfoPath = Join-Path $WorkDir "installer-path.txt"
$Installer.FullName | Set-Content -Path $InstallerInfoPath -Encoding UTF8

Write-Host ""
Write-Host "Package is ready."
Write-Host "Executable path:"
Write-Host $Installer.FullName
Write-Host ""
Write-Host "Next step: run the executable path in Step 3."
```

Ожидаемый результат:

```text
SHA256 OK: ...
Package is ready.
Executable path:
C:\Users\<you>\Downloads\FactoryTemplateLatest\factory-v...\windows-bootstrap\install-windows.ps1
```

### Шаг 3. Запустить executable path

Вставьте в PowerShell 7:

```powershell
$ErrorActionPreference = "Stop"
$WorkDir = Join-Path $HOME "Downloads\FactoryTemplateLatest"
$InstallerInfoPath = Join-Path $WorkDir "installer-path.txt"

if (Test-Path $InstallerInfoPath) {
    $InstallerPath = (Get-Content $InstallerInfoPath -Raw).Trim()
} else {
    $Installer = Get-ChildItem -Path $WorkDir -Recurse -Filter "install-windows.ps1" |
        Where-Object { $_.FullName -match '\\windows-bootstrap\\install-windows\.ps1$' } |
        Select-Object -First 1
    if (-not $Installer) { throw "windows-bootstrap\install-windows.ps1 not found under $WorkDir" }
    $InstallerPath = $Installer.FullName
}

if (-not (Test-Path $InstallerPath)) {
    throw "Installer path does not exist: $InstallerPath"
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& $InstallerPath
```

## Часть 2. Что делать внутри installer

Дальше работает `install-windows.ps1`. Он автоматизирует SSH и remote setup. Пользователь только отвечает на вопросы.

Рекомендуемые ответы:

```text
VPS host/IP: <IP вашего VPS>
SSH username [root]: Enter
SSH port [22]: Enter
Set up SSH key login to avoid repeated password prompts? [Y/n]: Enter
Target root [/projects/factory-template]: Enter
Incoming dir [/projects/factory-template/_incoming]: Enter
```

Что installer делает сам:

- проверяет локальные `ssh.exe`, `scp.exe`, `ssh-keygen.exe`;
- создает или использует ключ `%USERPROFILE%\.ssh\factory-template-vps-ed25519`;
- если private key уже есть, но `.pub` потерян, восстанавливает public key;
- проверяет, работает ли существующий ключ без пароля;
- если ключ уже работает, не трогает VPS `authorized_keys`;
- если ключ еще не добавлен на VPS, попросит VPS password один раз и добавит public key в `~/.ssh/authorized_keys`;
- дальше использует key login для `ssh` и `scp`, чтобы пароль не вводился постоянно;
- создает `/projects/factory-template/_incoming`;
- устанавливает или обновляет repo `/projects/factory-template`;
- запускает remote quick verification;
- показывает Codex prompt;
- предлагает скопировать Codex prompt в clipboard.

Если installer спрашивает:

```text
Copy Codex prompt to clipboard? [Y/n]
```

нажмите `Enter`.

## Часть 3. Вставить handoff в Codex

После сообщения `FACTORY TEMPLATE SETUP PASS`:

```text
1. Откройте VS Code.
2. Откройте Remote Explorer.
3. Подключитесь к SSH host: root@<IP вашего VPS>.
4. Откройте папку: /projects/factory-template.
5. Откройте Codex chat в VS Code.
6. Вставьте Codex prompt, который installer скопировал в clipboard.
7. Отправьте prompt.
```

Если clipboard не сработал, installer показывает prompt прямо в PowerShell в блоке `Codex prompt:`. Скопируйте этот текст вручную.

## Часть 4. Дальше работает Codex

После вставки handoff в Codex пользователь не должен вручную запускать внутренние repo-команды, если Codex может сделать это сам.

Codex должен:

- открыть и прочитать `template-repo/scenario-pack/00-master-router.md`;
- пройти repo-first route;
- проверить `git status --short --branch`;
- продолжить задачу пользователя внутри repo;
- не просить пользователя запускать внутренние проверки, сборки или release-команды, если доступ к repo уже есть;
- отвечать по-русски.

Пользователь вручную делает только внешние действия:

- вводит VPS password, если installer просит один раз для установки SSH key;
- авторизует GitHub, если это понадобится;
- создает или обновляет ChatGPT Project в browser, если это понадобится;
- подтверждает risky external/destructive actions.

## Если запуск пишет, что install-windows.ps1 не найден

Вставьте этот диагностический блок в PowerShell 7:

```powershell
$WorkDir = Join-Path $HOME "Downloads\FactoryTemplateLatest"
$Installer = Get-ChildItem -Path $WorkDir -Recurse -Filter "install-windows.ps1" |
    Where-Object { $_.FullName -match '\\windows-bootstrap\\install-windows\.ps1$' } |
    Select-Object -First 1

if (-not $Installer) {
    Write-Host "Installer not found under $WorkDir"
    Get-ChildItem -Path $WorkDir -Recurse -Depth 3 | Select-Object FullName
    throw "Download or unzip did not produce windows-bootstrap\install-windows.ps1"
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& $Installer.FullName
```

Чаще всего эта ошибка означает, что вы перешли в папку с неправильным номером версии, распаковали не весь ZIP или скачали только один `.ps1` без соседних файлов.
