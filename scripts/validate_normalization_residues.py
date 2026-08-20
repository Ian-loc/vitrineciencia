#!/usr/bin/env python3
"""Bloqueia regressões silenciosas na normalização pública.

A fila pendente continua exigindo correspondência exata com uma baseline
versionada. Valores que permanecem desconhecidos após revisão explícita são
registrados separadamente, com evidência canônica e justificativa, para não
serem confundidos com resíduos ainda não curados nem forçados a uma classe
mais específica do que a evidência suporta.
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path

import report_normalization_coverage as report

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "schema" / "public-normalization-pending-v0.1.json"
REVIEWED_UNKNOWNS = ROOT / "schema" / "public-normalization-reviewed-unknowns-v0.1.json"
PRODUCT_JSON = ROOT / "data" / "data_products.json"
FIELDS = (
    "spatial_support",
    "update_frequency",
    "spatial_resolution",
    "temporal_coverage",
    "temporal_resolution",
    "version_or_collection",
)
REVIEWABLE_UNKNOWN_VALUES = {
    "spatial_support": "desconhecido",
    "update_frequency": "desconhecida",
}


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text.casefold()).strip()


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


def current_pending() -> tuple[
    dict[str, set[str]], set[str], dict[str, dict], dict[str, dict]
]:
    raw = report.read_csv()
    public = json.loads(PRODUCT_JSON.read_text(encoding="utf-8"))
    raw_by_id = {row["product_id"]: row for row in raw}
    public_by_id = {row["product_id"]: row for row in public}
    valid_ids = set(raw_by_id)

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

    return pending, valid_ids, raw_by_id, public_by_id


def load_reviewed_unknowns(
    raw_by_id: dict[str, dict],
    public_by_id: dict[str, dict],
    pending: dict[str, set[str]],
) -> dict[str, set[str]]:
    payload = json.loads(REVIEWED_UNKNOWNS.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "0.1":
        raise SystemExit("schema_version inesperada em public-normalization-reviewed-unknowns-v0.1.json")
    if payload.get("status") != "stable":
        raise SystemExit("public-normalization-reviewed-unknowns-v0.1.json deve estar stable")
    if not str(payload.get("purpose", "")).strip():
        raise SystemExit("registro de desconhecidos revisados deve declarar purpose")
    unexpected = sorted(set(payload) - {"schema_version", "status", "purpose", "entries"})
    if unexpected:
        raise SystemExit(f"campos inesperados no registro de desconhecidos revisados: {unexpected}")

    entries = payload.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("entries deve ser uma lista em public-normalization-reviewed-unknowns-v0.1.json")

    reviewed = {field: set() for field in FIELDS}
    seen: set[tuple[str, str]] = set()
    today = date.today()

    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit("cada entrada de desconhecido revisado deve ser um objeto")
        field = str(entry.get("field", "")).strip()
        pid = str(entry.get("product_id", "")).strip()
        evidence = str(entry.get("evidence_contains", "")).strip()
        reason = str(entry.get("reason", "")).strip()
        reviewed_at_text = str(entry.get("reviewed_at", "")).strip()

        if field not in REVIEWABLE_UNKNOWN_VALUES:
            raise SystemExit(f"campo não suportado como desconhecido revisado: {field!r}")
        if pid not in raw_by_id or pid not in public_by_id:
            raise SystemExit(f"desconhecido revisado referencia produto inexistente: {pid!r}")
        key = (field, pid)
        if key in seen:
            raise SystemExit(f"desconhecido revisado duplicado: {field}/{pid}")
        seen.add(key)
        if not evidence:
            raise SystemExit(f"desconhecido revisado sem evidence_contains: {field}/{pid}")
        if norm(evidence) not in norm(raw_by_id[pid].get(field, "")):
            raise SystemExit(
                f"evidência do desconhecido revisado não está mais no valor canônico: {field}/{pid}"
            )
        if len(reason) < 24:
            raise SystemExit(f"justificativa insuficiente para desconhecido revisado: {field}/{pid}")
        try:
            reviewed_at = date.fromisoformat(reviewed_at_text)
        except ValueError as exc:
            raise SystemExit(f"reviewed_at inválido para {field}/{pid}: {reviewed_at_text!r}") from exc
        if reviewed_at > today:
            raise SystemExit(f"reviewed_at futuro para {field}/{pid}: {reviewed_at_text}")

        expected_public = REVIEWABLE_UNKNOWN_VALUES[field]
        actual_public = str(public_by_id[pid].get(field, "")).strip()
        if actual_public != expected_public:
            raise SystemExit(
                f"exceção revisada ficou obsoleta: {field}/{pid} agora é {actual_public!r}, "
                f"esperado {expected_public!r}; remova ou revise a exceção"
            )
        if pid not in pending[field]:
            raise SystemExit(
                f"exceção revisada não corresponde mais a um resíduo detectado: {field}/{pid}"
            )
        reviewed[field].add(pid)

    return reviewed


def main() -> None:
    pending, valid_ids, raw_by_id, public_by_id = current_pending()
    reviewed = load_reviewed_unknowns(raw_by_id, public_by_id, pending)

    for field in FIELDS:
        pending[field] -= reviewed[field]

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

    pending_summary = ", ".join(f"{field}={len(pending[field])}" for field in FIELDS)
    reviewed_summary = ", ".join(
        f"{field}={len(reviewed[field])}" for field in FIELDS if reviewed[field]
    ) or "nenhum"
    print(f"OK normalization residue baseline: {pending_summary}")
    print(f"OK reviewed unknown normalization states: {reviewed_summary}")


if __name__ == "__main__":
    main()
