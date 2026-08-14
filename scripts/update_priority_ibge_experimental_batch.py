from pathlib import Path
import json
p = Path(__file__).resolve().parents[1] / 'data' / 'brazil_scope_priorities.json'
obj = json.loads(p.read_text(encoding='utf-8'))
for tier in obj['tiers']:
    if tier['priority_tier'] == 'P0':
        ids = tier['resource_ids']
        for rid in ('DR0063','DR0064'):
            if rid not in ids:
                ids.append(rid)
        ids.sort()
obj['reviewed_at'] = '2026-08-15'
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
