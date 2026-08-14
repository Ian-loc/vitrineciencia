import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/brazil_scope_priorities.json'
data=json.loads(p.read_text(encoding='utf-8'))
for tier in data['tiers']:
    if tier['priority_tier']=='P0':
        for rid in ['DR0061','DR0062']:
            if rid not in tier['resource_ids']:
                tier['resource_ids'].append(rid)
        tier['resource_ids']=sorted(tier['resource_ids'])
data['reviewed_at']='2026-08-14'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('OK: DR0061-DR0062 registrados em P0')
