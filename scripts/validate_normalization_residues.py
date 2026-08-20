#!/usr/bin/env python3
"""Bloqueia regressões silenciosas na fila de normalização pública.

O relatório de cobertura continua descritivo. Este gate compara os IDs ainda
pendentes com uma baseline versionada e exige correspondência exata. Assim, uma
nova pendência não pode substituir silenciosamente outra que tenha sido resolvida.
"""
from __future__ import annotations

import json
from pathlib import Path

import report_normalization_coverage as report

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "schema" / "public-normalization-pending-v0.1.json"
PRODUCT_JSON = ROOT / "data" / "data_products.json"
FIELDS = (
    "spatial_support",
    "update_frequency",
    "spatial_resolution",
    "temporal_coverage",
    "temporal_resolution",
    "version_or_collection",
)


def load_baseline(valid_ids: set[str]) -> dict[str, set[str]]:
    payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "0.1":
        raise SystemExit("schema_version inesperada em public-normalization-pending-v0.1.json")

    unexpected = sorted(set(payload) - {"schema_version", "purpose", *FIELDS})
    if unexpected:
        raise SystemExit(f"campos inesperados na baseline de normalização: {unexpected}")

    baseline: dict[str, set[str]] = {}
    for field in FIELDS:
        values = payload.get(field)
        if not isinstance(values, list):
            raise SystemExit(f"baseline {field} deve ser uma lista")
        if len(values) != len(set(values)):
            raise SystemExit(f"baseline {field} contém IDs duplicados")
        unknown = sorted(set(values) - valid_ids)
        if unknown:
            raise SystemExit(f"baseline {field} referencia produtos inexistentes: {unknown}")
        baseline[field] = set(values)
    return baseline


def current_pending() -> tuple[dict[str, set[str]], set[str]]:
    raw = report.read_csv()
    public = json.loads(PRODUCT_JSON.read_text(encoding="utf-8"))
    public_by_id = {row["product_id"]: row for row in public}
    valid_ids = {row["product_id"] for row in raw}

    if set(public_by_id) != valid_ids:
        only_raw = sorted(valid_ids - set(public_by_id))
        only_public = sorted(set(public_by_id) - valid_ids)
        raise SystemExit(
            "data_products.json não corresponde aos IDs canônicos; "
            f"somente_csv={only_raw[:10]} somente_json={only_public[:10]}"
        )

    support_ids = [row["product_id"] for row in raw if report.support_warning(row)]
    update_ids = [row["product_id"] for row in raw if report.update_warning(row)]

    pending: dict[str, set[str]] = {
        "spatial_support": {
            pid
            for pid in support_ids
            if public_by_id.get(pid, {}).get("spatial_support") in {"", "desconhecido"}
        },
        "update_frequency": {
            pid
            for pid in update_ids
            if public_by_id.get(pid, {}).get("update_frequency") in {"", "desconhecida"}
        },
    }

    warning_fns = {
        "spatial_resolution": report.spatial_resolution_warning,
        "temporal_coverage": report.temporal_coverage_warning,
        "temporal_resolution": report.temporal_resolution_warning,
        "version_or_collection": report.version_warning,
    }
    for field, warning_fn in warning_fns.items():
        _, field_pending = report.field_coverage(raw, public_by_id, warning_fn)
        pending[field] = set(field_pending)

    return pending, valid_ids


def main() -> None:
    pending, valid_ids = current_pending()
    baseline = load_baseline(valid_ids)

    failures: list[str] = []
    for field in FIELDS:
        new = sorted(pending[field] - baseline[field])
        removed = sorted(baseline[field] - pending[field])
        if new or removed:
            failures.append(
                f"{field}: novas={new or '[]'}; resolvidas_sem_atualizar_baseline={removed or '[]'}"
            )

    if failures:
        raise SystemExit(
            "Fila de resíduos da normalização mudou. Revise a mudança e atualize a baseline "
            "no mesmo PR, se deliberada:\n- " + "\n- ".join(failures)
        )

    summary = ", ".join(f"{field}={len(pending[field])}" for field in FIELDS)
    print(f"OK normalization residue baseline: {summary}")


if __name__ == "__main__":
    main()
