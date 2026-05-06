# Checklist pilot migration проекта на VPS

Use this checklist for the first project migrated into the VPS project hosting topology standard. Keep evidence sanitized.

| Step | Done | Expected evidence | Secret boundary |
| --- | --- | --- | --- |
| Choose pilot project | [ ] | `PROJECT_SLUG`, GitHub repo URL, owner/operator recorded | No secrets |
| Choose topology mode | [ ] | `single-host` or `split-host` plus reason | No secrets |
| Record old VPS inventory | [ ] | OS, Docker/Compose, nginx, systemd, paths, ports, domains, backup paths, DB/data volumes, health endpoints | Env values redacted |
| Verify GitHub status | [ ] | `git status --short --branch`, remote, last tag/commit | No tokens |
| Prepare `/projects` workspace | [ ] | `/projects/<project>` exists, clean branch, tests/build command known | No prod env in repo |
| Prepare runtime target | [ ] | `single-host`: `/srv/<project>-prod`; `split-host`: runtime VPS `/srv/<project>-prod` | Runtime host metadata only |
| Create real env | [ ] | `/etc/<project>.env`, owner/mode recorded, `chmod 600` | Values never printed |
| Render compose/systemd/nginx | [ ] | Rendered paths and placeholders replaced | No secrets in rendered repo artifacts |
| Run layout validator | [ ] | `validate-vps-hosting-layout.sh` result | No secrets |
| Run runtime validator | [ ] | `validate-project-runtime.sh` result | No env values |
| Run secret boundary validator | [ ] | `validate-project-secrets-boundary.sh` result | No raw `.env` |
| Run network exposure validator | [ ] | `validate-project-network-exposure.sh` result | No secrets |
| Dry-run deploy | [ ] | deploy script dry-run output, sanitized report | No env echo |
| Backup runtime/config | [ ] | Backup path under `/var/backups/projects/<project>` and timestamp | Backup contents outside repo |
| Approved deploy | [ ] | systemd status, docker compose ps summary, nginx reload result | No env values |
| Local healthcheck | [ ] | `curl http://127.0.0.1:<port><path>` pass | No secrets |
| Public healthcheck | [ ] | `https://<domain><path>` pass | No private connection strings |
| Restore proof | [ ] | Restore to disposable/staging/recovery target passes | Raw backups outside repo |
| Rollback proof | [ ] | Previous Git/image tag redeploy passes healthcheck | No secrets |
| Grace period | [ ] | Old VPS kept online/restorable; monitoring window recorded | No secrets |
| Cutover decision | [ ] | Operator approval recorded | Approval only, no secret values |
| Decommission decision | [ ] | Final backup retained, DNS/firewall cleanup approved | Only after proof |
| Sanitized evidence transcript | [ ] | Commands, timestamps, versions, tags, pass/fail | Secrets redacted |

## Действия пользователя

- Provide real VPS hostnames/IPs when doing a real pilot.
- Choose domain/DNS.
- Create/edit `/etc/<project>.env` and enter real secrets.
- Approve production deploy/cutover.
- Approve old VPS decommission.

These actions are not required for repo implementation of this standard.
