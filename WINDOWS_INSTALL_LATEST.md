# Установка Factory Template на Windows: latest release

Этот файл для нового пользователя. Порядок важен: сначала подготовьте VPS и Windows, потом скачайте полный latest release package, и только после этого запускайте текущий executable path `windows-bootstrap/install-windows.ps1`.

## Ссылки

- Последний релиз: https://github.com/mppcoder/factory-template/releases/latest
- Репозиторий: https://github.com/mppcoder/factory-template
- Текущий executable path: `windows-bootstrap/install-windows.ps1`
- Исходник executable path: https://github.com/mppcoder/factory-template/blob/main/windows-bootstrap/install-windows.ps1

`FactoryTemplateSetup.exe` пока не является опубликованным signed installer. Сейчас запускаемый путь для Windows - прозрачный PowerShell script `windows-bootstrap/install-windows.ps1` внутри полного release ZIP.

Не скачивайте и не запускайте один `install-windows.ps1` отдельно: рядом с ним нужны `windows-bootstrap/scripts/` и `windows-bootstrap/prompts/`.

Npm install/download не поддерживается.

## Шаг 0. Что должно быть готово до запуска installer

До запуска `install-windows.ps1` подготовьте:

```text
1. Windows PC с интернетом.
2. VPS с Ubuntu 24.04 или близкой Ubuntu/Debian системой.
3. IP адрес VPS.
4. SSH username. Для нового VPS обычно: root.
5. SSH password от VPS или уже настроенный SSH key.
6. Открытый SSH port. Обычно: 22.
```

Если VPS еще не создан, сначала создайте его в панели провайдера и дождитесь письма/экрана с IP и root password. Без IP VPS installer запускать рано: первый обязательный вопрос будет `VPS host/IP`.

## Шаг 1. Установить или открыть PowerShell 7

Откройте обычный Windows PowerShell и вставьте:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Если Windows пишет, что пакет уже установлен и обновлений нет, это нормально.

Теперь откройте PowerShell 7:

```text
Start -> PowerShell 7
```

В PowerShell 7 проверьте версию:

```powershell
$PSVersionTable.PSVersion
```

Ожидаемо: major version `7` или выше.

## Шаг 2. Проверить SSH tools на Windows

В PowerShell 7 вставьте:

```powershell
Get-Command ssh.exe
Get-Command scp.exe
Get-Command ssh-keygen.exe
```

Если все три команды показывают путь к `.exe`, переходите дальше.

Если команда не найдена, откройте PowerShell от имени администратора и установите OpenSSH Client:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Потом снова откройте PowerShell 7 и повторите проверку.

## Шаг 3. Скачать latest release package и проверить SHA256

Этот блок только скачивает, проверяет и распаковывает latest release. Он еще не запускает installer.

Вставьте блок целиком в PowerShell 7:

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
Write-Host "Installer path:"
Write-Host $Installer.FullName
Write-Host ""
Write-Host "Next step: read Step 4, then run Step 5."
```

Ожидаемый результат:

```text
SHA256 OK: ...
Package is ready.
Installer path:
C:\Users\<you>\Downloads\FactoryTemplateLatest\factory-v...\windows-bootstrap\install-windows.ps1
```

## Шаг 4. Проверить данные перед запуском executable path

Перед запуском installer убедитесь, что у вас под рукой есть:

```text
VPS host/IP: <IP вашего VPS>
SSH username: root
SSH port: 22
VPS password: <пароль из панели/письма провайдера>
```

Также решите заранее:

```text
Set up SSH key login to avoid repeated password prompts? -> Enter
Target root -> Enter
Incoming dir -> Enter
```

Рекомендованный путь - нажимать `Enter` на default questions. Installer сам создаст или использует ключ `%USERPROFILE%\.ssh\factory-template-vps-ed25519`, сначала проверит уже существующий ключ и не будет трогать VPS `authorized_keys`, если ключ уже работает.

## Шаг 5. Запустить executable path

Теперь, когда VPS-данные готовы и package скачан полностью, вставьте в PowerShell 7:

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

## Шаг 6. Ответы в installer

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

## Шаг 7. Открыть проект через VS Code Remote SSH

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
