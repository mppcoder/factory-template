# Аудит repo-состояния brownfield: OpenClaw+

Дата: 2026-04-26

## Вывод

Оба входных корня являются brownfield filesystem roots без git metadata:
- `/root/.openclaw`
- `/root/openclaw-plus`

Это подтверждает профиль `brownfield-without-repo`.

## Git-состояние

Команды:

```bash
git -C /root/.openclaw rev-parse --show-toplevel
git -C /root/openclaw-plus rev-parse --show-toplevel
```

Результат для обоих корней:

```text
fatal: not a git repository (or any of the parent directories): .git
```

## Критичные файлы и структуры

Runtime:
- `/root/.openclaw/openclaw.json`
- `/root/.openclaw/agents/`
- `/root/.openclaw/hooks/`
- `/root/.openclaw/flows/registry.sqlite`
- `/root/.openclaw/tasks/runs.sqlite`
- `/root/.openclaw/credentials/`
- `/root/.openclaw/identity/`
- `/root/.openclaw/telegram/`

Package / overlay:
- `/root/openclaw-plus/ARCHITECTURE.md`
- `/root/openclaw-plus/KNOWN-BUGS.md`
- `/root/openclaw-plus/RUNBOOK-FULL.md`
- `/root/openclaw-plus/infra/systemd/*.service`
- `/root/openclaw-plus/validators/run-final-acceptance.sh`
- `/root/openclaw-plus/models/*.yaml`
- `/root/openclaw-plus/policies/*.yaml`
- `/root/openclaw-plus/facade/*.yaml`
- `/root/openclaw-plus/retrieval/`
- `/root/openclaw-plus/telemetry/`
- `/root/openclaw-plus/wrappers/delegate-specialist-plugin/`

## Расхождения repo/documentation

Найденные признаки:
- `ARCHITECTURE.md` утверждает invariant: live runtime exists only in `~/.openclaw`; это совпадает с фактом.
- `ARCHITECTURE.md` утверждает package tree is overlay only; `/root/openclaw-plus` действительно содержит package/overlay артефакты и systemd/templates/scripts.
- `README.md` фактически почти пустой и не достаточен как source-of-truth для восстановления.
- `KNOWN-BUGS.md` содержит подробную историю ручных фиксов установки и должен считаться важным evidence-source.
- В package root есть тяжелые generated/dependency зоны `.venvs/` и `wrappers/.../node_modules`, поэтому реконструкция source pack должна исключать generated artifacts.

## Backup- и drift-индикаторы

В runtime и package присутствуют множественные backup-файлы:
- `/root/.openclaw/openclaw.json.bak*`
- `/root/.openclaw/hooks/pre-execution/*.bak*`
- `/root/openclaw-plus/accounts/*.bak*`
- `/root/openclaw-plus/scripts/*.bak*`
- `/root/openclaw-plus/telemetry/*.bak*`
- `/root/openclaw-plus/wrappers/delegate-specialist-plugin/index.js.bak*`

Вывод: перед remediation нужна отдельная реконструкция change history и решение, какие backup-файлы являются evidence, а какие мусорным generated state.

## Граница реконструкции repo

Безопасный следующий шаг не в создании git repo прямо в `/root` и не во временных repo рядом в `/projects`.

Согласно brownfield scenario rule, reconstructed/intermediate repo должен создаваться только внутри выделенного project root, например:
- `/projects/openclaw-brownfield/reconstruction/`

На текущем этапе такой repo не создавался.
