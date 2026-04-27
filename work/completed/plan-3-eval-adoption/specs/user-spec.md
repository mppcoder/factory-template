# User Spec: Plan 3 Artifact Eval Adoption

> generated_at: 2026-04-27T12:21:06+03:00
> feature_id: plan-3-eval-adoption
> Этот документ отвечает на вопрос "что хочет пользователь" и должен быть понятен человеку без технического бэкграунда.

## Короткое описание
Закрыть P3-S3/P3-S4 как repo-native доказательство: расширить Artifact Eval Harness на routing-critical артефакты и провести реальный `feature-execution-lite` adoption через workspace, checkpoint, decisions, tasks и closeout.

## Какую проблему решаем
После Plan №3 audit часть улучшений была только roadmap. Нужно показать, что eval coverage и advanced feature execution работают на реальном изменении factory-template, не меняя beginner path и не заявляя runtime proof.

## Для кого делаем
- Пользователь factory-template, который хочет видеть проверяемое evidence перед следующей стадией Plan №3.
- Будущий Codex/ChatGPT исполнитель, которому нужен понятный след решений и проверок.

## Пользовательская ценность
Repo получает конкретное доказательство, что Artifact Eval и feature-execution-lite применимы к настоящему factory change, а не только к sample fixtures.

## Что входит в первую версию
- Новые Artifact Eval specs/reports для routing-critical артефактов.
- Negative fixtures для известных overclaim/source-boundary рисков.
- Один real advanced `work/features/...` workspace с задачами, checkpoint и closeout.
- Release/state/test docs, отражающие P3-S3/P3-S4 без смешивания с P3-S5 runtime QA.

## Что не входит в первую версию
- Реальный VPS deploy, backup restore или rollback drill.
- Внедрение task-state/evolve code сверх уже закрытого P3-S1/S2.
- Изменение beginner default path.

## Ограничения
- Dry-run/report-ready не считается production proof.
- External runtime evidence требует отдельного approval, secrets boundary и sanitized transcript.
- Workspace должен жить в repo-level `work/features`, не в `template-repo/work` и не в generated-project root artifacts.

## Критерии приемки
- Artifact Eval reports валидируются общим validator.
- `feature-execution-lite` adoption workspace проходит advanced validator до closeout.
- Closeout создаёт done-report, Project Knowledge proposal и downstream-impact.
- Quick verify проходит зелёно.

## User Intent Anchors
Короткие метки исходного пользовательского намерения. На них ссылаются tech-spec и задачи.

- US-001: расширить eval coverage на routing-critical артефакты.
- US-002: adoption `feature-execution-lite` на реальном factory change.
- US-003: сохранить boundary: beginner path unchanged, runtime proof deferred to P3-S5.

## User-Spec Deviations
Обычно здесь `Нет`. Если позже агент предлагает отойти от исходного intent, deviation нужно перенести в tech-spec и утвердить отдельно.

Нет.

## Открытые вопросы
Нет для P3-S3/P3-S4. P3-S5 остаётся отдельной следующей стадией.
