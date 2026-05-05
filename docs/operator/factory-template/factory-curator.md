# Factory curator / куратор фабрики

`template-repo/scripts/factory-curator.py` is a Hermes-like curator layer, but it is repo-reviewed and read-only by default.

## Policy / политика

- no hidden self-learning;
- all learning becomes a repo-reviewed artifact;
- curator scans repo control-plane artifacts and writes proposals under `reports/curator/`;
- no mutation by default;
- `--write` is reserved for a future explicit curator-class FT-TASK flow.

## Proposal shape / форма предложения

Each proposal must include evidence, proposal, risk and suggested validation. The curator may suggest a new runbook step, validator, fixture, reusable handoff template, obsolete doc/archive candidate or recurring defect pattern.
