# Codex workflow для этого проекта

## Контракт routing
- advisory layer: `AGENTS`, scenario-pack, runbooks, ChatGPT Project instructions;
- executable layer: `codex-routing.yaml`, `.codex/config.toml` named profiles и `./scripts/launch-codex-task.sh`;
- надежная единица маршрутизации: новый task launch.
- `goal first` является pre-routing normalization layer: сначала `goal_contract`, затем обычный scenario route;
- `goal first` не меняет selected_profile/model/reasoning сам по себе.

## Flow постановки цели

Любая новая задача должна иметь минимальный `goal_contract`: `normalized_goal`, DoD, evidence, scope/non-goals, safety/budget boundaries и proxy-signal denylist.

`goal`, `goal:`, `/goal`, `цель`, `цель:` в ChatGPT Project означают intent на goal-first flow, а не гарантию Codex CLI slash command.

`Codex /goal runtime` optional and live-gated. Для текущего CLI проверяйте:

```bash
codex --version
codex features list
```

Если `goals` виден как experimental/off by default, использовать его как рабочий runtime можно только по явному выбору пользователя/operator. Уже открытая live session не является надежным auto-switch boundary.

Не закрывайте цель по proxy signals alone: tests passed, file exists, commit exists, green dashboard или validator passed сами по себе не доказывают goal achieved.

## Именованные profiles
- `quick`: docs / triage / search
- `build`: feature / fix / implementation
- `deep`: root-cause / audit / architecture
- `review`: review / tests / cleanup

## Как запускать
- не проверяйте routing в старой уже открытой сессии Codex;
- для интерактивной работы через VS Code Codex extension используйте `manual-ui (default)`: откройте новый чат/окно Codex, вручную выставьте `selected_model` и `selected_reasoning_effort` в picker, затем вставьте handoff;
- `selected_profile` фиксирует intended route для repo; `selected_model` и `selected_reasoning_effort` описывают ожидаемую конфигурацию этого profile, но не auto-switch в уже открытой live session;
- `launcher-first strict mode` через `./scripts/launch-codex-task.sh --launch-source <chatgpt-handoff|direct-task> ...` нужен для automation, reproducibility, shell-first и scripted launch;
- `новый чат + вставка handoff` и `new task launch через executable launcher` — не одно и то же;
- для direct task launcher сначала создает `.chatgpt/direct-task-self-handoff.md` и `.chatgpt/direct-task-response.md`, а затем фиксирует route в `.chatgpt/task-launch.yaml`;
- первый substantive ответ Codex по direct task должен явно показать self-handoff block до remediation.
- если после manual UI apply или strict launch виден sticky last-used state, завершите текущую сессию, откройте новую и при необходимости выполните launcher еще раз, а затем сверьте model с `codex debug models`.
- для long goal loops задайте observation cadence, time/token/iteration budget и stop criteria; при quota/tool wall фиксируйте `budget_limited` или `tool_limited`, а не `achieved`.

## VPS Remote SSH-first orchestration по умолчанию

Default path для большой задачи: `VPS Remote SSH-first`.

Для full orchestration handoff default UX — one-paste autopilot: пользователь вставляет parent handoff один раз, а parent Codex сам запускает repo-native orchestrator после validation gate. `orchestrate-codex-handoff.py --execute` является parent Codex execution path; ручной shell-запуск оператора остается troubleshooting / strict fallback.

1. Browser ChatGPT Project выдает один большой handoff.
2. VS Code Remote SSH открывает repo на VPS.
3. Codex extension в этом Remote SSH окне получает handoff.
4. Repo-native orchestrator раскладывает работу на child subtasks.
5. Codex CLI sessions запускаются на VPS/repo context отдельно для каждого `selected_profile`.
6. Parent orchestration report собирает results, blockers и closeout.

`Codex App / Cloud Director` допустим как optional, not default. Codex App local/remote repo context допустим только если работает с тем же repo filesystem and shell context. Cloud delegation допустим только по явному выбору пользователя и при разрешенной repo/security boundary.

Already-open live session не является reliable auto-switch boundary. Child subtask не наследует parent route by default: каждый child handoff должен явно фиксировать `task_class`, `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort` и `selected_scenario`.

