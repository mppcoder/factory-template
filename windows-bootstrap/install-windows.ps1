param(
    [string]$RepoUrl = "https://github.com/mppcoder/factory-template.git",
    [string]$TargetRoot = "/projects/factory-template",
    [string]$IncomingDir = "/projects/factory-template/_incoming"
)

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message"
    Add-Content -Path $script:LogFile -Value "INFO $Message"
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
    Add-Content -Path $script:LogFile -Value "WARN $Message"
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    Add-Content -Path $script:LogFile -Value "FAIL $Message"
}

function Ask-Required {
    param([string]$Prompt)
    while ($true) {
        $value = Read-Host $Prompt
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value.Trim()
        }
        Write-Warn "Please enter a value."
    }
}

function Ask-Optional {
    param([string]$Prompt, [string]$Default)
    $value = Read-Host "$Prompt [$Default]"
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }
    return $value.Trim()
}

function Ask-YesNo {
    param([string]$Prompt, [bool]$DefaultYes = $false)
    $suffix = "[y/N]"
    if ($DefaultYes) { $suffix = "[Y/n]" }
    while ($true) {
        $value = Read-Host "$Prompt $suffix"
        if ([string]::IsNullOrWhiteSpace($value)) { return $DefaultYes }
        switch ($value.Trim().ToLowerInvariant()) {
            "y" { return $true }
            "yes" { return $true }
            "n" { return $false }
            "no" { return $false }
        }
        Write-Warn "Please answer y or n."
    }
}

function Require-Command {
    param([string]$Name, [bool]$Required = $true)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Info "$Name found: $($cmd.Source)"
        return $cmd.Source
    }
    if ($Required) {
        throw "$Name was not found in PATH."
    }
    Write-Warn "$Name not found. Continuing where possible."
    return $null
}

function Copy-ToClipboardSafe {
    param([string]$Text)
    try {
        Set-Clipboard -Value $Text
        Write-Info "Copied text to clipboard."
    } catch {
        Write-Warn "Could not copy to clipboard: $($_.Exception.Message)"
    }
}

function Build-SshArgs {
    param([string]$Port)
    $args = @("-o", "ServerAliveInterval=30")
    if (-not [string]::IsNullOrWhiteSpace($Port)) {
        $args += @("-p", $Port)
    }
    return $args
}

