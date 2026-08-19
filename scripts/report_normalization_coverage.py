#!/usr/bin/env python3
"""Mede quanto da fila de advertências já possui classe pública comparável.

Não altera os dados e não considera o texto canônico 'corrigido'. O objetivo é
separar duas perguntas: (1) o registro histórico ainda mistura conceitos? e
(2) a interface já dispõe de uma classe comparável sem apagar o texto original?
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


def support_warning(row: dict[str, str]) -> bool:
    value = row.get("spatial_support", "")
    items = split_pipe(value)
    text = norm(value)
    return len(items) >= 3 and any(token in text for token in ("mapa", "tabela", "gráfico", "grafico", "análise", "analise"))


def update_warning(row: dict[str, str]) -> bool:
    value = row.get("update_frequency", "")
    return ";" in value or len(value) > 90


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

    def pct(done: int, total: int) -> float:
        return round((100 * done / total), 1) if total else 100.0

    print(
        "COBERTURA DA NORMALIZAÇÃO PÚBLICA: "
        f"spatial_support {len(support_resolved)}/{len(support_ids)} ({pct(len(support_resolved), len(support_ids))}%); "
        f"update_frequency {len(update_resolved)}/{len(update_ids)} ({pct(len(update_resolved), len(update_ids))}%)."
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


if __name__ == "__main__":
    main()
