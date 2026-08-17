# OpenWeather catalog addition and structural review — 2026-08-17

## Scope

OpenWeather was added to the canonical source → product → distribution catalog. The Vitrine stores discovery, scientific meaning, access and provenance metadata only; it does not copy the external weather datasets.

## Materialized addition

- `DR0112` — OpenWeather — Weather, Air Pollution, Solar and Fire Weather APIs.
- `DP000454`–`DP000461` — 8 products.
- `DD000477`–`DD000486` — 10 distributions.
- Official documentation verified on 2026-08-17.
- Access and licensing are recorded at the lowest verified level because free access, subscription, attribution and ShareAlike requirements vary by OpenWeather product and plan.

## Structural result

- Sources: 112
- Products: 457
- Distributions: 482
- Orphan products: 0
- Orphan distributions: 0
- Products without distribution: 0
- Sources without an enumerated product row: 35 — non-blocking because product enumeration is intentionally partial.

## Pre-existing identity issue

The only duplicate product identity found is pre-existing: `DP000017` and `DP000075`, both named **Suscetibilidade a Deslizamentos do Brasil — primeira aproximação**. They currently encode different product-kind/description choices and distributions. This change does not delete or recycle either stable ID. Resolve that identity separately with an explicit alias/tombstone migration if appropriate.

## Focused quality backlog

Source-level values still marked unknown/variable in selected fields: {'license': 48, 'spatial_resolution': 46, 'temporal_coverage': 40, 'programmatic_access': 30}. These are catalog-quality signals, not proof that the underlying datasets are deficient. Prioritize high-use sources rather than indiscriminate re-auditing.

## Conclusion

The OpenWeather addition is structurally valid and introduces no orphan records. Duplicate product-name groups after the addition: [['DP000017', 'DP000075']]. The OpenWeather rows do not create a new duplicate identity.
