# Factory ops — дополнительный operational слой

Этот пакет не входит в обязательное ядро фабрики.
Он нужен для эксплуатационной дисциплины вокруг шаблона:
- проверка drift между фабрикой и working project;
- сбор advisory patch bundle для обратной синхронизации;
- детектор признаков factory issue;
- optional git hooks.
