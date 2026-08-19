#!/usr/bin/env python3
"""Validate JSON Schema identity against the canonical Vitrine Ciência URL."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
CANONICAL_BASE = "https://ian-loc.github.io/vitrineciencia/schema/"
LEGACY_TOKENS = ("ScienceDataSourcesCatalog", "EcologyDataCatalog")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> None:
    checked = 0
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: JSON inválido: {exc}")

        schema_id = payload.get("$id")
        if schema_id is None:
            continue
        if not isinstance(schema_id, str) or not schema_id.strip():
            fail(f"{path.relative_to(ROOT)}: $id vazio ou não textual")
        if any(token in schema_id for token in LEGACY_TOKENS):
            fail(f"{path.relative_to(ROOT)}: $id ainda usa identidade legada: {schema_id}")

        expected = CANONICAL_BASE + path.name
        if schema_id != expected:
            fail(
                f"{path.relative_to(ROOT)}: $id não corresponde à URL canônica; "
                f"esperado {expected}, obtido {schema_id}"
            )
        checked += 1

    if checked == 0:
        fail("nenhum JSON Schema com $id encontrado em schema/")
    print(f"OK: {checked} JSON Schemas usam IDs canônicos da Vitrine Ciência")


if __name__ == "__main__":
    main()
