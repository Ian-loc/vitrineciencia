from pathlib import Path
import csv
import io

ROOT = Path(__file__).resolve().parents[1]
products_path = ROOT / 'data/data_products.csv'
dists_path = ROOT / 'data/product_distributions.csv'

products = products_path.read_text(encoding='utf-8').splitlines()
dists = dists_path.read_text(encoding='utf-8').splitlines()

product_header = next(csv.reader([products[0]]))
dist_header = next(csv.reader([dists[0]]))
pi = {name: idx for idx, name in enumerate(product_header)}
di = {name: idx for idx, name in enumerate(dist_header)}

def parse(line):
    return next(csv.reader([line]))

def render(row):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='')
    w.writerow(row)
    return buf.getvalue()

for i, line in enumerate(dists):
    if line.startswith('DD000066,'):
        row = parse(line)
        row[di['access_conditions']] = 'API aberta, porém cada chamada requer uma chave de acesso no parâmetro apikey'
        dists[i] = render(row)
    elif line.startswith(('DD000079,','DD000080,','DD000081,')):
        row = parse(line)
        row[di['license']] = 'Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada (CC BY-ND 3.0)'
        if line.startswith('DD000081,'):
            note = row[di['notes']]
            if 'duas chaves' not in note.lower():
                note += ' O acesso à API exige solicitação por e-mail e duas chaves exclusivas.'
            row[di['notes']] = note
        dists[i] = render(row)

for i, line in enumerate(products):
    if line.startswith('DP000065,'):
        row = parse(line)
        extra = ' As previsões do módulo meteorológico correspondem à saída bruta dos modelos GFS/WRF sem intervenção de meteorologistas; não confundir previsão modelada com observação de EMS.'
        if 'GFS/WRF' not in row[pi['limitations']]:
            row[pi['limitations']] += extra
        products[i] = render(row)
    elif line.startswith('DP000058,'):
        row = parse(line)
        extra = ' O serviço legado de telemetria teve prazo de migração prorrogado apenas até 30/06/2026; para acesso programático corrente deve-se usar o Hidro Webservice documentado pela ANA.'
        if '30/06/2026' not in row[pi['limitations']]:
            row[pi['limitations']] += extra
        products[i] = render(row)

products_path.write_text('\n'.join(products)+'\n', encoding='utf-8')
dists_path.write_text('\n'.join(dists)+'\n', encoding='utf-8')

ptxt = products_path.read_text(encoding='utf-8')
dtxt = dists_path.read_text(encoding='utf-8')
assert 'cada chamada requer uma chave de acesso' in dtxt
assert dtxt.count('CC BY-ND 3.0') >= 3
assert 'GFS/WRF' in ptxt
assert '30/06/2026' in ptxt
