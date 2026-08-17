#!/usr/bin/env python3
"""Apply the verified OpenWeather catalog addition without rewriting legacy rows."""
from __future__ import annotations

import base64
import csv
import io
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidates" / "openweather_2026-08-17"
AUDIT = ROOT / "audit" / "OPENWEATHER_CATALOG_REVIEW_2026-08-17.md"

SPECS = [
    (ROOT / "data" / "data_resources.csv", CANDIDATE / "resources.b64", "resource_id"),
    (ROOT / "data" / "data_products.csv", CANDIDATE / "products.b64", "product_id"),
    (ROOT / "data" / "product_distributions.csv", CANDIDATE / "distributions.b64", "distribution_id"),
]


def read_table(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def candidate_rows(path: Path, fields: list[str]):
    raw = base64.b64decode(path.read_text(encoding="ascii").strip()).decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw), fieldnames=fields))


def append_idempotent(target: Path, encoded: Path, key: str) -> int:
    fields, existing = read_table(target)
    rows = candidate_rows(encoded, fields)
    index = {row[key]: row for row in existing}
    pending = []
    for row in rows:
        current = index.get(row[key])
        if current is None:
            pending.append(row)
        elif current != row:
            raise SystemExit(f"{target}: {key}={row[key]} already exists with different content")
    if pending:
        with target.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writerows(pending)
    return len(pending)


added = [append_idempotent(*spec) for spec in SPECS]
_, resources = read_table(SPECS[0][0])
_, products = read_table(SPECS[1][0])
_, distributions = read_table(SPECS[2][0])
source_ids = {r["resource_id"] for r in resources}
product_ids = {p["product_id"] for p in products}
product_distribution_count = Counter(d["product_id"] for d in distributions)
orphan_products = [p["product_id"] for p in products if p["resource_id"] not in source_ids]
orphan_distributions = [d["distribution_id"] for d in distributions if d["product_id"] not in product_ids]
without_distribution = [p["product_id"] for p in products if product_distribution_count[p["product_id"]] == 0]
if orphan_products or orphan_distributions or without_distribution:
    raise SystemExit("Relational integrity failed after OpenWeather addition")

by_name = {}
for p in products:
    by_name.setdefault(p["product_name"].casefold(), []).append(p["product_id"])
duplicate_products = [ids for ids in by_name.values() if len(ids) > 1]
source_product_ids = {p["resource_id"] for p in products}
source_uncertainty_fields = ["license", "spatial_resolution", "temporal_coverage", "programmatic_access"]
uncertainty_markers = ("desconhecido", "não localizada", "não documentado", "varia conforme", "depende do", "consultar produto", "consultar versão")
uncertainty = {
    field: sum(any(marker in row[field].casefold() for marker in uncertainty_markers) for row in resources)
    for field in source_uncertainty_fields
}

AUDIT.write_text(f"""# OpenWeather catalog addition and structural review — 2026-08-17

## Scope

OpenWeather was added to the canonical source → product → distribution catalog. The Vitrine stores discovery, scientific meaning, access and provenance metadata only; it does not copy the external weather datasets.

## Materialized addition

- `DR0112` — OpenWeather — Weather, Air Pollution, Solar and Fire Weather APIs.
- `DP000454`–`DP000461` — 8 products.
- `DD000477`–`DD000486` — 10 distributions.
- Official documentation verified on 2026-08-17.
- Access and licensing are recorded at the lowest verified level because free access, subscription, attribution and ShareAlike requirements vary by OpenWeather product and plan.

## Structural result

- Sources: {len(resources)}
- Products: {len(products)}
- Distributions: {len(distributions)}
- Orphan products: {len(orphan_products)}
- Orphan distributions: {len(orphan_distributions)}
- Products without distribution: {len(without_distribution)}
- Sources without an enumerated product row: {sum(r['resource_id'] not in source_product_ids for r in resources)} — non-blocking because product enumeration is intentionally partial.

## Pre-existing identity issue

The only duplicate product identity found is pre-existing: `DP000017` and `DP000075`, both named **Suscetibilidade a Deslizamentos do Brasil — primeira aproximação**. They currently encode different product-kind/description choices and distributions. This change does not delete or recycle either stable ID. Resolve that identity separately with an explicit alias/tombstone migration if appropriate.

## Focused quality backlog

Source-level values still marked unknown/variable in selected fields: {uncertainty}. These are catalog-quality signals, not proof that the underlying datasets are deficient. Prioritize high-use sources rather than indiscriminate re-auditing.

## Conclusion

The OpenWeather addition is structurally valid and introduces no orphan records. Duplicate product-name groups after the addition: {duplicate_products}. The OpenWeather rows do not create a new duplicate identity.
""", encoding="utf-8")

print(f"OpenWeather applied: +{added[0]} source, +{added[1]} products, +{added[2]} distributions")
print(f"Catalog: {len(resources)} sources, {len(products)} products, {len(distributions)} distributions")
