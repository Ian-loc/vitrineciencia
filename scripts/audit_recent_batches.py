from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
products_path = ROOT / 'data/data_products.csv'
dists_path = ROOT / 'data/product_distributions.csv'

products = products_path.read_text(encoding='utf-8').splitlines()
dists = dists_path.read_text(encoding='utf-8').splitlines()

for i, line in enumerate(dists):
    if line.startswith('DD000066,'):
        dists[i] = line.replace('API documentada; apikey pode ser requerida para operações','API aberta, porém cada chamada requer uma chave de acesso no parâmetro apikey')
    elif line.startswith('DD000079,'):
        parts = line.split(',')
        parts[10] = 'Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada (CC BY-ND 3.0)'
        dists[i] = ','.join(parts)
    elif line.startswith('DD000080,'):
        parts = line.split(',')
        parts[10] = 'Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada (CC BY-ND 3.0)'
        dists[i] = ','.join(parts)
    elif line.startswith('DD000081,'):
        parts = line.split(',')
        parts[10] = 'Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada (CC BY-ND 3.0)'
        note = parts[13]
        if 'duas chaves' not in note.lower():
            note += ' O acesso à API exige solicitação por e-mail e duas chaves exclusivas.'
        parts[13] = note
        dists[i] = ','.join(parts)

for i, line in enumerate(products):
    if line.startswith('DP000065,'):
        parts = line.split(',')
        extra = ' As previsões do módulo meteorológico correspondem à saída bruta dos modelos GFS/WRF sem intervenção de meteorologistas; não confundir previsão modelada com observação de EMS.'
        if 'GFS/WRF' not in parts[22]:
            parts[22] += extra
        products[i] = ','.join(parts)
    elif line.startswith('DP000058,'):
        parts = line.split(',')
        extra = ' O serviço legado de telemetria teve prazo de migração prorrogado apenas até 30/06/2026; para acesso programático corrente deve-se usar o Hidro Webservice documentado pela ANA.'
        if '30/06/2026' not in parts[22]:
            parts[22] += extra
        products[i] = ','.join(parts)

products_path.write_text('\n'.join(products)+'\n', encoding='utf-8')
dists_path.write_text('\n'.join(dists)+'\n', encoding='utf-8')

ptxt = products_path.read_text(encoding='utf-8')
dtxt = dists_path.read_text(encoding='utf-8')
assert 'cada chamada requer uma chave de acesso' in dtxt
assert dtxt.count('CC BY-ND 3.0') >= 3
assert 'GFS/WRF' in ptxt
assert '30/06/2026' in ptxt
