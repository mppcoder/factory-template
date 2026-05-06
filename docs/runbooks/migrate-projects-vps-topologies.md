# Runbook: миграция проектов в VPS hosting topology

## Область

This runbook migrates one or more projects from an old VPS/runtime into the standard described in `docs/architecture/vps-project-hosting-topologies.md`.

Supported topology modes:

- `single-host`: dev/build/factory and runtime area on the same big VPS.
- `split-host`: big Dev VPS is source/build/deploy control plane; each project runtime runs on a separate minimal VPS.

This runbook does not execute real production migration by itself. Real VPS IPs, domains, secrets, DNS, cutover and destructive decommission require operator approval.

## Входные данные

- Project slug, for example `my-project`.
- GitHub repo URL and current default branch.
- Old VPS inventory.
- Selected topology mode: `single-host` or `split-host`.
- Runtime host:
  - `localhost` for `single-host`;
  - SSH target for `split-host`, without passwords or private keys in repo.
- Project domain and health endpoint.
- Runtime port for loopback app bind.

## Этап 0: inventory старого VPS

Collect evidence without secrets:

- OS version and package state.
- Docker and Compose versions.
- Nginx version and enabled site configs.
- Systemd services for the app.
- Current app paths.
- Current env paths, file permissions and owner, without printing values.
- Exposed ports and firewall/security group.
- Domains and DNS target.
- Backup paths and retention.
- DB/data volumes and dump procedure.
- Health endpoints: local and public.
- Current git repo path and branch if a repo exists on the old VPS.

Expected evidence:

- Sanitized command transcript.
- List of paths and service names.
- No env values, tokens, passwords, private keys or connection strings.

Stage gate:

- Inventory exists and old runtime is restorable or backup status is explicitly blocked.

Rollback criteria:

- Stage 0 changes nothing.

## Этап 1: проверка GitHub/source status

On the old repo if present:

```bash
git status --short --branch
git remote -v
git log --oneline -5
```

On the new dev workspace:

```bash
cd /projects/<project>
git status --short --branch
git remote -v
```

Rules:

- GitHub remains source of truth.
- Commit and push current source before migration, or create a patch backup if old worktree cannot be pushed.
- Do not copy runtime-only edits from `/srv` back into source without review.

Stage gate:

- Source status is clean or dirty state is captured as a migration blocker.

Rollback criteria:

- No runtime changes until source status is understood.

## Этап 2: выбор topology

Record:

- `topology_mode`: `single-host` or `split-host`;
- reason;
- accepted blast radius;
- runtime host;
- rollback target;
- old VPS grace period.

Use `single-host` when one big VPS is acceptable for dev and several small runtimes. Use `split-host` when physical host separation, lower blast radius or per-customer/domain isolation matters.

Hybrid is allowed, but the decision is per project, not implicit global state.

Stage gate:

- Decision is recorded in the runtime inventory.

Rollback criteria:

- If topology decision is wrong before deploy, rerender inventory/templates and rerun preflight; no runtime decommission occurs.

## Этап 3: подготовка dev workspace

On the big Dev VPS:

```bash
mkdir -p /projects
cd /projects
git clone <github-url> <project>
cd /projects/<project>
git status --short --branch
```

Rules:

- Build and test dependencies stay in `/projects/<project>`.
- Codex and VS Code Remote SSH work in `/projects/<project>`.
- Do not put real prod env in the repo.
- Do not run prod directly from `/projects`.

Stage gate:

- `/projects/<project>` exists and points to GitHub.

Rollback criteria:

- Remove only the incomplete dev clone if it has no unpushed work; otherwise keep it for audit.

## Этап 4A: подготовка runtime target для `single-host`

On the big VPS:

```bash
sudo mkdir -p /srv/<project>-prod
sudo mkdir -p /var/backups/projects/<project>
sudo install -d -m 0750 /srv/<project>-prod
sudo install -d -m 0750 /var/backups/projects/<project>
```

Runtime files:

- `/srv/<project>-prod/compose.yaml`;
- `/etc/<project>.env`;
- `/etc/systemd/system/<project>.service`;
- `/etc/nginx/sites-available/<project>.conf`;
- `/etc/nginx/sites-enabled/<project>.conf`.

Stage gate:

- Runtime path and backup path exist on the same VPS, separate from `/projects`.

Rollback criteria:

- Stop the new service and restore previous runtime backup if deploy fails.

## Этап 4B: подготовка runtime target для `split-host`

On the runtime VPS:

```bash
sudo mkdir -p /srv/<project>-prod
sudo mkdir -p /var/backups/projects/<project>
sudo install -d -m 0750 /srv/<project>-prod
sudo install -d -m 0750 /var/backups/projects/<project>
```

On the big Dev VPS:

- store only sanitized SSH inventory metadata;
- do not commit passwords, private keys or real env;
- validate runtime target over SSH before deploy.

Stage gate:

- Runtime VPS has Docker Compose, nginx, systemd and backup path ready.

Rollback criteria:

- Runtime VPS remains isolated; old VPS remains active during grace period.

## Этап 5: подготовка env

Create the real env outside repo:

