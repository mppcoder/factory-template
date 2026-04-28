# Factory feedback: project-root boundary для intermediate repos

Дата: 2026-04-28

## Наблюдение

Фабричный запрет плоского `/projects` дерева был недостаточно точным для промежуточных repo: требовалось явно сказать, что они находятся внутри целевого `greenfield-product` repo.

## Предложение

Считать top-level `/projects` только реестром конечных project roots. Любые temporary/intermediate/reconstructed/helper repos для intake, adoption или reconstruction должны быть project-local workspaces внутри `/projects/<target-greenfield-project>/...`.

## Применение

- Active docs и scenario-pack должны использовать эту формулировку.
- Validators/evals должны ловить откат к неоднозначному "corresponding project root".
- Generated/bootstrap packs должны запрещать sibling intermediate repos в `/projects`.

## Статус

Применено в текущем scope.
