#!/usr/bin/env python3
import csv, io, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def preserve_append(path, id_field, keep_ids):
    p=ROOT/path
    with p.open(encoding='utf-8', newline='') as f:
        r=csv.DictReader(f); fields=r.fieldnames; selected=[x for x in r if x[id_field] in keep_ids]
    assert {x[id_field] for x in selected}==set(keep_ids)
    baseline=subprocess.check_output(['git','show',f'origin/main:{path}'],cwd=ROOT,text=True)
    s=io.StringIO(newline='')
    w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n'); w.writerows(selected)
    p.write_text(baseline.rstrip('\n')+'\n'+s.getvalue(),encoding='utf-8',newline='')

preserve_append('data/data_products.csv','product_id',['DP000127','DP000128','DP000129'])
preserve_append('data/product_distributions.csv','distribution_id',['DD000143','DD000144','DD000145'])
for cmd in [
 ['python','scripts/validate_brazil_scope.py'],
 ['python','scripts/validate_product_catalog.py'],
 ['python','scripts/build_catalog.py'],
 ['python','scripts/audit_link_roles.py','--write'],
 ['python','scripts/audit_link_roles.py'],
 ['python','scripts/validate_vitrine.py']]:
    print('+',' '.join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True)
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('NORMALIZED append-only canonical delta: +3 products, +3 distributions')
