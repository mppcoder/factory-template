# Beginner-first путь: Windows PC -> VPS -> первый проект

## Цель

Довести новичка от Windows PC и браузера до готового первого `greenfield-product` без ручных провалов между внутренними Codex-eligible шагами.

Canonical detailed runbooks:

- `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md`
- `docs/operator/runbook-packages/01-factory-template/02-codex-runbook.md`
- `docs/operator/runbook-packages/02-greenfield-product/01-user-runbook.md`
- `docs/operator/runbook-packages/02-greenfield-product/02-codex-runbook.md`

## Настройка Windows-to-VPS

1. Browser ChatGPT: verify ChatGPT/Codex access.
2. Browser GitHub: verify GitHub account and connector.
3. Windows PowerShell: install VS Code and required extensions.
4. Timeweb UI: create Ubuntu 24.04 VPS.
5. Windows PowerShell: create ed25519 SSH key and configure `Host factory-vps`.
6. VS Code Remote SSH: connect to `factory-vps` and open `/projects` or `/root`.
7. Codex extension / Codex chat: sign in inside the Remote SSH window.
8. Codex app remote fallback: use only if the remote thread can execute commands on the VPS.

## Маркер remote context

Before Codex takeover, the active Codex contour must prove remote context:

```bash
whoami
pwd
uname -a
lsb_release -a || cat /etc/os-release
```

Expected: remote Ubuntu VPS output. A local Windows/macOS Codex chat is not a valid takeover context.

## Точка передачи Codex

At `FT-170` and `GF-050`, the user inserts one complete handoff block into a new remote Codex chat/window. After that:

- Codex performs clone/setup/bootstrap/verify/dashboard/sync for `factory-template`.
- Codex creates repo/root/scaffold/verify/sync for the first greenfield project when GitHub write path is available.
- Codex prepares the repo-first instruction for the battle ChatGPT Project.
- The user only creates the battle ChatGPT Project in ChatGPT UI and pastes the prepared instruction.

No hidden second shell step is required from the user after takeover. Troubleshooting shell commands are allowed only as documented fallback when remote Codex context is not ready.

## Граница готового первого проекта

The first project is ready only when Codex closeout includes:

- GitHub repo URL or exact write-path blocker;
- VPS project root;
- generated repo-first core;
- quick verify result;
- commit/push or sync blocker;
- ready repo-first instruction for the battle ChatGPT Project;
- UI steps for the user to paste that instruction in ChatGPT Project settings.

## Не цели

- Do not promise that advisory text auto-switches model/profile/reasoning inside an already-open session.
- Do not ask the user to clone, create repo, add origin, run wizard, verify or sync when Codex has remote shell and GitHub write path.
- Do not use file-based handoff instead of one paste block.
