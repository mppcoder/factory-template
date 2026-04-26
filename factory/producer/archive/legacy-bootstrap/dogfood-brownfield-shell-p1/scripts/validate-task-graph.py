#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml
from pathlib import Path
raw=sys.argv[1] if len(sys.argv)>1 else '.chatgpt/task-index.yaml'
p=Path(raw); path=p/'.chatgpt/task-index.yaml' if p.is_dir() else p
data=yaml.safe_load(path.read_text(encoding='utf-8')) or {}; tasks=data.get('tasks',[])
ids=[t.get('id') for t in tasks]; errs=[]; seen=set()
for tid in ids:
    if tid in seen: errs.append(f'Повторяющийся идентификатор задачи: {tid}')
    seen.add(tid)
task_map={t['id']:t for t in tasks if 'id' in t}
for t in tasks:
    tid=t.get('id')
    for dep in (t.get('depends_on') or []):
        if dep==tid: errs.append(f'Задача зависит сама от себя: {tid}')
        if dep not in task_map: errs.append(f'Не найдена зависимость: {tid} -> {dep}')
visited,temp=set(),set()
def dfs(tid):
    if tid in temp: errs.append(f'Обнаружен цикл зависимостей на задаче: {tid}'); return
    if tid in visited: return
    temp.add(tid)
    for dep in (task_map.get(tid,{}).get('depends_on') or []):
        if dep in task_map: dfs(dep)
    temp.remove(tid); visited.add(tid)
for tid in ids:
    if tid in task_map: dfs(tid)
if errs:
    print('ГРАФ ЗАДАЧ НЕКОРРЕКТЕН'); [print('-',e) for e in errs]; raise SystemExit(1)
print('ГРАФ ЗАДАЧ КОРРЕКТЕН')
