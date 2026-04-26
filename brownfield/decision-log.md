# Журнал решений brownfield: OpenClaw+

Дата: 2026-04-26

## DEC-001: выбрать профиль `brownfield-without-repo`

Статус: accepted

Причина:
- оба входных корня существуют;
- оба входных корня не являются git repo;
- задача описывает existing configured distribution + thin custom overlay.

## DEC-002: выбрать сценарий `brownfield/00-brownfield-entry.md`

Статус: accepted

Причина:
- нужно сначала описать фактическое состояние;
- изменения/remediation запрещены до evidence и gap capture.

## DEC-003: executable-маршрут `deep`

Статус: accepted

Причина:
- brownfield without repo + два filesystem roots + реконструкция source boundary требуют deep route.
- self-handoff записан в `.chatgpt/task-launch.yaml` и `.chatgpt/direct-task-self-handoff.md`.

## DEC-004: не создавать repo в `/root` и не создавать temporary repo рядом в `/projects`

Статус: accepted

Причина:
- scenario-pack требует для brownfield without repo держать temporary/intermediate repo внутри выделенного project root.
- текущий этап только intake/evidence.

## DEC-005: не раскрывать значения секретов

Статус: accepted

Причина:
- `/etc/openclaw-plus.env`, `/root/.openclaw/credentials`, `/root/.openclaw/identity` и `/root/.openclaw/telegram` являются secret/state-bearing.
- в repo-артефакты переносится только структура и имена env keys с redaction.
