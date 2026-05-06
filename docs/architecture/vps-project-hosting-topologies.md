# Топологии размещения проектов на VPS

## Цель

Этот стандарт задает repo-first модель размещения нескольких проектов на VPS и выбор между двумя целевыми топологиями:

- `single-host`: один большой VPS совмещает dev workspace, factory host, Codex / VS Code Remote SSH host, build/test host и runtime/prod host для нескольких проектов.
- `split-host`: большой VPS остается dev/build/deploy control plane, а runtime/prod каждого готового проекта размещается на отдельном минимальном VPS.

Default supported topology для solo/beginner operator: `single-host`, то есть один большой VPS с жестким разделением `/projects/*` для dev/Codex/build и `/srv/*-prod` для runtime/prod. Маленькие VPS остаются optional runtime-only, staging или backup targets; они не являются default heavy dev/Codex/build host.

Стандарт расширяет существующий single-VPS deploy proof из `docs/deploy-on-vps.md` и `docs/production-vps-field-pilot.md`. Он не заменяет текущие production presets для template runtime reference app и не заявляет real migration proof без approved runtime evidence.

## Карта gap

1. До этого документа не было явного стандарта выбора между all-on-one big VPS и big dev VPS plus separate runtime VPS per project.
2. Не было единого inventory/runbook процесса переноса нескольких проектов: old VPS, repo status, runtime assets, env/systemd/nginx, backup/restore, cutover, grace period и decommission.
3. Не было канонического разделения:
   - `/projects` = git repo, dev workspace, build/test, Codex/factory operations;
   - `/srv` = runtime/prod copies only;
   - `/etc/<project>.env` = real secrets;
   - `/var/backups/projects/<project>` = runtime backups;
   - GitHub = source of truth for code/templates/docs/scripts.
4. Не было project-level templates для docker compose, systemd service, nginx reverse proxy, env example, deploy script, runtime inventory и migration checklist.
5. Не было validator набора для host layout, secret leakage, nginx/systemd/docker, compose config, port exposure, backup path, health endpoint и split-host runtime target.
6. Был риск смешивания dev и prod: prod secrets in repo, runtime edits in `/projects`, build artifacts in prod, shared compose/network/env across projects, direct app exposure without nginx, old VPS deletion before rollback proof.
7. Был риск unmanaged split-host deploy: dev VPS builds successfully while runtime VPS lacks env/service/nginx, host versions drift, backups remain on old VPS, only local healthcheck passes, source of truth moves manually instead of GitHub.

## Инварианты

- GitHub is the canonical source of truth for code, docs, templates and scripts.
- Real secrets and real prod env are never committed.
- Real prod env lives outside repo, normally in `/etc/<project>.env`, with owner and permissions controlled by the operator and `chmod 600`.
- `/projects` is for development git workspaces, Codex, factory operations, builds and tests.
- `/srv` is for runtime/prod copies only.
- Production must not run directly from `/projects`.
- Every project has an isolated runtime path, env file, systemd service, nginx config, compose project name, Docker network and backup directory.
- Public HTTP/HTTPS traffic enters through nginx; app containers bind to `127.0.0.1`.
- Externally exposed ports should be only `22`, `80` and `443`.
- Backups live outside repo under `/var/backups/projects/<project>`.
- Old VPS/runtime is not deleted until healthcheck, backup, restore proof, rollback proof and operator cutover approval are recorded.

## Общая модель

GitHub stores:

- application repo history;
- factory/template source;
- deploy templates and scripts;
- sanitized docs and reports;
- release tags used for rollback.

GitHub does not store:

- real `.env` files;
- passwords, tokens, private keys or private connection strings;
- raw runtime transcripts containing sensitive values;
- backup contents.

Big Dev VPS stores:

- `/projects/factory-template`;
- `/projects/<project-a>`;
- `/projects/<project-b>`;
- VS Code Remote SSH workspace;
- Codex execution workspace;
- build/test dependencies such as `node_modules` and Python deps;
- factory operations;
- deploy control plane for `split-host`;
- optional local runtime area only for `single-host`.

Runtime area or runtime VPS stores:

- `/srv/<project>-prod`;
- `/etc/<project>.env`;
- `/etc/systemd/system/<project>.service`;
- `/etc/nginx/sites-available/<project>.conf`;
- `/etc/nginx/sites-enabled/<project>.conf`;
- `/var/backups/projects/<project>`;
- per-project docker compose project/network;
- systemd, nginx and backup contour.

