# Factory Feedback 051: ChatGPT first answer needs title and card

Date: 2026-04-29

## Learning

Repo-first routing is not enough for a useful ChatGPT task start. The operator also needs a stable chat title to copy and a compact project card in the first answer, before route receipt or handoff details.

## Template Change

- `00-master-router.md` now defines a `ChatGPT First Answer Contract`.
- ChatGPT Project instruction snippets require `Название чата для копирования` and `Карточка проекта`.
- `validate-chatgpt-first-answer-contract.py` blocks missing first-answer contract drift.
- `reports/project-status-card.md` stores the compact card for ChatGPT readback when command execution is unavailable.