function Build-ScpArgs {
    param([string]$Port)
    $args = @()
    if (-not [string]::IsNullOrWhiteSpace($Port)) {
        $args += @("-P", $Port)
    }
    return $args
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BootstrapRoot = Split-Path -Parent $ScriptDir
if ((Split-Path -Leaf $ScriptDir) -eq "windows-bootstrap") {
    $BootstrapRoot = $ScriptDir
}

$RunRoot = Join-Path $env:TEMP "FactoryTemplateSetup"
$LogDir = Join-Path $RunRoot "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$script:LogFile = Join-Path $LogDir "install-$Stamp.log"
$ReportFile = Join-Path $RunRoot "next-step-report-$Stamp.txt"
New-Item -ItemType File -Force -Path $script:LogFile | Out-Null

Write-Host ""
Write-Host "Factory Template Windows Bootstrapper"
Write-Host "Target VPS path: $TargetRoot"
Write-Host ""
Write-Info "Local log: $script:LogFile"

try {
    Require-Command "ssh.exe" | Out-Null
    Require-Command "scp.exe" | Out-Null
    Require-Command "git.exe" -Required:$false | Out-Null
    $CodeExe = Require-Command "code.exe" -Required:$false

    $HostName = Ask-Required "VPS host/IP"
    $SshUser = Ask-Required "SSH username"
    $SshPort = Ask-Optional "SSH port" "22"
    $Remote = "$SshUser@$HostName"
    $SshArgs = Build-SshArgs -Port $SshPort
    $ScpArgs = Build-ScpArgs -Port $SshPort

    Write-Info "Testing SSH connection to $Remote ..."
    & ssh.exe @SshArgs $Remote "printf 'SSH PASS\n'; uname -a" 2>&1 | Tee-Object -FilePath $script:LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "SSH test failed. Check host, username, port, password/key, and VPS firewall."
    }

    Write-Info "Creating remote incoming folder: $IncomingDir"
    & ssh.exe @SshArgs $Remote "mkdir -p '$IncomingDir' && test -d '$IncomingDir' && printf 'REMOTE INCOMING PASS\n'" 2>&1 | Tee-Object -FilePath $script:LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create remote incoming folder."
    }

    $RemoteScriptLocal = Join-Path $BootstrapRoot "scripts\remote-install-factory-template.sh"
    if (-not (Test-Path $RemoteScriptLocal)) {
        throw "Remote script not found: $RemoteScriptLocal"
    }
    $RemoteScriptRemote = "$IncomingDir/remote-install-factory-template.sh"
    Write-Info "Uploading remote installer script."
    & scp.exe @ScpArgs $RemoteScriptLocal "$Remote`:$RemoteScriptRemote" 2>&1 | Tee-Object -FilePath $script:LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "Could not upload remote installer script."
    }

    Write-Host ""
    Write-Host "Install source:"
    Write-Host "1. Recommended GitHub clone/download from $RepoUrl"
    Write-Host "2. Fallback release archive files from this folder or another local path"
    $UseArchive = Ask-YesNo "Use fallback archive upload instead of GitHub clone?" $false

    if ($UseArchive) {
        $ArchivePath = Ask-Required "Local path to factory-v2.5.1.zip"
        $ManifestPath = Ask-Required "Local path to factory-v2.5.1.manifest.yaml"
        $ChecksumPath = Ask-Required "Local path to factory-v2.5.1.zip.sha256"
        foreach ($item in @($ArchivePath, $ManifestPath, $ChecksumPath)) {
            if (-not (Test-Path $item)) { throw "File not found: $item" }
        }
        Write-Info "Uploading fallback archive files to $IncomingDir"
        & scp.exe @ScpArgs $ArchivePath $ManifestPath $ChecksumPath "$Remote`:$IncomingDir/" 2>&1 | Tee-Object -FilePath $script:LogFile -Append
        if ($LASTEXITCODE -ne 0) {
            throw "Could not upload fallback archive files."
        }
        $ArchiveName = Split-Path -Leaf $ArchivePath
        $ManifestName = Split-Path -Leaf $ManifestPath
        $ChecksumName = Split-Path -Leaf $ChecksumPath
        $RemoteCommand = "bash '$RemoteScriptRemote' --mode archive --target-root '$TargetRoot' --incoming '$IncomingDir' --archive '$ArchiveName' --manifest '$ManifestName' --checksum '$ChecksumName'"
    } else {
        $RemoteCommand = "bash '$RemoteScriptRemote' --mode clone --repo-url '$RepoUrl' --target-root '$TargetRoot' --incoming '$IncomingDir'"
    }

    Write-Info "Running remote install and verification. This can take a while."
    & ssh.exe @SshArgs $Remote $RemoteCommand 2>&1 | Tee-Object -FilePath $script:LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "Remote install failed. See log: $script:LogFile"
    }

    $CodexPromptPath = Join-Path $BootstrapRoot "prompts\codex-install-prompt.txt"
    $ChatGptPromptPath = Join-Path $BootstrapRoot "prompts\chatgpt-project-instructions.txt"
    $CodexPrompt = Get-Content -Path $CodexPromptPath -Raw
    $ChatGptInstructions = Get-Content -Path $ChatGptPromptPath -Raw

    Write-Host ""
    Write-Host "Remote install PASS"
    Write-Host "Open VS Code Remote SSH:"
    Write-Host "  VS Code -> Remote Explorer -> SSH -> connect to $Remote"
    Write-Host "  Open folder: $TargetRoot"
    if ($CodeExe) {
        Write-Host "Detected code.exe. You can also run:"
        Write-Host "  code --remote ssh-remote+$HostName $TargetRoot"
    }

    Write-Host ""
    Write-Host "Codex prompt:"
    Write-Host $CodexPrompt
    if (Ask-YesNo "Copy Codex prompt to clipboard?" $true) {
        Copy-ToClipboardSafe $CodexPrompt
    }

    Write-Host ""
    Write-Host "ChatGPT Project Instructions are saved in:"
    Write-Host "  $ChatGptPromptPath"
    if (Ask-YesNo "Copy ChatGPT Project Instructions to clipboard?" $false) {
        Copy-ToClipboardSafe $ChatGptInstructions
    }

    @"
Factory Template install PASS

VPS: $Remote
Target root: $TargetRoot
Incoming folder: $IncomingDir
Install source: $(if ($UseArchive) { "fallback archive" } else { "GitHub clone/download" })
Local log: $script:LogFile

Next steps:
1. Open VS Code Remote SSH to $Remote.
2. Open folder $TargetRoot.
3. Paste the Codex prompt shown by the installer.
4. In browser, create/update ChatGPT Project with the instructions from windows-bootstrap/prompts/chatgpt-project-instructions.txt.

Manual user-only actions remaining:
- Enter secrets/passwords if prompted.
- Authorize GitHub if needed.
- Create ChatGPT Project in browser.
"@ | Set-Content -Path $ReportFile -Encoding UTF8

    Write-Info "Next-step report: $ReportFile"
    Write-Host "FACTORY TEMPLATE SETUP PASS"
    exit 0
} catch {
    Write-Fail $_.Exception.Message
    Write-Host "FACTORY TEMPLATE SETUP FAIL"
    Write-Host "Log: $script:LogFile"
    exit 1
}
