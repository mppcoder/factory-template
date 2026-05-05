# Журнал изменений

## Не выпущено
- physical root normalization: legacy/factory-only top-level folders moved under project core, `tests/`, `docs/operator/`, `project-knowledge/` or bounded `factory/producer/*`; tree contract now rejects old active root folders.
- Universal Codex Handoff Factory MVP добавляет repo-native `FT-TASK` слой для всех Codex-задач, не только bugs.
- Added task registry, allocator, issue bridge, handoff preview/prepare/status/queue commands and validators under `template-repo/scripts/`.
- Added GitHub Issue templates, Russian one-paste runbook, lifecycle dashboard integration and explicit Symphony/OpenClaw/Hermes future boundaries without daemon/runtime dependency.
- `verify-all quick` now includes Universal Task Control smoke with positive flow and explicit negative fixtures under `tests/universal-task-control/`.
- Downstream materialization now covers generated projects with `.chatgpt/task-registry.yaml`, root `scripts/*` commands, `.github/ISSUE_TEMPLATE/*.yml`, downstream operator docs and report target dirs.
- `verify-all quick` now includes a temporary generated-project Universal Task Control smoke that does not launch Codex and does not use GitHub API.
- Existing downstream sync guidance explicitly forbids blind overwrite of `.chatgpt/task-registry.yaml` when user tasks or evidence are present.

## 2.5.8
- `WINDOWS_INSTALL_LATEST.md` now preserves the executable automation boundary.
- before executable launch the user only opens PowerShell 7, downloads/verifies/unzips latest release package and runs `windows-bootstrap/install-windows.ps1`.
- SSH key setup, existing-key checks, VPS connection, remote install and Codex prompt copy are described as installer-owned automation.
- after handoff, repo-first work is described as Codex-owned work inside the VPS repo.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.8.zip`, `factory-v2.5.8.manifest.yaml` and `factory-v2.5.8.zip.sha256`.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not published as a real exe in this release.
- npm install/download path remains unsupported.

## 2.5.7
- `WINDOWS_INSTALL_LATEST.md` now puts user preparation before executable launch.
- Step 0 lists required VPS inputs before any installer run: IP, SSH username, SSH password/key and port.
- PowerShell 7 and OpenSSH Client checks happen before latest package download.
- latest release download/checksum/unzip is separated from launching `windows-bootstrap/install-windows.ps1`.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.7.zip`, `factory-v2.5.7.manifest.yaml` and `factory-v2.5.7.zip.sha256`.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not published as a real exe in this release.
- npm install/download path remains unsupported.

## 2.5.6
- one-file Windows beginner install guide added as `WINDOWS_INSTALL_LATEST.md`.
- the guide resolves the latest GitHub Release dynamically through `releases/latest` instead of hard-coding `factory-vX.Y.Z`.
- the copy-paste PowerShell block downloads ZIP, manifest and SHA256, verifies checksum, unzips and locates `windows-bootstrap/install-windows.ps1`.
- PowerShell 7 guidance, safe defaults and default-yes SSH key login remain the beginner path.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.6.zip`, `factory-v2.5.6.manifest.yaml` and `factory-v2.5.6.zip.sha256`.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not published as a real exe in this release.
- npm install/download path remains unsupported.

## 2.5.5
- Windows bootstrapper checks existing SSH key login with `ssh -o BatchMode=yes -i <key>` before touching VPS `authorized_keys`.
- If the existing key already works, password prompt and `authorized_keys` update are skipped.
- If private key exists but `.pub` is missing, the public key is recreated with `ssh-keygen.exe -y`.
- If key installation is needed, key login is verified again after updating `authorized_keys`.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.5.zip`, `factory-v2.5.5.manifest.yaml` and `factory-v2.5.5.zip.sha256`.
- npm install/download path remains unsupported.

