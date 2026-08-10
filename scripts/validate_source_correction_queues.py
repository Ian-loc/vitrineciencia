#!/usr/bin/env python3
"""Cross-audit source correction queues and materialize a proposed CSV safely.

The script is read-only with respect to the canonical catalog. By default it only
validates the queues. ``--output`` may write a proposed CSV to another path; the
canonical ``data/data_resources.csv`` is never overwritten by this script.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "data_resources.csv"
QUEUE_GLOB = "VITRINE_SOURCE_CORRECTION_QUEUE_DR*_2026-08-10.csv"
QUEUE_DIR = ROOT / "docs" / "audits"
OVERRIDES = ROOT / "config" / "source_correction_overrides_2026-08-10.json"
AUDIT_DATE = "2026-08-10"
EXPECTED_QUEUE_FILES = 8
EXPECTED_CORRECTIONS = 119
EXPECTED_CORRECTED_SOURCES = 43
EXPECTED_TOTAL_SOURCES = 51
EXPECTED_COLUMNS = 34
EXPECTED_NO_CHANGE_SOURCES = {
    "DR0001", "DR0004", "DR0007", "DR0009",
    "DR0014", "DR0029", "DR0035", "DR0039",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def queue_decision(row: dict[str, str]) -> str:
    decision = (row.get("decision") or "").strip()
    if decision:
        return decision
    status = (row.get("status") or "").strip()
    if status == "READY":
        return "apply"
    return status


def load_overrides() -> dict[str, str]:
    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        fail("arquivo de overrides deve ser objeto string→string")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="write proposed corrected CSV outside the canonical path")
    parser.add_argument("--summary-json", type=Path, help="write machine-readable validation summary")
    args = parser.parse_args()

    header, canonical_rows = read_csv(CANONICAL)
    if len(header) != EXPECTED_COLUMNS:
        fail(f"catálogo canônico deve ter {EXPECTED_COLUMNS} colunas, encontrou {len(header)}")
    if len(canonical_rows) != EXPECTED_TOTAL_SOURCES:
        fail(f"catálogo canônico deve ter {EXPECTED_TOTAL_SOURCES} fontes, encontrou {len(canonical_rows)}")

    ids = [row["resource_id"] for row in canonical_rows]
    expected_ids = [f"DR{i:04d}" for i in range(1, EXPECTED_TOTAL_SOURCES + 1)]
    if ids != expected_ids:
        fail("ordem/identidade canônica deve permanecer DR0001→DR0051")
    if len(set(ids)) != len(ids):
        fail("resource_id duplicado no catálogo canônico")

    index = {row["resource_id"]: row for row in canonical_rows}
    queue_paths = sorted(QUEUE_DIR.glob(QUEUE_GLOB))
    if len(queue_paths) != EXPECTED_QUEUE_FILES:
        fail(f"esperadas {EXPECTED_QUEUE_FILES} filas, encontradas {len(queue_paths)}")

    overrides = load_overrides()
    seen_keys: set[str] = set()
    corrections: list[dict[str, str]] = []
    explicit_no_change_sources: set[str] = set()

    for path in queue_paths:
        _, rows = read_csv(path)
        for line_number, row in enumerate(rows, start=2):
            resource_id = (row.get("resource_id") or "").strip()
            if resource_id not in index:
                fail(f"{path.name}:{line_number}: resource_id inexistente: {resource_id}")

            decision = queue_decision(row)
            field = (row.get("field") or "").strip()
            if decision == "no_change" or not field:
                if decision != "no_change":
                    fail(f"{path.name}:{line_number}: campo vazio sem decisão no_change")
                explicit_no_change_sources.add(resource_id)
                continue

            if decision not in {"apply", "apply_after_exact_row_check"}:
                fail(f"{path.name}:{line_number}: decisão não aplicável: {decision}")
            if field not in header:
                fail(f"{path.name}:{line_number}: campo fora do contrato canônico: {field}")
            if field in {"resource_id", "last_verified"}:
                fail(f"{path.name}:{line_number}: {field} não pode ser alterado por fila factual")

            key = f"{resource_id}|{field}"
            if key in seen_keys:
                fail(f"correção duplicada para {key}")
            seen_keys.add(key)

            current_value = row.get("current_value") or ""
            actual_value = index[resource_id][field]
            if current_value != actual_value:
                fail(
                    f"{path.name}:{line_number}: current_value diverge de main para {key}: "
                    f"fila={current_value!r}, main={actual_value!r}"
                )

            evidence_url = (row.get("evidence_url") or "").strip()
            if not is_https(evidence_url):
                fail(f"{path.name}:{line_number}: evidence_url deve ser HTTPS para {key}")

            candidate = overrides.get(key, row.get("candidate_value") or "")
            if candidate == actual_value:
                fail(f"{path.name}:{line_number}: candidato não altera {key}")
            if not candidate.strip():
                fail(f"{path.name}:{line_number}: candidato vazio para {key}")

            corrections.append({
                "resource_id": resource_id,
                "field": field,
                "current_value": actual_value,
                "candidate_value": candidate,
                "evidence_url": evidence_url,
                "queue_file": path.name,
            })

    if len(corrections) != EXPECTED_CORRECTIONS:
        fail(f"esperadas {EXPECTED_CORRECTIONS} correções, encontradas {len(corrections)}")

    corrected_sources = {item["resource_id"] for item in corrections}
    if len(corrected_sources) != EXPECTED_CORRECTED_SOURCES:
        fail(
            f"esperadas correções em {EXPECTED_CORRECTED_SOURCES} fontes, "
            f"encontradas {len(corrected_sources)}"
        )

    expected_no_change = set(ids) - corrected_sources
    if expected_no_change != EXPECTED_NO_CHANGE_SOURCES:
        fail(
            "complemento das fontes corrigidas não corresponde ao baseline sem correção: "
            f"esperado={sorted(EXPECTED_NO_CHANGE_SOURCES)}, observado={sorted(expected_no_change)}"
        )
    if not explicit_no_change_sources.issubset(EXPECTED_NO_CHANGE_SOURCES):
        fail(
            "fila marcou no_change para fonte que possui correção: "
            f"{sorted(explicit_no_change_sources - EXPECTED_NO_CHANGE_SOURCES)}"
        )

    unused_overrides = sorted(set(overrides) - seen_keys)
    if unused_overrides:
        fail("overrides sem correção correspondente: " + ", ".join(unused_overrides))

    proposed_rows = [dict(row) for row in canonical_rows]
    proposed_index = {row["resource_id"]: row for row in proposed_rows}
    for item in corrections:
        proposed_index[item["resource_id"]][item["field"]] = item["candidate_value"]

    last_verified_changes = 0
    for row in proposed_rows:
        if row["last_verified"] != AUDIT_DATE:
            last_verified_changes += 1
        row["last_verified"] = AUDIT_DATE

    if [row["resource_id"] for row in proposed_rows] != ids:
        fail("aplicação proposta alterou ordem/identidade das fontes")
    if len(proposed_rows) != EXPECTED_TOTAL_SOURCES:
        fail("aplicação proposta alterou número de fontes")

    url_fields = {"homepage_url", "data_access_url", "access_documentation_url", "verification_url"}
    enum_fields = {
        "free_download": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
        "programmatic_access": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
        "authentication_required": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
    }
    for item in corrections:
        if item["field"] in url_fields and item["candidate_value"] != "não se aplica" and not is_https(item["candidate_value"]):
            fail(f"candidato de URL deve ser HTTPS: {item['resource_id']}|{item['field']}")
        allowed = enum_fields.get(item["field"])
        if allowed and item["candidate_value"] not in allowed:
            fail(f"valor enum inválido em {item['resource_id']}|{item['field']}: {item['candidate_value']}")

    date.fromisoformat(AUDIT_DATE)
    total_cell_changes = len(corrections) + last_verified_changes
    field_counts = Counter(item["field"] for item in corrections)

    summary = {
        "audit_date": AUDIT_DATE,
        "canonical_sources": len(canonical_rows),
        "canonical_columns": len(header),
        "queue_files": [path.name for path in queue_paths],
        "correction_count": len(corrections),
        "corrected_source_count": len(corrected_sources),
        "no_change_source_count": len(EXPECTED_NO_CHANGE_SOURCES),
        "no_change_sources": sorted(EXPECTED_NO_CHANGE_SOURCES),
        "explicit_no_change_sources": sorted(explicit_no_change_sources),
        "last_verified_changes": last_verified_changes,
        "total_cell_changes": total_cell_changes,
        "field_counts": dict(sorted(field_counts.items())),
        "normalization_overrides": overrides,
        "source_ids_preserved": True,
        "row_count_preserved": True,
        "schema_preserved": True,
    }

    if args.output:
        output = args.output.resolve()
        if output == CANONICAL.resolve():
            fail("este validador nunca sobrescreve data/data_resources.csv")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
            writer.writeheader()
            writer.writerows(proposed_rows)

    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "OK: correction queues cross-audited — "
        f"{len(corrections)} corrections / {len(corrected_sources)} sources / "
        f"{last_verified_changes} last_verified updates / {total_cell_changes} total cell changes"
    )


if __name__ == "__main__":
    main()