## Топология A: `single-host`

The big VPS hosts both development and runtime, but with hard path separation:

- `/projects/factory-template`: factory/template repo and operator automation.
- `/projects/project-a`: dev workspace for project A.
- `/projects/project-b`: dev workspace for project B.
- `/projects/*`: development git workspaces only.
- `/srv/project-a-prod`: runtime copy for project A.
- `/srv/project-b-prod`: runtime copy for project B.
- `/srv/*-prod`: runtime copies only.
- `/etc/*.env`: real project env/secrets.
- `/etc/systemd/system/*.service`: project-specific services.
- `/etc/nginx/sites-available/*.conf`: project-specific reverse proxy configs.
- `/var/backups/projects/*`: project-specific backups.

Rules:

- Never start prod directly from `/projects`.
- Deploy copies/builds from `/projects/<project>` to `/srv/<project>-prod`.
- Use one compose project name per project, for example `<project>_prod`.
- Use one Docker network per project, for example `<project>_prod_net`.
- Use one env file per project, for example `/etc/<project>.env`.
- Use one service per project, for example `<project>.service`.
- Use one nginx config per project.
- Bind the app to `127.0.0.1:<project-port>` and publish only nginx publicly.
- Keep deploy/runtime boundaries separate: project-owned data, env files, backup sets, rollback tags and runtime transcripts are per project.
- Keep nginx/server-level shared infra separate from project runtime files.

Use `single-host` when:

- the big VPS is reliable enough for the accepted blast radius;
- there are several small projects;
- backup and operations should stay simple;
- minimal operational overhead is more important than physical host separation.

## Топология B: `split-host`

The big VPS is dev/build/deploy control plane only:

- `/projects/*`: git workspaces, build/test and factory operations.
- No prod secrets on the dev VPS unless explicitly required for deploy control and secured.
- Optional SSH deploy inventory contains host/user/path metadata, not passwords or private keys.

Each ready production project gets its own runtime VPS:

- `/srv/<project>-prod`;
- `/etc/<project>.env`;
- systemd/nginx/docker/backup contour;
- healthcheck and rollback proof executed on that runtime VPS.

Rules:

- Runtime VPS can be small and should not host heavy dev dependencies unless runtime requires them.
- Deploy flow uses a GitHub tag/artifact or controlled rsync/scp from the dev VPS.
- Runtime env, nginx and systemd files are backed up before each change.
- Host parity is validated: Docker Compose, nginx, systemd, firewall and backup path.
- Old VPS remains during grace period.

Use `split-host` when:

- the project needs lower blast radius;
- projects have different domains, customers or security boundaries;
- runtime should be cheap/minimal;
- the big VPS should be only dev/build/Codex/factory;
- there is a requirement to physically separate dev and prod hosts.

## Матрица выбора

| Criterion | Prefer `single-host` | Prefer `split-host` |
| --- | --- | --- |
| Operational overhead | Minimal overhead and one host to manage | More moving parts are acceptable |
| Blast radius | One VPS failure can affect dev and several runtimes | Runtime failure is isolated per project |
| Security boundary | Projects share one physical host | Projects need stronger host separation |
| Cost model | One bigger VPS is acceptable | Cheap minimal runtime VPS per project is preferred |
| Team flow | Operator wants one SSH workspace | Dev/build host should not be runtime host |
| Backup/restore | Centralized backups are simpler | Per-project restore boundary is clearer |
| Domains/customers | Small or internal projects | Customer/domain-specific runtime isolation |

Hybrid is allowed:

- some projects stay `single-host`;
- critical projects move to `split-host`;
- the runbook and validators must record topology per project instead of assuming one global mode.

## Операторский чеклист для `single-host`

Use this checklist before claiming that the big VPS topology is ready for a project:

