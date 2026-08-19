#!/usr/bin/env python3
"""Audita internamente a separação entre página institucional e acesso aos dados.

O resultado é mantido como QA do repositório e não precisa ser exibido na
interface pública da Vitrine. Quando a mesma URL desempenha legitimamente os
dois papéis, a exceção precisa estar documentada em
``data/link_role_exceptions.json``; ela deixa de ser uma pendência sem ocultar
a igualdade dos destinos.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "data_resources.csv"
REPORT_PATH = ROOT / "data" / "link_role_audit.json"
EXCEPTIONS_PATH = ROOT / "data" / "link_role_exceptions.json"
BUILD_META_PATH = ROOT / "data" / "build-meta.json"
BUILD_META_JS_PATH = ROOT / "assets" / "build-meta.js"
METHODOLOGY_PATH = ROOT / "METHODOLOGY.md"
CODEBOOK_PATH = ROOT / "CODEBOOK.md"

REQUIRED_FIELDS = {"resource_id", "resource_name", "homepage_url", "data_access_url"}
EXCEPTION_REQUIRED_FIELDS = {"resource_id", "rationale", "evidence_url", "reviewed_at"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def load_exceptions() -> dict[str, dict[str, str]]:
    if not EXCEPTIONS_PATH.exists():
        return {}
    payload = json.loads(EXCEPTIONS_PATH.read_text(encoding="utf-8"))
    entries = payload.get("reviewed_same_destination", [])
    if not isinstance(entries, list):
        fail("link_role_exceptions.json: reviewed_same_destination deve ser lista")

    by_id: dict[str, dict[str, str]] = {}
    for item in entries:
        if not isinstance(item, dict):
            fail("link_role_exceptions.json contém item que não é objeto")
        missing = EXCEPTION_REQUIRED_FIELDS - set(item)
        if missing:
            fail(f"exceção de link sem campos obrigatórios: {sorted(missing)}")
        resource_id = str(item["resource_id"]).strip()
        if not resource_id:
            fail("exceção de link com resource_id vazio")
        if resource_id in by_id:
            fail(f"exceção de link duplicada para {resource_id}")
        for field in ("rationale", "evidence_url", "reviewed_at"):
            if not str(item[field]).strip():
                fail(f"exceção {resource_id} com {field} vazio")
        by_id[resource_id] = {key: str(value).strip() for key, value in item.items()}
    return by_id


def build_report() -> dict:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not REQUIRED_FIELDS.issubset(fields):
            fail("CSV sem os campos necessários para auditar papéis dos links")
        rows = list(reader)

    exceptions = load_exceptions()
    resource_ids = {row["resource_id"].strip() for row in rows}
    orphan_exceptions = sorted(set(exceptions) - resource_ids)
    if orphan_exceptions:
        fail(f"exceções de link sem fonte correspondente: {orphan_exceptions}")

    records: list[dict[str, str]] = []
    counts = {
        "separate_destinations": 0,
        "same_destination_reviewed_exception": 0,
        "same_destination_pending_review": 0,
        "data_access_not_applicable": 0,
    }

    for row in rows:
        resource_id = row["resource_id"].strip()
        homepage = row["homepage_url"].strip()
        data_access = row["data_access_url"].strip()
        same_destination = (
            data_access != "não se aplica"
            and normalize_url(homepage) == normalize_url(data_access)
        )
        exception = exceptions.get(resource_id)

        if data_access == "não se aplica":
            if exception:
                fail(f"exceção {resource_id} inválida: data_access_url é não se aplica")
            status = "data_access_not_applicable"
        elif same_destination and exception:
            status = "same_destination_reviewed_exception"
        elif same_destination:
            status = "same_destination_pending_review"
        else:
            if exception:
                fail(
                    f"exceção {resource_id} obsoleta: homepage_url e data_access_url já são distintos"
                )
            status = "separate_destinations"

        counts[status] += 1
        record = {
            "resource_id": resource_id,
            "resource_name": row["resource_name"].strip(),
            "status": status,
            "homepage_url": homepage,
            "data_access_url": data_access,
        }
        if exception:
            record.update({
                "exception_rationale": exception["rationale"],
                "exception_evidence_url": exception["evidence_url"],
                "exception_reviewed_at": exception["reviewed_at"],
            })
        records.append(record)

    return {
        "records": len(records),
        "standard": {
            "homepage_url": "Página institucional principal ou página oficial sobre a fonte.",
            "data_access_url": "Página onde os dados podem ser pesquisados, visualizados, solicitados ou baixados.",
            "same_destination": "Pendência de revisão; quando a mesma URL desempenha legitimamente os dois papéis, a exceção deve ser explicitamente documentada e evidenciada.",
            "not_applicable": "Usado quando o recurso não oferece dados para consulta ou download, como software de publicação.",
        },
        "counts": counts,
        "records_requiring_review": [
            record for record in records if record["status"] == "same_destination_pending_review"
        ],
        "reviewed_same_destination_exceptions": [
            record for record in records if record["status"] == "same_destination_reviewed_exception"
        ],
        "interpretation": "A igualdade entre os dois links não prova erro. Casos ainda não inspecionados permanecem pendentes; casos em que a mesma interface cumpre legitimamente os dois papéis são preservados como exceções revisadas com justificativa e evidência.",
    }


def validate_documentation() -> None:
    for path in (BUILD_META_JS_PATH, METHODOLOGY_PATH, CODEBOOK_PATH):
        if not path.exists():
            fail(f"arquivo obrigatório ausente: {path.relative_to(ROOT)}")

    build_meta_js = BUILD_META_JS_PATH.read_text(encoding="utf-8")
    methodology = METHODOLOGY_PATH.read_text(encoding="utf-8")
    codebook = CODEBOOK_PATH.read_text(encoding="utf-8")

    # O indicador permanece disponível para QA interno, mas não é requisito da
    # homepage nem integra o artefato público do GitHub Pages.
    if '"q-link-role-pending":quality.link_role_pending_records' not in build_meta_js:
        fail("assets/build-meta.js não conecta o indicador aos metadados internos do build")
    for token in ("Site oficial", "Acessar dados", "homepage_url", "data_access_url"):
        if token not in methodology or token not in codebook:
            fail(f"regra dos links sem documentação completa: {token}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="atualiza o relatório versionado")
    args = parser.parse_args()

    validate_documentation()
    report = build_report()
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"

    if args.write:
        REPORT_PATH.write_text(serialized, encoding="utf-8")
    elif not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != serialized:
        fail("data/link_role_audit.json diverge do CSV/exceções; execute scripts/audit_link_roles.py --write")

    if BUILD_META_PATH.exists():
        meta = json.loads(BUILD_META_PATH.read_text(encoding="utf-8"))
        quality = meta.setdefault("quality", {})
        quality["link_role_pending_records"] = report["counts"]["same_destination_pending_review"]
        BUILD_META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = report["counts"]
    print(
        "OK: papéis dos links auditados internamente — "
        f"{counts['separate_destinations']} destinos separados; "
        f"{counts['same_destination_reviewed_exception']} URLs iguais revisadas; "
        f"{counts['same_destination_pending_review']} URLs iguais pendentes; "
        f"{counts['data_access_not_applicable']} não aplicáveis"
    )


if __name__ == "__main__":
    main()
