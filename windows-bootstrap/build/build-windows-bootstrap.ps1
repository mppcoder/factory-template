param(
    [string]$OutputPath = "FactoryTemplateSetup.exe",
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Installer = Join-Path $Root "install-windows.ps1"

if (-not (Test-Path $Installer)) {
    throw "Missing installer script: $Installer"
}

Write-Host "FactoryTemplateSetup.exe packaging contract"
Write-Host ""
Write-Host "Current supported artifact: windows-bootstrap/install-windows.ps1"
Write-Host "Requested exe output: $OutputPath"
Write-Host ""
Write-Host "This repo does not fake an exe wrapper."
Write-Host "To produce FactoryTemplateSetup.exe later, choose and review a Windows packaging toolchain, embed or ship the transparent source scripts, build on Windows, then sign the exe."
Write-Host ""
Write-Host "Required release-side checks before publishing an exe:"
Write-Host "- source scripts are shipped next to the exe;"
Write-Host "- SHA256 file is published;"
Write-Host "- signing status is stated honestly;"
Write-Host "- SmartScreen warning is documented if unsigned;"
Write-Host "- install-windows.ps1 remains a transparent fallback."

if ($CheckOnly) {
    exit 0
}

throw "FactoryTemplateSetup.exe build is not implemented in the current portable repo environment. Use install-windows.ps1 as the MVP executable path."
