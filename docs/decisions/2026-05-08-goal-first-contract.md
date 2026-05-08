# Goal-first контракт для factory-template

Date: 2026-05-08
Status: accepted

## Решение

`goal first` becomes a mandatory repo/template governance layer for `factory-template`.
Every new task is normalized into a `goal_contract` before scenario-specific execution continues.

The goal contract captures:
- raw and normalized goal;
- measurable DoD or a validation contour that must be created first;
- evidence and evidence sources;
- scope and non-goals;
- safety, production, destructive and secrets boundaries;
- feedback/tooling readiness;
- budget and stop criteria;
- proxy-signal denylist;
- continuation policy.

## Граница runtime

`goal first` and `Codex /goal runtime` are different things.

`goal first`:
- mandatory template contract;
- works through scenario-pack, handoff, templates, docs, validators and closeout;
- does not require Codex CLI `/goal`.

`Codex /goal runtime`:
- optional runtime mode;
- live-gated by current CLI capability and operator choice;
- may be experimental/off by default;
- never auto-enabled by ChatGPT Project instructions or advisory handoff text.

On 2026-05-08 this repo observed `codex-cli 0.129.0` and `codex features list` exposed `goals` as `experimental false`.
The current task treats it as a working candidate because the user explicitly requested it, not because the already-open session switched automatically.

## Правило evidence

Do not mark a goal as achieved from proxy signals alone:
- tests passed alone;
- file exists alone;
- commit exists alone;
- green dashboard alone;
- validator passed alone.

Goal closure compares evidence to DoD.

## Pattern для broad tasks

Large migrations and architecture changes must not run as one unstructured goal.
Use `scrappy -> PRD -> clean`:
- exploratory goal;
- PRD/spec goal;
- clean implementation goal.

## Совместимость

The existing router, handoff shape and executable routing stay intact.
Goal-first normalization happens before scenario route, but does not change `task_class`, `selected_profile`, model or reasoning by itself.
