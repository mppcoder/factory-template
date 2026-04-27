# Спецификация artifact eval

Используйте этот reference, когда lite QA нужно превратить в reusable deterministic report.

## Когда нужен spec

Пишите `artifact-eval/v1` spec, если проверяется один из reusable artifacts:

- scenario-pack route;
- Codex handoff block или handoff response;
- runbook;
- policy doc;
- prompt-like checklist/template;
- template skill;
- advanced execution artifact для `feature-execution-lite`.

Не требуйте spec от beginner path и маленьких разовых задач.

## Обязательные поля

```yaml
schema: artifact-eval/v1
id: short-stable-id
target_artifact: path/from/repo/root.md
artifact_type: scenario-pack
expected_trigger:
  cases: []
non_trigger_cases: []
expected_output:
  guided: "Что artifact должен улучшить"
compliance_assertions: []
thresholds:
  min_case_pass_rate: 0.8
  min_assertion_pass_rate: 0.85
  max_false_positive_rate: 0.25
```

## Категории assertions

- `process` — проверяет порядок и обязательные шаги.
- `outcome` — проверяет форму результата и evidence.
- `compliance` — проверяет boundaries, запреты и route contract.

## Deterministic checks для assertions

Каждая assertion должна иметь хотя бы один check:

- `must_contain`;
- `must_contain_any`;
- `must_not_contain`;
- `regex_contains`;
- `regex_not_contains`.

## Команды

```bash
python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/master-router.yaml --output /tmp/master-router-eval.md
python3 template-repo/scripts/validate-artifact-eval-report.py /tmp/master-router-eval.md
```

Static examples:

- `tests/artifact-eval/specs/`
- `tests/artifact-eval/reports/`
