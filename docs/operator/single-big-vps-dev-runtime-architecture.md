# Архитектура single big VPS dev/runtime

Canonical source: `docs/architecture/vps-project-hosting-topologies.md`.

## Статус

`single-host` является supported topology для solo/beginner operator: один большой VPS может держать factory-template, несколько dev workspaces и несколько runtime/prod контуров, если dev и runtime строго разделены.

Это не downstream/battle application proof. Реальный downstream proof начинается только после выбора downstream repo, real `APP_IMAGE`, approved target, secrets outside repo, deploy approval, healthcheck, backup, restore, rollback и sanitized transcript.

## Layout / размещение

```text
/projects/factory-template
/projects/project-a
/projects/project-b
/srv/project-a-prod
/srv/project-b-prod
/etc/project-a.env
/etc/project-b.env
/etc/systemd/system/project-a.service
/etc/systemd/system/project-b.service
/etc/nginx/sites-available/project-a.conf
/etc/nginx/sites-available/project-b.conf
/var/backups/projects/project-a
/var/backups/projects/project-b
```

## Два режима

- Dev workspace per project: `/projects/<repo>`. Здесь живут git repo, VS Code Remote SSH workspace, Codex work, build/test dependencies and factory automation.
- Prod runtime per project: `/srv/<project>-prod`. Здесь живут rendered compose/runtime files, runtime copy, project service and operational scripts.

Production не запускается напрямую из `/projects`.

## Правила изоляции

- Env/secrets не в repo; real env lives in `/etc/<project>.env` with restricted permissions.
- Project-owned data, backups, runtime transcripts and rollback tags are per project.
- Template-owned files stay in `factory-template` and generated template-owned zones; project-owned data is not overwritten by template sync.
- Nginx/server-level shared infra is separate from each project runtime.
- `systemd` unit names, compose project names, Docker networks, domains, ports, backup paths and rollback targets are unique per project.
- Backups and restore/rollback drills are per project.

## Маленькие VPS

Small VPS targets remain allowed as:

- optional runtime-only targets;
- staging/disposable restore targets;
- backup or fallback targets.

They are not the default heavy dev/Codex/build host.

## Операторский чеклист

- Confirm SSH access to the big VPS and record remote context marker: `whoami`, `pwd`, `uname -a`, `lsb_release -a || cat /etc/os-release`.
- Create `/projects` and clone repos under `/projects/<repo>`.
- Open VS Code Remote SSH to the relevant `/projects/<repo>` root; Codex app remote is fallback when it can execute commands on the VPS.
- Create `/srv/<project>-prod` only for runtime copies.
- Store real env in `/etc/<project>.env`; commit only `.env.example`.
- Render compose/runtime files under `/srv/<project>-prod` with project-unique compose project name and network.
- Configure one nginx site and one systemd service per project.
- Verify with `docker compose config`, `nginx -t`, `systemd-analyze verify` where available, local healthcheck and public HTTPS healthcheck when public runtime is in scope.
- Before deploy, create backup; before proof pass, test restore on disposable/staging target and run rollback drill.

## Не делать

- Не смешивать `/projects` и `/srv`.
- Не хранить secrets in repo, reports or transcript.
- Не запускать production from dev workspace.
- Не считать placeholder app proof реального продукта.
- Не считать dev healthcheck production proof.
- Не объединять несколько проектов в один compose/systemd/nginx contour without an explicit architectural decision.
