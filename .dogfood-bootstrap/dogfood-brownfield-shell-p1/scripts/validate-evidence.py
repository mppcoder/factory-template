#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
TAGS=['[PROJECT]','[FIX]','[DOC]','[REAL]','[ASSUMPTION]']
IGNORE_PATTERNS=[r'^>\s*', r'^##\s*(допустимые теги|как заполнять|заполните ниже)', r'^-\s*(PROJECT|FIX|DOC|REAL|ASSUMPTION)', r'^-\s*укажите минимум', r'^#\s*']

def resolve(raw):
    if not raw: return Path('.chatgpt/evidence-register.md')
    p=Path(raw)
    return p/'.chatgpt/evidence-register.md' if p.is_dir() else p

def ignored(line: str) -> bool:
    s=line.strip()
    if not s:
        return True
    return any(re.search(p, s, flags=re.I) for p in IGNORE_PATTERNS)
path=resolve(sys.argv[1] if len(sys.argv)>1 else None)
if not path.exists() or not path.is_file():
    print('ОШИБКА: не найден файл evidence-register.md'); raise SystemExit(1)
text=path.read_text(encoding='utf-8')
found=[]
for line in text.splitlines():
    if ignored(line):
        continue
    if any(tag in line for tag in TAGS):
        found.append(line.strip())
unique=sorted({tag for line in found for tag in TAGS if tag in line})
meaningful=[]
link_like=0
for line in found:
    cleaned=re.sub(r'^[-*]\s*','',line).strip()
    after_tag=re.sub(r'^\[[A-Z]+\]\s*','',cleaned).strip()
    if len(after_tag) >= 18:
        meaningful.append(line)
    if re.search(r'(/|\.|issue|README|config|yaml|json|repo|документац|схем|шаблон|service|api|ветк|модул|worker)', line, flags=re.I):
        link_like += 1
if len(found)<2:
    print('РЕЕСТР ДОКАЗАТЕЛЬСТВ НЕКОРРЕКТЕН'); print('- Нужно минимум два evidence-пункта'); raise SystemExit(1)
if len(unique)<2:
    print('РЕЕСТР ДОКАЗАТЕЛЬСТВ НЕКОРРЕКТЕН'); print('- Нужно минимум два разных evidence-тега'); raise SystemExit(1)
if len(meaningful)<2:
    print('РЕЕСТР ДОКАЗАТЕЛЬСТВ НЕКОРРЕКТЕН'); print('- Пункты evidence выглядят как заглушки и заполнены слишком слабо'); raise SystemExit(1)
if link_like < 1:
    print('РЕЕСТР ДОКАЗАТЕЛЬСТВ НЕКОРРЕКТЕН'); print('- Нужно минимум одно указание на файл, репозиторий, документ или реальный источник'); raise SystemExit(1)
print('РЕЕСТР ДОКАЗАТЕЛЬСТВ КОРРЕКТЕН:', ', '.join(unique))
