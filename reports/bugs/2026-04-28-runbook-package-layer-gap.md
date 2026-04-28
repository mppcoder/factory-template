# Defect: отсутствует финальный слой runbook-checklist packages

Дата: 2026-04-28

## Summary

В repo есть отдельные operator runbooks для `factory-template`, brownfield transition doc, presets и validators, но нет единого финального package layer, который дает новичку и Codex пошаговый путь "с нуля до рабочего состояния" для всех четырех входов:

- `factory-template`;
- `greenfield-product`;
- `greenfield via brownfield with repo`;
- `greenfield via brownfield without repo`.

## Evidence

- `docs/operator/factory-template/*` покрывает только контур самого шаблона.
- `docs/brownfield-to-greenfield-transition.md` фиксирует conversion logic, но не является complete user/Codex/checklist/verify/closeout package.
- `docs/operator/runbook-packages/` отсутствовал как canonical package layer.
- Quick verify не проверял существование такого слоя и не ловил разрыв между runbooks, commands, validators, dashboard и brownfield conversion gates.

## Classification

- Layer: factory producer-owned docs + validators + dashboard integration.
- Reusable issue: yes.
- Severity: medium.
- Risk: onboarding/operator flows могли смешивать factory-template, generated greenfield и transitional brownfield paths, а brownfield done мог выглядеть как самостоятельный финал вместо conversion.

## Expected Behavior

Repo должен содержать проверяемые runbook-checklist packages для четырех входов, где:

- боевой финал всегда `greenfield-product`;
- brownfield пути являются только temporary entry/adoption/reconstruction paths;
- conversion или documented blocker являются обязательным done gate;
- transitional materials после conversion архивируются, переименовываются или переносятся вне active greenfield root;
- validators проверяют package existence, commands/paths, lifecycle gates, dashboard contract и handoff language/routing boundary.

## Remediation Plan

- Добавить `docs/operator/runbook-packages/` с package contract и четырьмя пакетами.
- Добавить `validate-runbook-packages.py`.
- Подключить validator к `verify-all.sh quick`.
- Обновить lifecycle dashboard contract/readout.
- Обновить release-facing docs, changelog/current state и source manifest.
