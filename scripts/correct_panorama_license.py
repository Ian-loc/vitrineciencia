from pathlib import Path
import csv, io

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/product_distributions.csv'
lines = path.read_text(encoding='utf-8').splitlines()
header = next(csv.reader([lines[0]]))
idx = {name:i for i,name in enumerate(header)}

def parse(line):
    return next(csv.reader([line]))

def render(row):
    buf = io.StringIO(); csv.writer(buf, lineterminator='').writerow(row); return buf.getvalue()

for i, line in enumerate(lines):
    if line.startswith(('DD000079,','DD000080,','DD000081,')):
        row = parse(line)
        row[idx['license']] = 'licença específica do dado/API não localizada; o portal informa CC BY-ND 3.0 para o conteúdo do site'
        note = row[idx['notes']]
        extra = ' A licença exibida no rodapé do PANORAMA refere-se ao conteúdo do site; não foi localizada, nesta auditoria, uma declaração inequívoca de que esta licença se aplica especificamente aos dados/API desta distribuição.'
        if 'rodapé do PANORAMA' not in note:
            row[idx['notes']] = note + extra
        lines[i] = render(row)

path.write_text('\n'.join(lines)+'\n', encoding='utf-8')
text = path.read_text(encoding='utf-8')
assert text.count('licença específica do dado/API não localizada; o portal informa CC BY-ND 3.0 para o conteúdo do site') == 3
