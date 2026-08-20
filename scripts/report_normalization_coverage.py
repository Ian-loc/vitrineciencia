#!/usr/bin/env python3
"""Mede cobertura da normalização pública e expõe apenas resíduos reais.

Não altera os dados. O relatório distingue problemas históricos do CSV de casos
que já possuem representação pública comparável e de valores mantidos como
"desconhecidos" após revisão explícita da evidência canônica.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_CSV = ROOT / "data" / "data_products.csv"
PRODUCT_JSON = ROOT / "data" / "data_products.json"
REVIEWED_UNKNOWNS = ROOT / "schema" / "public-normalization-reviewed-unknowns-v0.1.json"


def read_csv() -> list[dict[str, str]]:
    with PRODUCT_CSV.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split("|") if item.strip()]


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def contains_any(value: str, patterns: tuple[str, ...]) -> bool:
    text = norm(value)
    return any(pattern in text for pattern in patterns)


def contains_word(value: str, words: tuple[str, ...]) -> bool:
    text = norm(value)
    return any(re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text) for word in words)


def support_warning(row: dict[str, str]) -> bool:
    value = row.get("spatial_support", "")
    items = split_pipe(value)
    return len(items) >= 3 and contains_any(value, ("mapa", "tabela", "gráfico", "grafico", "análise", "analise"))


def update_warning(row: dict[str, str]) -> bool:
    value = row.get("update_frequency", "")
    return ";" in value or len(value) > 90


def spatial_resolution_warning(row: dict[str, str]) -> bool:
    return contains_word(
        row.get("spatial_resolution", ""),
        ("diária", "diaria", "mensal", "anual", "semanal", "trimestral"),
    )


def temporal_coverage_warning(row: dict[str, str]) -> bool:
    return contains_any(
        row.get("temporal_coverage", ""),
        ("atualização diária", "atualizacao diaria", "atualizado diariamente", "frequência de atualização", "frequencia de atualizacao"),
    )


def temporal_resolution_warning(row: dict[str, str]) -> bool:
    return contains_any(
        row.get("temporal_resolution", ""),
        ("atualizado", "publicado", "edição corrente", "edicao corrente"),
    )


def version_warning(row: dict[str, str]) -> bool:
    return contains_any(
        row.get("version_or_collection", ""),
        ("auditado em", "acesso auditado", "atualização diária", "atualizacao diaria"),
    )


def pct(done: int, total: int) -> float:
    return round((100 * done / total), 1) if total else 100.0


def reviewed_unknown_ids(field: str) -> set[str]:
    if not REVIEWED_UNKNOWNS.exists():
        return set()
    payload = json.loads(REVIEWED_UNKNOWNS.read_text(encoding="utf-8"))
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        return set()
    return {
        str(entry.get("product_id", "")).strip()
        for entry in entries
        if isinstance(entry, dict) and entry.get("field") == field and entry.get("product_id")
    }


def field_coverage(
    raw_rows: list[dict[str, str]],
    public_by_id: dict[str, dict[str, str]],
    warning_fn,
) -> tuple[list[str], list[str]]:
    ids = [row["product_id"] for row in raw_rows if warning_fn(row)]
    resolved = [pid for pid in ids if not warning_fn(public_by_id.get(pid, {}))]
    pending = [pid for pid in ids if pid not in resolved]
    return resolved, pending


def print_pending(title: str, pending: list[str], raw_by_id: dict[str, dict[str, str]], field: str) -> None:
    if not pending:
        return
    print(f"PENDÊNCIAS {title}: {len(pending)}")
    for pid in pending:
        row = raw_by_id[pid]
        print(f"- {pid} | {row.get('product_name','')} | {row.get(field,'')}")


def main() -> None:
    raw = read_csv()
    public = json.loads(PRODUCT_JSON.read_text(encoding="utf-8"))
    by_id = {row["product_id"]: row for row in public}
    raw_by_id = {row["product_id"]: row for row in raw}

    support_ids = [row["product_id"] for row in raw if support_warning(row)]
    update_ids = [row["product_id"] for row in raw if update_warning(row)]
    support_resolved = [pid for pid in support_ids if by_id.get(pid, {}).get("spatial_support") not in {"", "desconhecido"}]
    update_resolved = [pid for pid in update_ids if by_id.get(pid, {}).get("update_frequency") not in {"", "desconhecida"}]

    support_unknown_candidates = [pid for pid in support_ids if pid not in support_resolved]
    update_unknown_candidates = [pid for pid in update_ids if pid not in update_resolved]
    reviewed_support_ids = reviewed_unknown_ids("spatial_support")
    reviewed_update_ids = reviewed_unknown_ids("update_frequency")
    support_reviewed = [pid for pid in support_unknown_candidates if pid in reviewed_support_ids]
    update_reviewed = [pid for pid in update_unknown_candidates if pid in reviewed_update_ids]
    support_pending = [pid for pid in support_unknown_candidates if pid not in reviewed_support_ids]
    update_pending = [pid for pid in update_unknown_candidates if pid not in reviewed_update_ids]

    spatial_resolved, spatial_pending = field_coverage(raw, by_id, spatial_resolution_warning)
    coverage_resolved, coverage_pending = field_coverage(raw, by_id, temporal_coverage_warning)
    temporal_resolved, temporal_pending = field_coverage(raw, by_id, temporal_resolution_warning)
    version_resolved, version_pending = field_coverage(raw, by_id, version_warning)

    spatial_total = len(spatial_resolved) + len(spatial_pending)
    coverage_total = len(coverage_resolved) + len(coverage_pending)
    temporal_total = len(temporal_resolved) + len(temporal_pending)
    version_total = len(version_resolved) + len(version_pending)
    support_curated = len(support_resolved) + len(support_reviewed)
    update_curated = len(update_resolved) + len(update_reviewed)

    print(
        "COBERTURA DA NORMALIZAÇÃO PÚBLICA: "
        f"spatial_support {support_curated}/{len(support_ids)} curados "
        f"({len(support_resolved)} classificados + {len(support_reviewed)} desconhecidos revisados; {pct(support_curated, len(support_ids))}%); "
        f"update_frequency {update_curated}/{len(update_ids)} curados "
        f"({len(update_resolved)} classificados + {len(update_reviewed)} desconhecidos revisados; {pct(update_curated, len(update_ids))}%); "
        f"spatial_resolution {len(spatial_resolved)}/{spatial_total} ({pct(len(spatial_resolved), spatial_total)}%); "
        f"temporal_coverage {len(coverage_resolved)}/{coverage_total} ({pct(len(coverage_resolved), coverage_total)}%); "
        f"temporal_resolution {len(temporal_resolved)}/{temporal_total} ({pct(len(temporal_resolved), temporal_total)}%); "
        f"version_or_collection {len(version_resolved)}/{version_total} ({pct(len(version_resolved), version_total)}%)."
    )

    if support_reviewed or update_reviewed:
        print(
            "DESCONHECIDOS REVISADOS: "
            f"spatial_support={len(support_reviewed)}; update_frequency={len(update_reviewed)}"
        )

    if support_pending:
        print("PENDÊNCIAS spatial_support:")
        for pid in support_pending:
            row = raw_by_id[pid]
            print(f"- {pid} | {row.get('product_name','')} | {row.get('spatial_support','')}")
    if update_pending:
        print("PENDÊNCIAS update_frequency:")
        for pid in update_pending:
            row = raw_by_id[pid]
            print(f"- {pid} | {row.get('product_name','')} | {row.get('update_frequency','')}")

    print_pending("spatial_resolution", spatial_pending, raw_by_id, "spatial_resolution")
    print_pending("temporal_coverage", coverage_pending, raw_by_id, "temporal_coverage")
    print_pending("temporal_resolution", temporal_pending, raw_by_id, "temporal_resolution")
    print_pending("version_or_collection", version_pending, raw_by_id, "version_or_collection")


if __name__ == "__main__":
    main()
