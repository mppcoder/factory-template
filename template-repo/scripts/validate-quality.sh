#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys, re, yaml
root=Path(sys.argv[1] if len(sys.argv)>1 else '.'); chat=root/'.chatgpt'; errors=[]
classes_file=root/'change-classes.yaml'
if not classes_file.exists():
    classes_file=Path(__file__).resolve().parents[1]/'change-classes.yaml'

def non_placeholder(text):
    out=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line.startswith('>') or line.startswith('#') or line in {'-','*','""',"''"}: continue
        if '{{' in line and '}}' in line: continue
        if line.lower().startswith('подсказка:') or line.lower().startswith('пример:'): continue
        out.append(line)
    return out

def has_any(text,pats): return any(re.search(p,text,flags=re.I|re.M) for p in pats)
rp=chat/'reality-check.md'
if not rp.exists(): errors.append('Не найден .chatgpt/reality-check.md')
else:
    text=rp.read_text(encoding='utf-8')
    groups=[[r'^##\s*(текущее состояние проекта|что подтверждено в проекте|что найдено в проекте)'],[r'^##\s*(официальная документация|что говорит документация|что говорит официальная документация|что сказано в официальной документации|выводы по документации)'],[r'^##\s*(реальные кейсы|реальные кейсы и известные баги|какие есть реальные кейсы, issue-треды и известные баги|какие есть реальные кейсы, issues и known bugs|реальные наблюдения и кейсы)'],[r'^##\s*(сопоставление|расхождения|где есть расхождения между проектом и внешними источниками|конфликты и расхождения|расхождения и выводы)'],[r'^##\s*(вывод|предварительный вывод|итоговый вывод|вывод по проверке реальности|итог проверки реальности)']]
    for pats in groups:
        if not has_any(text,pats): errors.append('reality-check.md не содержит один из обязательных смысловых разделов'); break
    if len(non_placeholder(text))<8: errors.append('reality-check.md выглядит слишком пустым: нужно больше конкретных строк с фактами и выводами')
    if not re.search(r'верси|version|v\d+\.\d+|релиз', text, flags=re.I): errors.append('reality-check.md: нет явных признаков проверки версий или релизов')
    if not re.search(r'/|\.ya?ml|\.json|\.md|config|конфиг|repo|ветк|файл|директор', text, flags=re.I): errors.append('reality-check.md: нет ссылок на файлы, конфиги или repo-состояние')
    if not re.search(r'расхожд|не совпад|конфликт|вывод|сопостав', text, flags=re.I): errors.append('reality-check.md: нет зафиксированных расхождений или вывода')
ep=chat/'evidence-register.md'
if not ep.exists(): errors.append('Не найден .chatgpt/evidence-register.md')
else:
    text=ep.read_text(encoding='utf-8'); tags=re.findall(r'\[(PROJECT|FIX|DOC|REAL|ASSUMPTION)\]', text)
    meaningful=[l for l in non_placeholder(text) if '[' in l and re.search(r'\[[A-Z]+\]\s+.{10,}', l)]
    if len(tags)<2: errors.append('evidence-register.md должен содержать минимум два evidence-тега')
    if len(set(tags))<2: errors.append('evidence-register.md должен содержать минимум два разных evidence-тега')
    if len(meaningful)<2: errors.append('evidence-register.md должен содержать минимум два содержательных пункта')
ip=chat/'task-index.yaml'
if not ip.exists(): errors.append('Не найден .chatgpt/task-index.yaml')
else:
    data=yaml.safe_load(ip.read_text(encoding='utf-8')) or {}; change=data.get('change',{}) if isinstance(data,dict) else {}; tasks=data.get('tasks',[]) if isinstance(data,dict) else []
    for field in ['id','title','summary']:
        if not str(change.get(field,'')).strip(): errors.append(f'task-index.yaml: change.{field} должен быть заполнен')
    classes=(yaml.safe_load(classes_file.read_text(encoding='utf-8')) or {}).get('change_classes', {}) if classes_file.exists() else {}
    change_class=change.get('class')
    cfg=classes.get(change_class, {}) if isinstance(classes, dict) else {}
    for rel in cfg.get('required_artifacts', []) if isinstance(cfg, dict) else []:
        if not (root / rel).exists():
            errors.append(f'task-index.yaml: для класса {change_class} отсутствует обязательный артефакт {rel}')
    if not isinstance(tasks,list) or not tasks: errors.append('task-index.yaml: должна быть хотя бы одна задача')
    else:
        for i,task in enumerate(tasks,1):
            tid=task.get('id',f'#{i}')
            if not str(task.get('title','')).strip(): errors.append(f'task-index.yaml: у задачи {tid} не заполнен title')
            if not isinstance(task.get('outputs',[]),list) or not task.get('outputs'): errors.append(f'task-index.yaml: у задачи {tid} должен быть минимум один output')
            if not isinstance(task.get('acceptance',[]),list) or not task.get('acceptance'): errors.append(f'task-index.yaml: у задачи {tid} должен быть минимум один acceptance criterion')
for name in ['user-spec-validation.md','tech-spec-validation.md','verification-report.md','done-report.md']:
    p=chat/name
    if not p.exists(): errors.append(f'Не найден .chatgpt/{name}'); continue
    if len(non_placeholder(p.read_text(encoding='utf-8')))<4: errors.append(f'{name} выглядит слишком пустым: нужно минимум 4 содержательные строки')
if errors:
    print('ПРОВЕРКА КАЧЕСТВА НЕ ПРОЙДЕНА'); [print('-',e) for e in errors]; raise SystemExit(1)
print('ПРОВЕРКА КАЧЕСТВА ПРОЙДЕНА')
