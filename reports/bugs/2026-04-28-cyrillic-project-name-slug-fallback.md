# BUG: Cyrillic-only project names collapsed to `new-project`

Date: 2026-04-28

## Summary

`first-project-wizard.py` and `factory-launcher.py` used local slug helpers that kept Cyrillic during an intermediate pass and then removed all non-Latin characters. A Cyrillic-only project name could therefore become an empty slug and silently fall back to `new-project`.

## Evidence

- A name such as `Мой первый проект!!!` should produce a deterministic technical slug.
- Existing helpers could erase Cyrillic characters after punctuation normalization.
- The fallback `new-project` is generic and ambiguous, so it is unsafe for local repo paths, GitHub repo names, registry records and project-origin metadata.

## Layer

factory-template reusable generator layer.

## Impact

- Multiple unrelated projects could be created as `./new-project`.
- GitHub repo names could become ambiguous.
- Registry and project-origin records could lose the stable technical identity of the project.

## Required Remediation

- Treat user-entered name as `project_name` only.
- Generate and validate a separate `project_slug`.
- Add Russian transliteration instead of silent fallback.
- Block empty, invalid and reserved/generic slugs unless explicitly overridden.
- Validate local path and GitHub origin naming consistency.
