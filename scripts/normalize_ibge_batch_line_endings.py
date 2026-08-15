from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for rel in ['data/data_resources.csv','data/data_products.csv','data/product_distributions.csv']:
    p = ROOT / rel
    b = p.read_bytes()
    p.write_bytes(b.replace(b'\r\n', b'\n'))