Для большого handoff действует правило `user_actions_policy: defer-to-final-closeout`: все действия пользователя, ввод реальных external values, runtime approvals и downstream/battle inputs переносятся в конец parent plan как `deferred_user_actions`. Если internal work можно продолжить без них, orchestrator использует temporary placeholders и фиксирует `placeholder_replacements`, чтобы финальный closeout напомнил заменить placeholders на реальные данные и повторить нужные checks.

Dry-run orchestration command:

```bash
python3 template-repo/scripts/orchestrate-codex-handoff.py --plan tests/codex-orchestration/fixtures/valid/parent-plan.yaml --report reports/orchestration/parent-orchestration-report.md
```

Execute orchestration command, normally run by parent Codex after paste:

```bash
python3 template-repo/scripts/orchestrate-codex-handoff.py --plan <parent-orchestration-plan.yaml> --report reports/orchestration/parent-orchestration-report.md --execute
```

Validator:

```bash
python3 template-repo/scripts/validate-codex-orchestration.py .
```

## Model availability auto-check / авто-проверка доступности моделей

Repo-configured mapping живет в `codex-model-routing.yaml`: `task_class_routing` выбирает profile, `profile_routes` выбирает model/reasoning/plan-mode reasoning. Live Codex catalog не является тем же самым: его нужно проверять командой `python3 scripts/check-codex-model-catalog.py .`, которая вызывает `codex debug models`, когда CLI доступен.

`--write-proposal` создает `reports/model-routing/model-routing-proposal.md` с текущим mapping, сводкой live catalog, предложенным mapping, evidence поддержки reasoning, рисками и точными файлами для обновления. `--apply-safe` может обновить только snapshot-поля catalog; promotion новых моделей в profile mapping требует ручного review.

Model proposal также обязан обновлять prompt policy contour. `prompt_migration_policy` требует official OpenAI source map, fresh prompt baseline, проверку reasoning/verbosity/tool-use guidance, обновление `reports/prompt-migration/`, prompt contract validator и Artifact Eval spec. Новая model не считается drop-in replacement: сначала проверьте prompt-like artifacts, затем меняйте profile mapping.

Диагностика:
- новый model есть в live catalog, но отсутствует в routing: сначала создайте proposal, затем осознанно обновите `codex-model-routing.yaml` и named profiles в `.codex/config.toml`;
- новый model имеет новые official OpenAI prompt recommendations: сначала обновите prompt migration report, validators/evals и handoff/task-pack contract;
- configured model исчез: handoff должен сказать, что `selected_model` repo-configured и требует live validation; strict validator может упасть;
- unsupported reasoning: выберите supported reasoning или другой `selected_model` до release-facing handoff;
- sticky model в VS Code picker: откройте новый chat/window и вручную проверьте picker;
- handoff вставлен в уже открытую session: считайте это non-canonical fallback, а не executable route switching.

## Когда handoff допустим
Переключение в рабочий Codex launch допустимо только после того, как:
- собран минимальный evidence pack;
- заполнены `reality-check.md`, `evidence-register.md`, `reverse-engineering-summary.md`;
- определены safe zones и rollback plan;
- handoff в Codex больше не противоречит policy preset.

## Внешние boundary-действия
Эти действия остаются за оператором:
- создание новых GitHub repos только если connector/`gh` write path недоступен или repo owner/name не подтверждены; в greenfield handoff при доступном write path repo/root/origin/first push выполняет Codex;
- подключение репозиториев и app sources в ChatGPT Projects;
- загрузка архивов в `/projects/<project-root>/_incoming/`;
- ввод секретов и работа с внешними UI.

## Intake с решениями по умолчанию

Для beginner intake используйте recommendation-first flow:

1. После `новый проект` выбрать `default_decision_mode`: `global-defaults`, `confirm-each-default` или `manual`.
2. Для каждого safe decision показать recommended default, basis и override path.
3. В generated handoff записать `accepted_defaults`, `overridden_defaults`, `default_source_basis`, `uncertainty_notes` и `decisions_requiring_user_confirmation`.
4. Risky, paid, destructive, security, privacy, legal и secret-related decisions требуют explicit confirmation и не автопринимаются.

## Canonical VPS layout / каноническая VPS layout
- `/projects` содержит только project roots;
- `_incoming` допускается только как подпапка проекта: `/projects/<project-root>/_incoming/`;
- brownfield temporary, intermediate, reconstructed и helper repos должны жить внутри repo целевого `greenfield-product`;
- такие промежуточные repo нельзя раскладывать плоско рядом в `/projects`.
