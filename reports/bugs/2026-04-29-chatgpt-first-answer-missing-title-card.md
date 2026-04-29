# Bug: ChatGPT first answer misses chat title and project card

Date: 2026-04-29

## Summary

ChatGPT project answers could follow repo-first routing but still omit two operator-critical first-answer surfaces: the copyable stable chat title and the compact project status card.

## Evidence

- The canonical Project Instructions only required reading `00-master-router.md` before answering.
- The router required route fields, but did not require a first-answer `Название чата для копирования` block.
- The compact project card was enforced for Codex closeout, not for ChatGPT first answers.

## Expected Behavior

The first substantive ChatGPT answer in a new task chat starts with:

- `Название чата для копирования`;
- `Карточка проекта`.

If the exact next number cannot be read from repo state, ChatGPT must say `Нужно выделить номер через repo chat-handoff-index / allocator.` instead of inventing or omitting the title.

## Remediation

- Add the ChatGPT first-answer contract to the master router and handoff scenario.
- Update canonical ChatGPT Project Instructions snippets.
- Add validator coverage for the first-answer contract and generated status card.
- Generate `reports/project-status-card.md` as a compact card artifact ChatGPT can read.
