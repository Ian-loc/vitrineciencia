#!/usr/bin/env python3
import csv, io, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[('data/data_resources.csv','resource_id','DR0058'),('data/data_products.csv','product_id','DP000039'),('data/product_distributions.csv','distribution_id','DD000047')]
for rel,key,last_base in SPECS:
    path=ROOT/rel
    with path.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); fields=list(r.fieldnames or []); rows=list(r)
    new=[x for x in rows if x[key]>last_base]
    baseline=subprocess.check_output(['git','show',f'origin/main:{rel}']).decode('utf-8')
    if not baseline.endswith('\n'): baseline+='\n'
    buf=io.StringIO(newline='')
    w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n'); w.writerows(new)
    path.write_text(baseline+buf.getvalue(),encoding='utf-8')
    print(rel, 'novas linhas:', len(new))
