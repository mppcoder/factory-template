## Обязательное правило фиксации дефектов
Если в ходе анализа, реализации, тестирования, reverse engineering или verification обнаружен дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure, его нельзя silently patch.

Нужно:
1. создать или обновить bug report в `reports/bugs/`;
2. собрать evidence и шаги воспроизведения;
3. указать слой дефекта: `project-only`, `factory-template` или `shared/unknown`;
4. при необходимости подготовить ChatGPT handoff bug note;
5. если проблема reusable — создать или обновить factory feedback в `reports/factory-feedback/` или `meta-feedback/`;
6. только после этого или одновременно с этим делать fix.