- Prerequisites: Ubuntu VPS is selected, SSH access works, Docker/Compose/nginx/systemd are available or listed as blockers, and GitHub is the source of truth.
- Folder creation: create `/projects/<repo>` for each dev workspace and `/srv/<project>-prod` for each runtime copy; never run production from `/projects`.
- GitHub clone roots: clone `factory-template` to `/projects/factory-template` and each battle repo to `/projects/<project>`.
- VS Code Remote SSH: open `/projects/factory-template` for factory work and `/projects/<project>` for project work; do not use a local Codex context for remote VPS automation.
- Codex working directory: Codex starts in the relevant repo root and records `pwd`, `git status --short --branch`, selected contour and remote OS evidence.
- Deploy root: create `/srv/<project>-prod`, render compose/runtime files there and read real env from `/etc/<project>.env`.
- Nginx/systemd/docker: use unique domain, port, compose project name, Docker network, nginx config and systemd unit for every project.
- Verification commands: run `docker compose config`, `nginx -t`, `systemd-analyze verify` where available, service healthcheck and public HTTPS healthcheck when a public runtime is in scope.
- Backup/restore/rollback: create a project backup before deploy, test restore on disposable/staging target, and run rollback drill before deleting old runtime or old VPS.

## Не делать

- Не смешивать `/projects` и `/srv`.
- Не хранить secrets, real `.env`, private keys or raw transcripts in repo.
- Не складывать все проекты в один compose/network/service without a documented reason.
- Не считать dev proof production proof.
- Не считать `factory-template-placeholder-app:local` proof реального downstream продукта.
- Не открывать app container напрямую наружу, если nginx/TLS boundary required.
- Не переиспользовать systemd unit names, compose project names, ports, domains, backup paths or rollback tags between projects.

## Модель env и secrets

- Commit only `.env.example` files with placeholders.
- Store real runtime env at `/etc/<project>.env`.
- Set permissions to `chmod 600 /etc/<project>.env`.
- Do not echo env contents in deploy logs.
- Do not commit SSH private keys, deploy passwords or split-host inventory with secrets.
- Keep sanitized evidence transcripts: commands, timestamps, versions, image tags and pass/fail status are allowed; secret values are redacted.

## Модель Docker, systemd и nginx

- Compose file lives in `/srv/<project>-prod/compose.yaml` or a rendered runtime equivalent.
- Compose project name is project-specific.
- Docker network is project-specific.
- App service binds to `127.0.0.1:<PROJECT_INTERNAL_PORT>`.
- Nginx proxies public HTTP/HTTPS to `127.0.0.1:<PROJECT_INTERNAL_PORT>`.
- Systemd service points to `/srv/<project>-prod` and reads `/etc/<project>.env`.
- `docker compose config`, `systemd-analyze verify` where available and `nginx -t` are preflight gates.

## Модель backup и restore

Before each runtime change, back up:

- `/srv/<project>-prod`;
- `/etc/<project>.env`;
- `/etc/systemd/system/<project>.service`;
- `/etc/nginx/sites-available/<project>.conf`;
- runtime inventory and compose file;
- database/data volumes when applicable.

Backups live under `/var/backups/projects/<project>`. A backup is not sufficient proof until restore is tested on a disposable/staging target or a documented runtime recovery target.

## Требования безопасности

- No real `.env` in repo.
- No production runtime from `/projects`.
- No direct public app exposure unless explicitly documented as dev-only.
- Nginx is the public HTTP/HTTPS edge.
- Only `22`, `80` and `443` should be externally exposed.
- Old VPS deletion is prohibited before rollback/restore proof and operator approval.
- Host-dependent validators must have dry-run/fixture mode so generic repo verify does not require real production access.

## Не цели

- This standard does not perform a real production migration.
- It does not require every project to leave `single-host`.
- It does not replace application-specific DB migrations, data restore logic or business healthchecks.
- It does not store secrets in GitHub, task notes or sanitized transcripts.

## Этапные gate

- Entry: source repo exists or old VPS inventory is captured.
- Topology decision: `single-host` or `split-host` is recorded with reason.
- Runtime target: `/srv/<project>-prod` and `/etc/<project>.env` are prepared on the selected runtime host.
- Preflight: layout, env boundary, compose config, nginx/systemd and network exposure validators pass or record explicit blockers.
- Deploy: dry-run precedes real deploy.
- Post-deploy: local and public healthchecks pass.
- Recovery: backup, restore proof and rollback proof pass.
- Cutover: old VPS grace period is completed and operator approves decommission.

## Критерии rollback

- Docs rollback: revert this document and dependent runbooks if it contradicts accepted architecture.
- Templates rollback: remove rendered templates if placeholders or secret boundaries are unsafe.
- Scripts rollback: disable deploy scripts if dry-run or backup behavior is unsafe.
- Validators rollback: keep host-dependent checks opt-in if they break generic CI without real runtime dependencies.