```bash
sudo install -m 0600 -o root -g root /dev/null /etc/<project>.env
sudoedit /etc/<project>.env
sudo chmod 600 /etc/<project>.env
```

Rules:

- Use `deploy/templates/env.project.example` only as a placeholder source.
- Never commit `/etc/<project>.env`.
- Never paste real values into docs, tickets, transcripts or closeout.

Stage gate:

- Env exists outside repo and has `600` permissions.

Rollback criteria:

- Restore previous env backup before restarting service if env change fails.

## Этап 6: render compose/systemd/nginx

Render from:

- `deploy/templates/docker-compose.project.template.yml`;
- `deploy/templates/systemd.project.service.template`;
- `deploy/templates/nginx.project.conf.template`;
- `deploy/templates/project-runtime-inventory.template.yaml`.

Required placeholders:

- `PROJECT_SLUG`;
- `PROJECT_REPO_PATH`;
- `PROJECT_RUNTIME_PATH`;
- `PROJECT_ENV_FILE`;
- `PROJECT_DOMAIN`;
- `PROJECT_INTERNAL_PORT`;
- `PROJECT_HEALTH_PATH`;
- `COMPOSE_PROJECT_NAME`;
- `DOCKER_NETWORK`;
- `TOPOLOGY_MODE`;
- `RUNTIME_HOST`.

Preflight:

```bash
docker compose --env-file /etc/<project>.env -f /srv/<project>-prod/compose.yaml config
sudo systemd-analyze verify /etc/systemd/system/<project>.service
sudo nginx -t
```

Stage gate:

- Compose config, systemd and nginx checks pass or blockers are recorded.

Rollback criteria:

- Restore previous compose/service/nginx backups.

## Этап 7: включение HTTPS

USER ACTIONS:

- choose domain;
- set DNS `A/AAAA` to the runtime host;
- approve certificate/ACME flow when required;
- open ports `80` and `443` on the runtime host firewall/security group.

Rules:

- App stays on `127.0.0.1:<PROJECT_INTERNAL_PORT>`.
- Nginx is the public edge.
- Healthcheck must pass through the final public domain before cutover is accepted.

Stage gate:

- Public healthcheck passes through `https://<domain><health-path>` or cutover remains pending.

Rollback criteria:

- Repoint DNS to old VPS or disable new nginx site if public route fails.

## Этап 8: backup

Before deploy:

- runtime dir;
- `/etc/<project>.env`;
- systemd service;
- nginx conf;
- compose file;
- runtime inventory;
- DB dump/data volume when applicable.

Use:

```bash
bash scripts/deploy/backup-project-runtime.template.sh
```

after rendering placeholders or use equivalent operator commands.

Stage gate:

- Backup artifact exists under `/var/backups/projects/<project>` and is readable by the operator.

Rollback criteria:

- No deploy/cutover without backup; if backup fails, keep old runtime active.

## Этап 9: deploy

Run dry-run first:

```bash
bash scripts/deploy/deploy-project.template.sh --dry-run
```

Then approved deploy:

```bash
bash scripts/deploy/deploy-project.template.sh --yes
```

For `split-host`, the deploy script uses the configured runtime SSH target; no real secrets are committed.

Stage gate:

- Service restarts.
- `systemctl status <project>` is healthy.
- Local healthcheck passes.
- Public healthcheck passes through nginx/domain.
- Sanitized report is written.

Rollback criteria:

- Restore previous runtime/config backup or previous Git/image tag; old VPS remains available.

## Этап 10: rollback proof

Perform rollback proof before declaring migration accepted:

- record current healthy Git tag/image tag;
- deploy candidate;
- restore previous Git tag/image tag;
- restart service;
- run local and public healthcheck;
- record result without secrets.

Stage gate:

- Rollback proof passes.

Rollback criteria:

- If rollback proof fails, keep traffic on old VPS or revert DNS to old runtime.

## Этап 11: restore proof

Perform restore proof:

- restore runtime dir to a disposable/staging target or approved recovery target;
- restore env/systemd/nginx/compose from backup;
- restore DB/data if applicable;
- reload systemd and nginx;
- start service;
- run local and public/staging healthcheck.

Stage gate:

- Restore proof passes or cutover remains pending.

Rollback criteria:

- Do not delete old VPS until restore proof passes.

## Этап 12: grace period

During grace period:

- keep old VPS online or restorable;
- monitor logs and healthchecks;
- keep final backup from old runtime;
- do not remove DNS fallback until acceptance.

Stage gate:

- Operator approves final cutover after monitoring window.

Rollback criteria:

- Repoint DNS to old VPS or restart old service if new runtime fails.

## Этап 13: decommission old runtime

USER ACTIONS:

- approve old VPS decommission;
- confirm final backup retention;
- approve DNS/firewall cleanup.

Rules:

- No decommission before healthcheck, backup, restore proof, rollback proof and explicit operator approval.
- Keep sanitized evidence transcript in repo; keep raw sensitive runtime artifacts outside repo.

Stage gate:

- Old runtime decommission is explicitly accepted.

Rollback criteria:

- If decommission approval is absent, old runtime remains in grace period.
