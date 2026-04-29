# Вход в brownfield-режим

Цель: зафиксировать реальное состояние существующей системы до обсуждения изменений.

## Подсказка
Сначала опишите то, что реально существует, а не то, как хотелось бы это видеть.

## Default-decision layer для brownfield

Brownfield intake тоже recommendation-first. В начале зафиксируй `default_decision_mode`: `global-defaults`, `confirm-each-default` или `manual`.

Для brownfield with repo recommended defaults:

- keep existing repo as canonical root when possible;
- do not overwrite product-owned code;
- evidence-first audit before remediation;
- convert to `greenfield-product` / `greenfield-converted` или documented blocker.

Для brownfield without repo recommended defaults:

- incoming materials live in `/projects/<target-slug>/_incoming`;
- reconstructed/intermediate repos live only inside target project root, not siblings in `/projects`;
- path: evidence inventory -> reconstruction -> with-repo adoption -> greenfield conversion.

Каждый default должен быть explainable and overrideable. Записывай `accepted_defaults`, `overridden_defaults`, `default_source_basis`, `uncertainty_notes` и `decisions_requiring_user_confirmation`. Risky, paid, destructive, security, privacy, legal и secret-related decisions требуют explicit user confirmation.

## Canonical VPS layout / каноническая VPS layout
Если brownfield-контур живёт на VPS, корень `/projects` должен содержать только project roots.

Рабочее правило:
- live project shell lives in `/projects/<project-root>/`;
- входящие архивы и install/input files при необходимости лежат в `/projects/<project-root>/_incoming/`;
- temporary, intermediate, reconstructed и helper repo создаются только внутри repo целевого `greenfield-product`, например `/projects/<target-greenfield-project>/...`, а не рядом в `/projects`.

Для brownfield without repo это требование безусловное: нельзя создавать временные и промежуточные repo прямо в `/projects`.

## Правило фиксации gap / defect
Любой gap, найденный в reverse engineering или brownfield-анализе, должен стать bug report или structured defect report до remediation planning.
