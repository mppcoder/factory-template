# Learning patch proposal / тест proposal

source_bug: reports/bugs/reusable.md
status: proposed
target_surface: validator
proposed_change: "Добавить проверку reusable bug learning."
verification: "Запустить validate-learning-patch-loop.py на positive fixture."
justification: "Reusable bug влияет на будущие factory tasks."

## Контекст

Bug повторяемый и должен давать reusable factory learning.

## Предложение

Добавить validator contract для новых reusable bug reports.

## Проверка

Positive fixture должна проходить.
