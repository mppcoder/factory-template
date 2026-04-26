# Журнал изменений шаблона

## [Unreleased]

## [2.5.0] - 2026-04-26
### Добавлено
- canonical `codex-model-routing.yaml` для model availability policy and selected profile/model/reasoning mapping
- `scripts/check-codex-model-catalog.py` и reusable catalog helper для live checks через `codex debug models`, proposal generation и fixture-based validation
- `scripts/validate-25-ga-kpi-evidence.py` для проверки GA KPI evidence перед `ga_ready: true`

### Изменено
- completion/handoff routing layer теперь выдает явный `Launch в Codex` boundary с launcher command вместо неявного ожидания, что новый чат сам переключит route
- source-facing routing docs и generated `.chatgpt` guidance теперь везде различают advisory handoff text и executable profile switch
- resolver/bootstrap/launcher/validators теперь читают canonical model routing, сохраняют plan-mode reasoning и фиксируют catalog status в normalized handoffs
- template docs, launcher metadata и generated versioning strings синхронизированы с релизом `2.5.0`

### Исправлено
- устранен defect completion/handoff layer: handoff package больше не подменяет новый task launch понятием "новый чат"
- добавлены troubleshooting и validators против sticky last-used profile/reasoning state и неподтвержденных model mappings
- live catalog unavailable mode теперь деградирует в warning без automatic mapping promotion; strict mode остается opt-in
- зафиксирован и исправлен `bug-031`: closeout guidance и validators теперь запрещают типовые англоязычные человекочитаемые headings в финальном closeout
- зафиксирован и исправлен `bug-032`: `.chatgpt/codex-input.md` и normalized handoff теперь проходят language-contract validation для upstream ChatGPT handoff
- исправлен `bug-033`: active source-facing человекочитаемый слой очищен от английских headings, documented archival exceptions закреплены отдельным policy artifact, language validator подключен к quick verify
- закрыт GA evidence gap для `G25-GA`: novice timing, controlled pilot, safe-sync report и handoff loop register стали проверяемыми артефактами

## [2.4.4] - 2026-04-22
### Добавлено
- canonical preset alias map для совместимости со старыми preset names
- нейтральный workspace bootstrap pack и optional domain reference contour в release-facing guidance

### Изменено
- template docs, launcher metadata и generated versioning strings синхронизированы с patch-релизом `2.4.4`
- canonical presets переведены на универсальные factory names без product-specific naming в core слое

### Исправлено
- устранён gap, при котором downstream guidance продолжала выдавать legacy preset/workspace names как canonical
- cleanup path теперь убирает `.factory-runtime`, чтобы generated release prep не наследовал stale runtime reports
- verified-sync/release automation больше не ломается на non-ASCII git paths из-за quoted porcelain output

## [2.4.3] - 2026-04-22
### Добавлено
- root-level `RELEASE_NOTES.md` в factory root включен в канонический release-facing пакет и release/export layer
- полный reference-doc по архитектуре, дереву проекта и workflow для `factory-template`

### Изменено
- template docs и release metadata синхронизированы с patch-релизом `2.4.3`
- generated release-facing guidance теперь ожидает root `RELEASE_NOTES.md` как notes source в factory repo

### Исправлено
- устранён gap между release bundle, published notes source и обзорной release documentation

## [2.4.2] - 2026-04-20
### Добавлено
- reusable scripts `verified-sync` и `execute-release-decision` для generated project automation
- templates для `release-decision`, `sync-report` и `release-report`
- lightweight follow-up mode для low-risk post-verify docs/ignore cleanup
- internal-followup precedence rule для handoff/boundary layers generated project
- completion package и impact model для repo-first instruction layers generated project
- immediate completion-package rule для generated closeout/handoff behavior
- generated boundary guidance больше не должна перекладывать internal prepare/export commands на пользователя
- executable routing layer для каждой новой Codex-задачи: `codex-routing.yaml`, named profiles и launcher/router scripts
- direct-task self-handoff standard с `.chatgpt/task-launch.yaml`, `.chatgpt/normalized-codex-handoff.md`, `.chatgpt/direct-task-self-handoff.md` и `.chatgpt/direct-task-response.md`
- root-level visual/workflow reference doc для архитектуры шаблона и основных deployment/update событий

### Изменено
- template/runtime/policy layer теперь закрепляет обязательный inline Codex handoff, если handoff уже допустим и задача достаточно определена
- template guidance теперь требует финальный блок `Инструкция пользователю` при любом pending user/external step
- generated projects теперь могут отделять verified sync от release publication
- generated docs, `.chatgpt` artifacts и validators теперь различают advisory layer и executable routing layer
- generated direct-task contour теперь требует отдельный visible response artifact до remediation и проверяется routing validator-ом

### Исправлено
- устранен reusable process gap между router, handoff rules, runbook, AGENTS и closeout layer
- устранен template defect: routing по типу задачи больше не сводится к одному static profile без launch-time фиксации
- устранен template process gap, при котором direct task мог не показывать self-handoff явно в первом substantive ответе

## [2.4.1] - 2026-04-20
### Изменено
- template layer синхронизирован с repo-first режимом для ChatGPT Projects
- generated guidance теперь требует сначала читать GitHub repo и `00-master-router.md`

## [2.4.0] - 2026-04-16
### Изменено
- launcher и generated versioning layer переведены на финальную версию фабрики `2.4.0`
- generated project origin и changelog больше не несут `rc2` как текущую фабричную версию

## [2.4.0-rc2] - 2026-04-15
### Добавлено
- единый release-alignment/versioning layer для generated projects
- автоматическая генерация `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`
- валидатор versioning layer

### Изменено
- `project-origin.md` и launcher синхронизированы с актуальной версией фабрики
