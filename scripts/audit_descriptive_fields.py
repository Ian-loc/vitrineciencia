#!/usr/bin/env python3
"""Audita a comparabilidade dos campos descritivos da Vitrine.

O contrato ainda é experimental. Por padrão, esta auditoria quantifica e lista
problemas sem bloquear a publicação. Use --strict quando a migração histórica
estiver concluída e as advertências restantes tiverem sido resolvidas ou
explicitamente aceitas.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "schema" / "descriptive-field-contract-v0.1.json"
SOURCE_CSV = ROOT / "data" / "data_resources.csv"
PRODUCT_CSV = ROOT / "data" / "data_products.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split("|") if item.strip()]


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def add_issue(issues: list[dict[str, str]], entity: str, entity_id: str, field: str, code: str, value: str) -> None:
    issues.append({
        "entity": entity,
        "id": entity_id,
        "field": field,
        "code": code,
        "value": value,
    })


def audit_pipe_list(issues: list[dict[str, str]], entity: str, entity_id: str, field: str, value: str) -> None:
    items = split_pipe(value)
    folded = [norm(item) for item in items]
    if len(folded) != len(set(folded)):
        add_issue(issues, entity, entity_id, field, "duplicate_list_value", value)
    if ";" in value:
        add_issue(issues, entity, entity_id, field, "noncanonical_list_separator", value)


def audit_max_chars(issues: list[dict[str, str]], entity: str, entity_id: str, field: str, value: str, limit: int) -> None:
    if len((value or "").strip()) > limit:
        add_issue(issues, entity, entity_id, field, f"recommended_max_chars_{limit}", value)


def contains_any(value: str, patterns: tuple[str, ...]) -> bool:
    text = norm(value)
    return any(pattern in text for pattern in patterns)


def contains_word(value: str, words: tuple[str, ...]) -> bool:
    text = norm(value)
    return any(re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text) for word in words)


def audit_sources(rows: list[dict[str, str]], issues: list[dict[str, str]]) -> None:
    for row in rows:
        rid = row.get("resource_id", "?")
        audit_max_chars(issues, "source", rid, "official_identity", row.get("official_identity", ""), 160)
        audit_max_chars(issues, "source", rid, "description", row.get("description", ""), 280)
        audit_max_chars(issues, "source", rid, "academic_uses", row.get("academic_uses", ""), 320)
        for field in ("research_areas", "keywords"):
            audit_pipe_list(issues, "source", rid, field, row.get(field, ""))

        geographic = row.get("geographic_coverage", "")
        if contains_any(geographic, ("resolução", "resolucao", "escala cartográfica", "escala cartografica")):
            add_issue(issues, "source", rid, "geographic_coverage", "mixes_coverage_and_resolution", geographic)

        spatial = row.get("spatial_resolution", "")
        if contains_any(spatial, ("atualização", "atualizacao", "frequência", "frequencia", "mensalmente", "anualmente")):
            add_issue(issues, "source", rid, "spatial_resolution", "mixes_spatial_and_update", spatial)

        temporal_coverage = row.get("temporal_coverage", "")
        if contains_any(temporal_coverage, ("atualização diária", "atualizacao diaria", "atualizado diariamente", "frequência de atualização", "frequencia de atualizacao")):
            add_issue(issues, "source", rid, "temporal_coverage", "mixes_coverage_and_update", temporal_coverage)

        temporal_resolution = row.get("temporal_resolution", "")
        if contains_any(temporal_resolution, ("atualizado", "atualizada", "publicado", "publicada", "lançamento", "lancamento")):
            add_issue(issues, "source", rid, "temporal_resolution", "mixes_resolution_and_publication", temporal_resolution)

        access = row.get("access_conditions", "")
        if len(access) > 180 or ". " in access:
            add_issue(issues, "source", rid, "access_conditions", "class_and_note_mixed", access)


def audit_products(rows: list[dict[str, str]], issues: list[dict[str, str]]) -> None:
    temporal_resolution_words = ("diária", "diaria", "mensal", "anual", "semanal", "trimestral")
    for row in rows:
        pid = row.get("product_id", "?")
        audit_max_chars(issues, "product", pid, "product_description", row.get("product_description", ""), 360)
        for field in ("research_areas", "keywords"):
            audit_pipe_list(issues, "product", pid, field, row.get(field, ""))

        spatial_support = row.get("spatial_support", "")
        support_items = split_pipe(spatial_support)
        if len(support_items) >= 3 and contains_any(spatial_support, ("mapa", "tabela", "gráfico", "grafico", "análise", "analise")):
            add_issue(issues, "product", pid, "spatial_support", "support_mixes_unit_and_presentation", spatial_support)

        spatial_resolution = row.get("spatial_resolution", "")
        if contains_word(spatial_resolution, temporal_resolution_words):
            add_issue(issues, "product", pid, "spatial_resolution", "mixes_spatial_and_temporal", spatial_resolution)

        temporal_coverage = row.get("temporal_coverage", "")
        if contains_any(temporal_coverage, ("atualização diária", "atualizacao diaria", "atualizado diariamente", "frequência de atualização", "frequencia de atualizacao")):
            add_issue(issues, "product", pid, "temporal_coverage", "mixes_coverage_and_update", temporal_coverage)

        temporal_resolution = row.get("temporal_resolution", "")
        if contains_any(temporal_resolution, ("atualizado", "publicado", "edição corrente", "edicao corrente")):
            add_issue(issues, "product", pid, "temporal_resolution", "mixes_resolution_and_publication", temporal_resolution)

        update = row.get("update_frequency", "")
        if ";" in update or len(update) > 90:
            add_issue(issues, "product", pid, "update_frequency", "class_and_note_mixed", update)

        version = row.get("version_or_collection", "")
        if contains_any(version, ("auditado em", "acesso auditado", "atualização diária", "atualizacao diaria")):
            add_issue(issues, "product", pid, "version_or_collection", "version_mixes_audit_or_update", version)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="falha se qualquer advertência for encontrada")
    parser.add_argument("--json", action="store_true", help="imprime relatório completo em JSON")
    args = parser.parse_args()

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if contract.get("status") not in {"experimental", "stable"}:
        raise SystemExit("ERRO: estado inválido do contrato descritivo")

    sources = read_csv(SOURCE_CSV)
    products = read_csv(PRODUCT_CSV)
    issues: list[dict[str, str]] = []
    audit_sources(sources, issues)
    audit_products(products, issues)

    counts = Counter((item["entity"], item["field"], item["code"]) for item in issues)
    summary = {
        "contract": contract.get("schema_version"),
        "contract_status": contract.get("status"),
        "sources_audited": len(sources),
        "products_audited": len(products),
        "warnings": len(issues),
        "warning_groups": [
            {"entity": entity, "field": field, "code": code, "count": count}
            for (entity, field, code), count in sorted(counts.items())
        ],
    }

    if args.json:
        print(json.dumps({**summary, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        print(
            "AUDITORIA DESCRITIVA: "
            f"{len(sources)} fontes, {len(products)} produtos, {len(issues)} advertências "
            f"({contract.get('status')})."
        )
        for group in summary["warning_groups"]:
            print(f"- {group['entity']}.{group['field']}: {group['code']} = {group['count']}")
        if issues:
            print("Primeiros registros para revisão:")
            for item in issues[:20]:
                preview = re.sub(r"\s+", " ", item["value"]).strip()
                if len(preview) > 120:
                    preview = preview[:117] + "..."
                print(f"  {item['id']} · {item['field']} · {item['code']} · {preview}")

    if args.strict and issues:
        raise SystemExit(f"ERRO: {len(issues)} advertências descritivas permanecem")


if __name__ == "__main__":
    main()
