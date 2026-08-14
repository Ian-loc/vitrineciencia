#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parent / "validate_source_correction_queues.py"
s = p.read_text(encoding="utf-8")
repls = [
    (
        "EXPECTED_TOTAL_SOURCES = 51\n",
        "BASELINE_SOURCE_COUNT = 51\n",
    ),
    (
        '    if len(canonical_rows) != EXPECTED_TOTAL_SOURCES:\n        fail(f"catálogo canônico deve ter {EXPECTED_TOTAL_SOURCES} fontes, encontrou {len(canonical_rows)}")\n\n    ids = [row["resource_id"] for row in canonical_rows]\n    expected_ids = [f"DR{i:04d}" for i in range(1, EXPECTED_TOTAL_SOURCES + 1)]\n    if ids != expected_ids:\n        fail("ordem/identidade canônica deve permanecer DR0001→DR0051")\n',
        '    if len(canonical_rows) < BASELINE_SOURCE_COUNT:\n        fail(f"catálogo canônico deve preservar ao menos as {BASELINE_SOURCE_COUNT} fontes auditadas; encontrou {len(canonical_rows)}")\n\n    ids = [row["resource_id"] for row in canonical_rows]\n    expected_baseline_ids = [f"DR{i:04d}" for i in range(1, BASELINE_SOURCE_COUNT + 1)]\n    if ids[:BASELINE_SOURCE_COUNT] != expected_baseline_ids:\n        fail("baseline auditado deve permanecer DR0001→DR0051 nas primeiras 51 posições")\n',
    ),
    (
        '    expected_no_change = set(ids) - corrected_sources\n',
        '    expected_no_change = set(expected_baseline_ids) - corrected_sources\n',
    ),
    (
        '    for row in proposed_rows:\n        if row["last_verified"] != AUDIT_DATE:\n            last_verified_changes += 1\n        row["last_verified"] = AUDIT_DATE\n',
        '    for row in proposed_rows[:BASELINE_SOURCE_COUNT]:\n        if row["last_verified"] != AUDIT_DATE:\n            last_verified_changes += 1\n        row["last_verified"] = AUDIT_DATE\n',
    ),
    (
        '    if len(proposed_rows) != EXPECTED_TOTAL_SOURCES:\n        fail("aplicação proposta alterou número de fontes")\n',
        '    if len(proposed_rows) != len(canonical_rows):\n        fail("aplicação proposta alterou número de fontes")\n',
    ),
]
for old, new in repls:
    if old not in s:
        raise SystemExit(f"trecho esperado não encontrado:\n{old}")
    s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
print("validator patched for immutable 51-source audit baseline + uncapped catalog growth")
