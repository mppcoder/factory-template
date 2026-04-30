# Установка Factory Template на Windows: latest release

Этот файл для нового пользователя. Он ведет от скачивания последней версии до запуска Windows bootstrapper без ручного угадывания номера релиза.

## Ссылки

- Последний релиз: https://github.com/mppcoder/factory-template/releases/latest
- Репозиторий: https://github.com/mppcoder/factory-template
- Текущий executable path: `windows-bootstrap/install-windows.ps1`
- Исходник executable path: https://github.com/mppcoder/factory-template/blob/main/windows-bootstrap/install-windows.ps1

`FactoryTemplateSetup.exe` пока не является опубликованным signed installer. Сейчас запускаемый путь для Windows - прозрачный PowerShell script `windows-bootstrap/install-windows.ps1` внутри последнего release ZIP.

Не скачивайте и не запускайте один `install-windows.ps1` отдельно: рядом с ним нужны `windows-bootstrap/scripts/` и `windows-bootstrap/prompts/`. Используйте блок ниже, он скачивает полный latest release package.

Npm install/download не поддерживается.

## Шаг 1. Открыть PowerShell 7

Откройте обычный PowerShell и вставьте блок целиком:

```powershell
winget install --id Microsoft.PowerShell --source winget
pwsh
```

Если `winget` пишет, что PowerShell уже установлен и обновлений нет, это нормально. Проверьте, что открылась версия 7:

```powershell
$PSVersionTable.PSVersion
```

Ожидаемо: major version `7` или выше.

## Шаг 2. Скачать latest release, проверить SHA256 и запустить installer

Вставьте этот блок целиком в PowerShell 7:

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

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& $Installer.FullName
```

## Шаг 3. Ответы в installer

Когда installer задает вопросы, используйте такие ответы:

```text
VPS host/IP: <IP вашего VPS>
SSH username [root]: Enter
SSH port [22]: Enter
Set up SSH key login to avoid repeated password prompts? [Y/n]: Enter
Target root [/projects/factory-template]: Enter
Incoming dir [/projects/factory-template/_incoming]: Enter
```

Что важно:

- `VPS host/IP` нельзя предложить по умолчанию, его нужно взять из панели VPS.
- `SSH username=root` и `SSH port=22` подходят для обычного нового Ubuntu VPS.
- На вопрос про SSH key login просто нажмите `Enter`: это включает вход по ключу без постоянного ввода пароля.
- Если ключ `%USERPROFILE%\.ssh\factory-template-vps-ed25519` уже есть, installer сначала проверит, работает ли он.
- Если существующий ключ уже пускает на VPS, пароль не понадобится.
- Если ключа еще нет на VPS, пароль понадобится один раз, чтобы добавить public key в `~/.ssh/authorized_keys`.

## Шаг 4. Открыть проект через VS Code Remote SSH

После успешной установки откройте VS Code и подключитесь к VPS:

```text
VS Code -> Remote Explorer -> SSH -> <root@IP вашего VPS>
```

На VPS рабочая папка:

```text
/projects/factory-template
```

## Если запуск снова пишет, что install-windows.ps1 не найден

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
