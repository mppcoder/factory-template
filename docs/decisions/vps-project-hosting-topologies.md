# ADR: топологии размещения проектов на VPS

Status: accepted for template implementation.
Date: 2026-05-06.

## Контекст

`factory-template` already contains a safe single-VPS deploy proof for the template runtime reference app. The missing layer was a multi-project hosting standard that separates development workspaces from production runtime and supports both all-on-one and split runtime host models.

Without this standard, operators could mix `/projects` and `/srv`, run production directly from development worktrees, commit real env files, share compose/network/service names between projects or delete an old VPS before rollback/restore proof.

## Решение

Adopt two supported topology modes:

- `single-host`: one big VPS hosts `/projects/*` development workspaces and `/srv/*-prod` runtime copies, with hard separation.
- `split-host`: one big Dev VPS hosts `/projects/*` and deploy control; each project runtime lives on a separate runtime VPS under `/srv/<project>-prod`.

GitHub remains source of truth for code, templates and scripts. Real runtime env lives outside repo, normally in `/etc/<project>.env`, and backups live under `/var/backups/projects/<project>`.

Production must not run directly from `/projects`.

## Последствия

- New architecture and runbook docs define topology selection, migration flow, security boundary and recovery gates.
- New deploy templates provide per-project compose, systemd, nginx, env example and runtime inventory.
- New scripts provide dry-run-first deploy, backup and restore templates.
- New validators check layout, runtime, secrets boundary and network exposure.
- Host-dependent validators remain safe for generic repo verify through fixture/dry-run mode.

## Откат

If this standard conflicts with future accepted architecture, revert the docs/templates/scripts/validators together. Do not partially keep deploy scripts without the secret-boundary validators and runbooks.
