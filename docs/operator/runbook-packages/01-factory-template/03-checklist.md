# Чеклист: factory-template

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.

- [ ] `FT-000` стартовое состояние подтверждено: есть Windows PC, браузер и интернет.
- [ ] `FT-010` ChatGPT plan с Codex access проверен.
- [ ] `FT-020` GitHub account создан или проверен.
- [ ] `FT-030` GitHub подключен к ChatGPT Project/connector.
- [ ] `FT-040` VS Code установлен.
- [ ] `FT-050` VS Code extensions установлены: Remote - SSH, GitHub Pull Requests and Issues, Codex IDE extension, YAML, Markdown All in One, Docker при deploy contour.
- [ ] `FT-060` Codex app установлен или явно пропущен, если выбран только VS Code contour.
- [ ] `FT-070` Codex CLI локально установлен, если нужен local test contour.
- [ ] `FT-080` Codex sign in проверен через ChatGPT account или API key.
- [ ] `FT-090` Timeweb Cloud account создан.
- [ ] `FT-100` VPS Ubuntu 24.04 создан.
- [ ] `FT-110` SSH key создан на Windows PC.
- [ ] `FT-120` SSH public key добавлен в Timeweb/VPS.
- [ ] `FT-130` SSH alias `factory-vps` настроен.
- [ ] `FT-140` `ssh factory-vps` проходит и показывает Ubuntu 24.04.
- [ ] `FT-200` выбран один contour: `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.
- [ ] `FT-300` или `FT-400` выполнен до remote Codex context.
- [ ] `FT-500` Codex takeover point достигнут: handoff вставлен одним цельным блоком в remote Codex thread/chat.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.

- [ ] `00-master-router.md` прочитан из repo.
- [ ] Профиль подтвержден как `factory-template as greenfield-product + factory-producer-owned layer`.
- [ ] Advisory/policy layer отделен от executable routing layer.
- [ ] Handoff route receipt или self-handoff выбран по `launch_source`.
- [ ] Defect-capture создан для найденных mismatch.
- [ ] Codex сам выполнил VPS preflight, package install, clone/sync, bootstrap/setup discovery.
- [ ] Обновлены только релевантные docs/scripts/validators/manifests.
- [ ] Dashboard отражает current phase, gates, blockers и next action.
- [ ] Verification выполнена targeted или quick/full по затронутому контуру.
- [ ] Release-facing docs обновлены, если change release-facing.
- [ ] Verified sync выполнен при green verify и доступном `origin`, либо зафиксирован blocker.
