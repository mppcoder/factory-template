# Отчет готовности первого проекта

Date: 2026-05-07
Work item: FT-CX-0020 beginner-first-hardening

## Результат

Status: ready, with one remaining external UI boundary.

Codex created and verified the first greenfield rehearsal project through the factory path.

## Проект

- Project name: `Beginner First Rehearsal E`
- Project slug: `beginner-first-rehearsal-20260507e`
- Project profile: `greenfield-product`
- Project mode: `greenfield`
- VPS project root: `/projects/beginner-first-rehearsal-20260507e`
- GitHub repo: `https://github.com/mppcoder/beginner-first-rehearsal-20260507e`
- Visibility: `private`
- Default branch: `main`

## Что создал Codex

- GitHub repo and `origin`.
- VPS project root.
- Generated repo-first scaffold.
- `.chatgpt` lifecycle artifacts.
- `AGENTS.md`.
- `template-repo/scenario-pack`.
- `project-knowledge`.
- First feature workspace: `work/features/first-feature`.
- Verification and done evidence.
- Verified sync.

## Проверка

- Generated project quick verify: `bash scripts/verify-all.sh quick` passed.
- Generated DoD: `python3 scripts/check-dod.py .` passed.
- Generated handoff validator: `python3 scripts/validate-handoff.py .` passed.
- Verified sync status: `no-op` after final cleanup.
- Latest pushed commit: `68cd156`.

## Примечания

The rehearsal found and fixed reusable template defects before the final green project:

- missing git identity on clean VPS;
- generated-root `work-templates` lookup;
- generated task-pack support artifacts;
- missing plan-mode reasoning default;
- smoke helper handoff-response drift;
- generated `.gitignore` / pycache hygiene.

Earlier rehearsal repos with suffixes `20260507`, `20260507b`, `20260507c`, and `20260507d` are retained as failure evidence because current `gh` auth lacks `delete_repo` scope.

## Оставшееся UI-действие пользователя

The first project is repo-ready. The only remaining user action is external ChatGPT UI setup:

1. Create the battle ChatGPT Project.
2. Open Project settings/instructions.
3. Paste the prepared repo-first instruction for `https://github.com/mppcoder/beginner-first-rehearsal-20260507e`.
4. Save settings.
