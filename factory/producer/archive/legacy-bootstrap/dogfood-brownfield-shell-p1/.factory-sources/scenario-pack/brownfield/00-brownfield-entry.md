# Вход в brownfield-режим

Цель: зафиксировать реальное состояние существующей системы до обсуждения изменений.

## Подсказка
Сначала опишите то, что реально существует, а не то, как хотелось бы это видеть.

## Canonical VPS Layout
Если brownfield-контур живёт на VPS, корень `/projects` должен содержать только project roots.

Рабочее правило:
- live project shell lives in `/projects/<project-root>/`;
- входящие архивы и install/input files при необходимости лежат в `/projects/<project-root>/_incoming/`;
- temporary, intermediate и reconstructed repo создаются только внутри `/projects/<project-root>/...`, а не рядом в `/projects`.

Для brownfield without repo это требование безусловное: нельзя создавать временные и промежуточные repo прямо в `/projects`.

## Правило фиксации gap / defect
Любой gap, найденный в reverse engineering или brownfield-анализе, должен стать bug report или structured defect report до remediation planning.
