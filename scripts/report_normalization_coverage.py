#!/usr/bin/env python3
"""Mede cobertura da normalização pública e expõe resíduos para curadoria.

Não altera os dados. O relatório distingue problemas históricos do CSV de casos
que já possuem representação pública comparável e lista apenas o que permanece
semanticamente problemático na camada pública.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_CSV = ROOT / "data" / "data_products.csv"
PRODUCT_JSON = ROOT / "data" / "data_products.json"


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
    support_pending = [pid for pid in support_ids if pid not in support_resolved]
    update_pending = [pid for pid in update_ids if pid not in update_resolved]

    spatial_resolved, spatial_pending = field_coverage(raw, by_id, spatial_resolution_warning)
    coverage_resolved, coverage_pending = field_coverage(raw, by_id, temporal_coverage_warning)
    temporal_resolved, temporal_pending = field_coverage(raw, by_id, temporal_resolution_warning)
    version_resolved, version_pending = field_coverage(raw, by_id, version_warning)

    spatial_total = len(spatial_resolved) + len(spatial_pending)
    coverage_total = len(coverage_resolved) + len(coverage_pending)
    temporal_total = len(temporal_resolved) + len(temporal_pending)
    version_total = len(version_resolved) + len(version_pending)

    print(
        "COBERTURA DA NORMALIZAÇÃO PÚBLICA: "
        f"spatial_support {len(support_resolved)}/{len(support_ids)} ({pct(len(support_resolved), len(support_ids))}%); "
        f"update_frequency {len(update_resolved)}/{len(update_ids)} ({pct(len(update_resolved), len(update_ids))}%); "
        f"spatial_resolution {len(spatial_resolved)}/{spatial_total} ({pct(len(spatial_resolved), spatial_total)}%); "
        f"temporal_coverage {len(coverage_resolved)}/{coverage_total} ({pct(len(coverage_resolved), coverage_total)}%); "
        f"temporal_resolution {len(temporal_resolved)}/{temporal_total} ({pct(len(temporal_resolved), temporal_total)}%); "
        f"version_or_collection {len(version_resolved)}/{version_total} ({pct(len(version_resolved), version_total)}%)."
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
