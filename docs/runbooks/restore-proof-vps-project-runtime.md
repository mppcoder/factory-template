# Restore proof для project runtime на VPS

## Цель

Backup is not proof by itself. This checklist proves that a project runtime can be restored after a failed deploy, host loss or rollback event for both `single-host` and `split-host` topologies.

## Набор pre-deploy backup

Before each production runtime change, capture:

- `/srv/<project>-prod`;
- `/etc/<project>.env`;
- `/etc/systemd/system/<project>.service`;
- `/etc/nginx/sites-available/<project>.conf`;
- `/etc/nginx/sites-enabled/<project>.conf` target if symlinked;
- `/srv/<project>-prod/compose.yaml`;
- project runtime inventory;
- DB dump or data volume backup if applicable.

Store backups under:

```text
/var/backups/projects/<project>/<timestamp>/
```

Do not commit backup contents.

## Цель restore

Use one of:

- disposable runtime VPS;
- staging runtime VPS;
- approved recovery directory on the runtime host;
- for `split-host`, the actual project runtime VPS only when the operator explicitly approves destructive restore.

## Последовательность restore

1. Stop the candidate/new service:

   ```bash
   sudo systemctl stop <project>.service
   ```

2. Restore runtime dir:

   ```bash
   sudo tar -C /srv -xzf /var/backups/projects/<project>/<timestamp>/runtime.tgz
   ```

3. Restore env with secure permissions:

   ```bash
   sudo install -m 0600 /var/backups/projects/<project>/<timestamp>/env.backup /etc/<project>.env
   ```

4. Restore systemd service:

   ```bash
   sudo cp /var/backups/projects/<project>/<timestamp>/systemd.service /etc/systemd/system/<project>.service
   sudo systemctl daemon-reload
   ```

5. Restore nginx config:

   ```bash
   sudo cp /var/backups/projects/<project>/<timestamp>/nginx.conf /etc/nginx/sites-available/<project>.conf
   sudo ln -sfn /etc/nginx/sites-available/<project>.conf /etc/nginx/sites-enabled/<project>.conf
   sudo nginx -t
   sudo systemctl reload nginx
   ```

6. Restore DB/data if applicable with the application-specific restore command.

7. Start service:

   ```bash
   sudo systemctl start <project>.service
   sudo systemctl status <project>.service --no-pager
   ```

8. Run healthchecks:

   ```bash
   curl -fsS http://127.0.0.1:<internal-port>/<health-path>
   curl -fsS https://<domain>/<health-path>
   ```

## Rollback через Git tag или image tag

Rollback proof must record:

- previous Git tag or image tag;
- candidate Git tag or image tag;
- command used to restore the previous tag;
- healthcheck result after rollback;
- whether DB/data rollback was needed.

If DB schema migration is involved:

- create a fresh DB dump before migration;
- document application-specific migration rollback;
- do not claim rollback proof until data restore or migration rollback has been tested.

## Restore proof для `split-host`

For `split-host`:

- execute restore proof on the runtime VPS or approved staging runtime VPS;
- validate runtime host Docker/nginx/systemd parity;
- prove healthcheck through the final domain or staging domain;
- ensure backups are on the runtime VPS or an approved external backup location, not only on the old VPS.

## Acceptance gate приемки

Restore proof passes only when:

- runtime dir restored;
- env restored with `600` permissions;
- systemd service restored and starts;
- nginx config passes `nginx -t`;
- compose config passes;
- DB/data restored if applicable;
- local healthcheck passes;
- public/staging route healthcheck passes;
- sanitized transcript exists.

## Stop rules выполнения

- Do not delete old VPS before restore proof and rollback proof pass.
- Do not run destructive restore on production without operator approval.
- Do not paste env values into repo, reports or chat.
- Do not commit raw backup files.
