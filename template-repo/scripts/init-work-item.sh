#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml, pathlib
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
data = yaml.safe_load((root/".chatgpt/task-index.yaml").read_text(encoding="utf-8"))
change = data.get("change", {})
tasks = data.get("tasks", [])
change_id = change.get("id") or "chg-unknown-000"
change_class = change.get("class", "")
execution_mode = change.get("execution_mode", "")
work_dir = root/"work/active"/change_id
(work_dir/"tasks").mkdir(parents=True, exist_ok=True)
(work_dir/"brief.md").write_text(f"# {change.get('title', change_id)}\n\n## Что это за изменение\n\nЗаполните краткое описание изменения.\n", encoding="utf-8")
(work_dir/"plan.md").write_text(f"# План по {change_id}\n\nОпишите последовательность выполнения задач.\n", encoding="utf-8")
(work_dir/"verification.md").write_text(f"# Проверка по {change_id}\n\nОпишите, как будет подтверждаться результат.\n", encoding="utf-8")
template = (root/"work/_task-template.md").read_text(encoding="utf-8")
for task in tasks:
    txt = template.replace("{{TASK_ID}}", task.get("id", "")).replace("{{TASK_TITLE}}", task.get("title", "")).replace("{{CHANGE_CLASS}}", change_class).replace("{{EXECUTION_MODE}}", execution_mode)
    (work_dir/"tasks"/f"{task.get('id', 'TASK')}.md").write_text(txt, encoding="utf-8")
print(f"Work item создан: {work_dir}")