## 2.5.4
- Windows bootstrapper now offers default-yes SSH key setup to avoid repeated VPS password prompts.
- Installer creates or reuses `%USERPROFILE%\\.ssh\\factory-template-vps-ed25519`.
- Public key is added to VPS `~/.ssh/authorized_keys`; the password is needed once if key login is not already configured.
- Later installer steps use `ssh.exe -i` and `scp.exe -i`.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.4.zip`, `factory-v2.5.4.manifest.yaml` and `factory-v2.5.4.zip.sha256`.
- npm install/download path remains unsupported.

## 2.5.3
- Windows bootstrapper now recommends PowerShell 7 and shows the `winget` install command.
- Installer prompts include safe defaults: `SSH username=root`, `SSH port=22`, `TargetRoot=/projects/factory-template`, `IncomingDir=/projects/factory-template/_incoming`.
- `VPS host/IP` remains required user input without a default.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.3.zip`, `factory-v2.5.3.manifest.yaml` and `factory-v2.5.3.zip.sha256`.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not published as a real exe in this release.
- npm install/download path remains unsupported.

## 2.5.2
- Windows beginner bootstrapper MVP is included in the downloadable release artifact.
- GitHub clone/download from `mppcoder/factory-template` remains the recommended install path.
- `windows-bootstrap/install-windows.ps1` is the current Windows beginner executable path.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not published as a real exe in this release.
- archive + manifest + SHA256 fallback is published as `factory-v2.5.2.zip`, `factory-v2.5.2.manifest.yaml` and `factory-v2.5.2.zip.sha256`.
- npm install/download path remains unsupported.

## 2.5.1
- release package assembly now produces canonical zip, sidecar manifest and SHA256 checksum for install-from-scratch verification.
- fallback manual upload path is documented through `/projects/factory-template/_incoming`.
- npm install/download path is explicitly unsupported until a real `package.json` packaging contract exists.

## 2.5.0
- `G25-GA` закрыт как passed на основании full-KPI evidence.
- release docs, manifests, launcher metadata и closeout artifacts синхронизированы под `factory-v2.5.0`.
- добавлен validator для GA KPI evidence перед `ga_ready: true`.

## 2.4.4
- canonical preset naming переведён на нейтральные factory names с compatibility aliases для legacy preset names
- предметный reference-case вынесен из core/release-facing слоя в optional domain pack
- release docs, manifests, examples и closeout artifacts синхронизированы под `factory-v2.4.4`

## 2.4.3
- собран полный release-facing пакет по самому `factory-template`
- добавлен root-level `RELEASE_NOTES.md` как canonical published notes source
- архитектурный reference-doc теперь покрывает функционал, дерево repo и все ключевые workflow от intake до выпуска релиза
- release-facing docs, source/export profiles и closeout artifacts синхронизированы под `factory-v2.4.3`

## 2.4.2
- ChatGPT Project переведён на repo-first режим с обязательным чтением GitHub repo и `00-master-router.md`
- canonical archive `sources-pack-core-20` закреплён как steady-work snapshot, а не как единственный daily upload
- boundary guidance и release docs выровнены под hybrid-модель `direct hot-set + canonical archive`

## 2.4.1
- в отдельный patch-релиз вынесены ops-policy, phase detection и release-facing improvements из бывшего `Unreleased`
- release metadata, bundle name и GitHub tag синхронизированы под `factory-v2.4.1`
- release checklist и release note приведены к финальному go-статусу

## 2.4.0
- `rc2-smokefix` переведен в финальный релиз после полного прохождения smoke/examples/matrix
- метаданные и build output синхронизированы под финальное имя `factory-v2.4.0`
- smoke-fix включен в основной пакет

## 2.4.0-rc2
- выровнены версии и release labels между root, template, meta-template и working examples
- `RELEASE_BUILD.sh` переведен на чтение версии из `VERSION.md`
- `PRE_RELEASE_AUDIT.sh` дополнен проверками version drift и legacy-ссылок

## 2.4.0-rc1-consistency
- добавлен единый versioning/documentation layer для фабрики, шаблона и generated projects
- examples и generated project templates получили `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

## 2.4.0-base
- введен defect-capture layer
- добавлены process-файлы и шаблоны для bug report / factory feedback / ChatGPT handoff

## 2.3.7
- stabilization-релиз
- matrix runner и controlled back-sync
