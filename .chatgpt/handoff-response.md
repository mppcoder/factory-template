## Handoff в Codex

```text
Repo: factory-template
Цель: усилить process rules для completion/handoff layer и validator contour.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции, если нет конфликта.
Scope: обновить handoff/validator/docs слой без размывания release semantics.
Verify: использовать существующие repo validators, smoke/matrix checks и semantic pack validation.
```

## Инструкция пользователю
1. Цель
Понять, что handoff layer и validators уже синхронизированы.
2. Где сделать
В текущем repo `factory-template`.
3. Точные шаги
При необходимости посмотреть `README.md`, `CURRENT_FUNCTIONAL_STATE.md` и `TEST_REPORT.md`.
4. Ожидаемый результат
Repo отражает актуальные handoff rules и соответствующие verify checks.
5. Что прислать обратно
Ничего, если дополнительный follow-up не нужен.
