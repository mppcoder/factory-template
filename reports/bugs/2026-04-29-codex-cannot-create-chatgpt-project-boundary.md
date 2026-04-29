# Отчет о дефекте: граница ChatGPT Project боевого проекта

Дата: 2026-04-29
Статус: исправлено в текущем remediation
Слой: `docs/operator/runbook-packages/02-greenfield-product`

## Краткое описание

Greenfield runbook нуждался в более строгой boundary-формулировке: Codex нельзя считать исполнителем, который создает ChatGPT Project боевого проекта или вставляет/сохраняет repo-first instructions в ChatGPT UI.

## Влияние

Без явной границы beginner path мог подразумевать ненадежную desktop/browser UI automation как canonical route. Это смешивает external-action ledger: Codex может создать repo/root/core/verify/sync и подготовить текст instruction, но пользователь должен создать ChatGPT Project в ChatGPT UI, вставить подготовленную instruction и сохранить настройки.

## Ожидаемое поведение

- Codex создает GitHub repo, нормализует slug/repo name, готовит VPS project root, запускает launcher/wizard, materializes repo-first core, запускает bootstrap/verify, выполняет initial commit/push/verified sync, готовит текст repo-first instruction и инструкцию по вставке.
- Пользователь создает ChatGPT Project боевого проекта в ChatGPT UI, открывает Project settings/instructions, вставляет подготовленную repo-first instruction и сохраняет настройки.
- Canonical beginner docs не опираются на browser/desktop UI automation для создания ChatGPT Project или редактирования instructions.

## Исправление

- Добавлена явная boundary-формулировка в package contract и greenfield package files.
- Добавлена validator coverage, которая падает на claims, что Codex создает ChatGPT Project или вставляет/сохраняет ChatGPT Project instructions.
- Добавлены dashboard fields для ChatGPT Project UI ownership и instruction-preparation ownership.

## Проверка

Run:

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
bash template-repo/scripts/verify-all.sh quick
```
