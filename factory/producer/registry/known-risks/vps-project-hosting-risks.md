# Known risks: топологии размещения проектов на VPS

Status: active.
Date: 2026-05-06.

## Риски

| ID | Risk | Mitigation |
| --- | --- | --- |
| VPS-HOST-01 | `single-host` increases blast radius: one VPS failure can affect dev and multiple runtimes. | Record accepted blast radius, keep backups, restore proof and old VPS grace period. |
| VPS-HOST-02 | `split-host` increases operational complexity and SSH/deploy inventory drift. | Keep sanitized runtime inventory and validate runtime host before deploy. |
| VPS-HOST-03 | Production accidentally runs from `/projects`. | Require `/projects` vs `/srv` validators and systemd `WorkingDirectory=/srv/<project>-prod`. |
| VPS-HOST-04 | Real `.env` is accidentally committed. | Keep real env at `/etc/<project>.env`, run secret-boundary validator, commit only examples. |
| VPS-HOST-05 | Nginx is bypassed by direct container port exposure. | Bind app to `127.0.0.1`, validate compose/network exposure, expose only nginx publicly. |
| VPS-HOST-06 | Compose project/network collision between projects. | Require `COMPOSE_PROJECT_NAME` and `DOCKER_NETWORK` per project. |
| VPS-HOST-07 | Backup exists but restore is not tested. | Require restore proof before cutover/decommission. |
| VPS-HOST-08 | Old VPS is deleted too early. | Prohibit deletion before healthcheck, backup, restore proof, rollback proof and operator approval. |
| VPS-HOST-09 | Runtime VPS lacks Docker/nginx/systemd parity. | Run runtime validator on the runtime VPS or fixture-equivalent preflight. |
| VPS-HOST-10 | Healthcheck only passes locally, not through the public route. | Require final domain healthcheck before cutover. |
| VPS-HOST-11 | GitHub tag/image tag rollback is not aligned. | Record previous Git/image tag before deploy and prove rollback. |
| VPS-HOST-12 | Host-dependent validators break generic CI. | Keep real host checks opt-in or fixture-backed in quick verify. |
| VPS-HOST-13 | Raw deploy reports leak secrets. | Write sanitized reports only and never echo env contents. |
