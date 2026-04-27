# Feature workspace: plan-3-eval-adoption

Этот workspace поддерживает resumable planning:
1. Заполните интервью (можно частями):
   python3 "/projects/factory-template/template-repo/scripts/resume-setup.py" --workspace "/projects/factory-template/template-repo/../work/features/plan-3-eval-adoption" --answer problem="..."
2. Сгенерируйте user-spec:
   python3 "/projects/factory-template/template-repo/scripts/generate-user-spec.py" --workspace "/projects/factory-template/template-repo/../work/features/plan-3-eval-adoption"
3. Сгенерируйте tech-spec и задачи:
   python3 "/projects/factory-template/template-repo/scripts/decompose-feature.py" --workspace "/projects/factory-template/template-repo/../work/features/plan-3-eval-adoption"

Можно остановиться в любой момент и вернуться позже: состояние хранится в interview-state.yaml.
Если нужен advanced feature execution, создайте workspace с --advanced-execution и ведите logs/checkpoint.yaml после каждой wave.
