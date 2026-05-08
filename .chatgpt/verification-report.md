# Отчёт о проверке результата

## Что проверяли

- Goal-first contract schema/template/current state.
- Positive and negative goal-contract fixtures.
- Codex routing, route explanation and beginner handoff UX.
- Mode parity, tree contract and human-language layer.
- Full quick verification suite.

## Что подтверждено

- `codex --version`: `codex-cli 0.129.0`.
- `codex features list`: `goals` найден как `experimental false`; используется как рабочий candidate только по явному указанию пользователя.
- `python3 template-repo/scripts/validate-goal-contract.py template-repo/template/.chatgpt/goal-contract.yaml.template --template`: PASS.
- `python3 template-repo/scripts/validate-goal-contract.py .chatgpt/goal-contract.yaml`: PASS.
- `tests/goal-contract/valid/*.yaml`: PASS.
- `tests/goal-contract/negative/*.yaml`: rejected as expected.
- `python3 template-repo/scripts/validate-codex-routing.py .`: PASS.
- `python3 template-repo/scripts/validate-route-explain.py .`: PASS.
- `python3 template-repo/scripts/validate-beginner-handoff-ux.py` on positive fixtures: PASS.
- `python3 template-repo/scripts/validate-mode-parity.py .`: PASS.
- `python3 template-repo/scripts/validate-tree-contract.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick`: PASS.

## Evidence относительно DoD

- Router has goal-first normalization gate.
- Handoff scenario requires `goal_contract`, runtime recommendation and live validation boundary.
- Closeout scenario requires `goal_status` and evidence vs DoD.
- Validators reject missing DoD, proxy-only evidence, enabled goal runtime without live validation and budget-limited closeout without summary.

## Guard от proxy signals

- Goal achieved is based on evidence vs DoD and full validator results, not tests/file/commit/dashboard alone.

## Что не подтверждено или требует повторной проверки

- Codex runtime `/goal` was not switched inside this already-open session; only CLI capability/feature flag was live-checked.
- `goals` remains experimental/off by default in `codex-cli 0.129.0`.

## Итоговый вывод

- Goal-first transition verification passed.
