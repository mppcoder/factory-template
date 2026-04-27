## Обязательное правило фиксации дефектов
Если в ходе анализа, реализации, тестирования, reverse engineering или verification обнаружен дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure, его нельзя silently patch.

Нужно:
1. создать или обновить bug report в `reports/bugs/`;
2. собрать evidence и шаги воспроизведения;
3. указать слой дефекта: `project-only`, `factory-template` или `shared/unknown`;
4. определить, исправляется ли дефект в текущем scope или требует отдельного task boundary;
5. выполнить self-handoff для нового defect;
6. при необходимости подготовить ChatGPT handoff bug note или deep-research prompt;
7. если проблема reusable — создать или обновить factory feedback в `reports/factory-feedback/` или `meta-feedback/`;
8. для reusable bug указать `learning_patch_status: required` и создать `reports/learnings/<bug-id>-learning-patch.md`, либо указать `learning_patch_status: not_required` с причиной;
9. только после этого или одновременно с этим делать fix.
