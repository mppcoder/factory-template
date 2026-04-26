# BUG-036: FP-02 был отмечен passed до создания repo проекта

Дата: 2026-04-26

## Кратко

В сценарии `brownfield-without-repo` был выполнен аудит и source-candidate mapping, но FP-02 был закрыт как `passed` до фактического создания локального project repo.

## Симптом

Пользователь справедливо указал, что brownfield без repo подразумевает не только аудит, но и создание repo проекта, если нет явного blocker.

## Evidence

- `/root/.openclaw` и `/root/openclaw-plus` не являлись git repo.
- До remediation существовали audit/reconstruction notes, но не было repo boundary для проекта.
- `reports/release/field-pilot-scenarios/02-brownfield-without-repo.md` содержал формулировку про `create reconstruction workspace`, но field status уже был `passed`.

## Impact

- FP-02 evidence мог переоценивать результат field run.
- Следующий оператор получил бы план создания repo вместо созданного repo.
- Roadmap field pilot терял различие между `audit complete` и `repo created`.

## Classification

- Defect layer: field pilot closeout / evidence criteria.
- Reusable issue: yes.
- Severity: high для field evidence integrity.

## Remediation

- Создан локальный project repo `/projects/openclaw-brownfield`.
- В repo перенесен sanitized source layer в `src/openclaw-plus`.
- Raw `/root/.openclaw` и raw `/etc/openclaw-plus.env` не переносились.
- Создан redacted env inventory в `runtime-evidence/openclaw-plus-env.inventory.md`.
- Создан commit проекта `4a58c8d`.
- FP-02 release evidence обновлен с actual repo path и commit.

## Verification

- `python scripts/validate-brownfield-transition.py .` в `/projects/openclaw-brownfield`: passed.
- `python scripts/validate-evidence.py .` в `/projects/openclaw-brownfield`: passed.
- `python scripts/validate-codex-task-pack.py .` в `/projects/openclaw-brownfield`: passed.
- `git -C /projects/openclaw-brownfield status --short --branch`: clean on `main`.

## Status

Fixed in current scope.

