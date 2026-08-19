#!/usr/bin/env python3
"""Build and validate the immutable Vitrine Ciência v1.0.0 Zenodo package."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
PACKAGE_NAME = f"vitrine-ciencia-v{VERSION}"
DIST = ROOT / "dist"
OUT = DIST / PACKAGE_NAME
ZIP_PATH = DIST / f"{PACKAGE_NAME}.zip"

CANONICAL = {
    "data/data_resources.csv": {
        "dest": "data/sources.csv",
        "blob": "6277d8f68a446b3ba71c8778bb52f90c954488e2",
        "rows": 135,
        "id": "resource_id",
        "pattern": r"^DR\d{4}$",
        "entity": "source",
    },
    "data/data_products.csv": {
        "dest": "data/products.csv",
        "blob": "a77dac3e9025cf81299ce244183ea38ee1fe6c65",
        "rows": 843,
        "id": "product_id",
        "pattern": r"^DP\d{6}$",
        "entity": "product",
    },
    "data/product_distributions.csv": {
        "dest": "data/distributions.csv",
        "blob": "c626ac4697aeb2bd009a54e8f05b135375242dcb",
        "rows": 876,
        "id": "distribution_id",
        "pattern": r"^DD\d{6}$",
        "entity": "distribution",
    },
}

DOCUMENTS = {
    "README.md": "README.md",
    "LICENSE": "LICENSE",
    "DATA_LICENSE.md": "LICENSE-DATA.md",
    "CHANGELOG.md": "CHANGELOG.md",
    "CITATION.cff": "CITATION.cff",
    "CODEBOOK.md": "CODEBOOK.md",
    "METHODOLOGY.md": "METHODOLOGY.md",
    "RELEASE_NOTES_v1.0.0.md": "RELEASE_NOTES_v1.0.0.md",
    "FINAL_OBJECTIVES_AND_DOI_GATES.md": "FINAL_OBJECTIVES_AND_DOI_GATES.md",
    "docs/RELEASE_POLICY.md": "docs/RELEASE_POLICY.md",
}

AUXILIARY = {
    "data/brazil_scope_priorities.json": "data/brazil_scope_priorities.json",
    "data/data_quality_report.json": "metadata/data_quality_report.json",
    "schema/product-catalog-v0.1.json": "metadata/product-catalog-v0.1.json",
    "schema/public-discovery-v0.1.json": "metadata/public-discovery-v0.1.json",
}

FIELD_DESCRIPTIONS = {
    "resource_id": "Identificador estável e não reciclado da fonte.",
    "resource_name": "Nome público ou oficial da fonte.",
    "acronym": "Sigla ou nome curto da fonte, quando aplicável.",
    "official_identity": "Identidade institucional ou função oficial sustentada.",
    "description": "Descrição factual concisa da fonte.",
    "homepage_url": "Página institucional ou oficial principal.",
    "data_access_url": "Rota principal para descobrir, consultar ou baixar dados.",
    "research_areas": "Áreas científicas ou temáticas associadas.",
    "keywords": "Palavras-chave para descoberta.",
    "data_product_types": "Tipos gerais de produtos disponibilizados.",
    "data_formats": "Formatos de dados ou arquivos documentados.",
    "visualization_types": "Formas de visualização disponibilizadas.",
    "geographic_coverage": "Abrangência geográfica documentada.",
    "covers_brazil": "Indica se o conteúdo possui cobertura ou aplicação ao Brasil.",
    "spatial_resolution": "Resolução ou granularidade espacial documentada.",
    "temporal_coverage": "Período temporal coberto.",
    "temporal_resolution": "Granularidade temporal dos dados.",
    "data_sources": "Origens empíricas ou institucionais dos dados.",
    "free_download": "Condição geral de download gratuito.",
    "access_conditions": "Restrições, cadastro, solicitação, quota ou outras condições de acesso.",
    "programmatic_access": "Disponibilidade de acesso automatizado.",
    "access_protocols": "Protocolos de acesso, como HTTPS, API, OGC ou STAC.",
    "authentication_required": "Indica necessidade de autenticação.",
    "access_documentation_url": "Documentação técnica do acesso.",
    "license": "Licença ou condição de uso sustentada no nível do registro.",
    "institutional_status": "Natureza institucional da fonte.",
    "owner_or_manager": "Instituição ou unidade responsável.",
    "academic_uses": "Usos científicos, didáticos ou de extensão plausíveis.",
    "limitations": "Limitações e cautelas de interpretação.",
    "academic_evidence_type": "Tipo de evidência acadêmica, técnica ou oficial registrada.",
    "academic_evidence_url": "URL da evidência representativa.",
    "academic_evidence_note": "Nota sobre o que a evidência sustenta.",
    "verification_url": "URL oficial principal usada na verificação.",
    "last_verified": "Data da última revisão efetiva do registro.",
    "product_id": "Identificador estável e não reciclado do produto.",
    "product_name": "Nome do produto científico ou serviço.",
    "product_acronym": "Sigla ou nome curto do produto, quando aplicável.",
    "product_family": "Família temática ou funcional do produto.",
    "product_kind": "Classe controlada do tipo de produto.",
    "product_description": "Descrição factual concisa do produto.",
    "spatial_support": "Unidade ou suporte espacial da informação.",
    "update_frequency": "Frequência de atualização documentada.",
    "product_status": "Estado operacional do produto.",
    "version_or_collection": "Versão, coleção, edição ou estado corrente documentado.",
    "enumeration_scope": "Grau de enumeração do portfólio representado.",
    "product_page_url": "Página oficial do produto.",
    "methodology_url": "Página ou documento de metodologia do produto.",
    "primary_or_derived": "Natureza primária, derivada, agregadora, serviço ou mista.",
    "distribution_id": "Identificador estável e não reciclado da distribuição.",
    "distribution_name": "Nome da forma concreta de acesso ao produto.",
    "access_url": "URL da distribuição ou rota concreta de acesso.",
    "format": "Formato disponibilizado pela distribuição.",
    "access_protocol": "Protocolo usado pela distribuição.",
    "access_tool": "Ferramenta, cliente ou interface usada para acesso.",
    "provider_attribution_required": "Indica exigência de atribuição ao provedor.",
    "subset_support": "Capacidade de selecionar subconjuntos do produto.",
    "notes": "Notas específicas da distribuição.",
}


def fail(message: str) -> None:
    raise SystemExit(f"BLOCKED: {message}")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def copy_file(source: Path, destination: Path) -> None:
    if not source.exists():
        fail(f"required file is missing: {source.relative_to(ROOT)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def write_data_dictionary(headers_by_entity: dict[str, list[str]]) -> None:
    path = OUT / "metadata" / "data_dictionary.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["entity", "field", "required", "key_role", "description"])
        for entity in ("source", "product", "distribution"):
            for field in headers_by_entity[entity]:
                key_role = "none"
                if (entity, field) in {
                    ("source", "resource_id"),
                    ("product", "product_id"),
                    ("distribution", "distribution_id"),
                }:
                    key_role = "primary_key"
                if entity == "product" and field == "resource_id":
                    key_role = "foreign_key:source.resource_id"
                if entity == "distribution" and field == "product_id":
                    key_role = "foreign_key:product.product_id"
                required = "no" if entity == "source" and field in {"acronym", "access_documentation_url"} else "yes"
                writer.writerow([entity, field, required, key_role, FIELD_DESCRIPTIONS.get(field, field.replace("_", " "))])


def write_schema() -> None:
    path = OUT / "metadata" / "schema.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rule_id", "entity", "rule_type", "field", "parent_entity", "parent_field", "constraint"])
        writer.writerows([
            ["S001", "source", "primary_key", "resource_id", "", "", r"^DR\d{4}$"],
            ["S002", "product", "primary_key", "product_id", "", "", r"^DP\d{6}$"],
            ["S003", "distribution", "primary_key", "distribution_id", "", "", r"^DD\d{6}$"],
            ["S004", "product", "foreign_key", "resource_id", "source", "resource_id", "must_exist"],
            ["S005", "distribution", "foreign_key", "product_id", "product", "product_id", "must_exist"],
            ["S006", "source", "snapshot_count", "", "", "", "135"],
            ["S007", "product", "snapshot_count", "", "", "", "843"],
            ["S008", "distribution", "snapshot_count", "", "", "", "876"],
            ["S009", "product", "cardinality", "product_id", "distribution", "product_id", ">=1 distribution per product"],
        ])


def main() -> None:
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if not re.search(r'^version:\s*["\']?1\.0\.0["\']?\s*$', citation, flags=re.MULTILINE):
        fail("CITATION.cff does not declare version 1.0.0")

    source_commit = git("rev-parse", "HEAD")
    if OUT.exists():
        shutil.rmtree(OUT)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    (OUT / "data").mkdir(parents=True)
    (OUT / "metadata").mkdir(parents=True)

    validation: dict[str, object] = {
        "status": "PASS",
        "version": VERSION,
        "source_commit": source_commit,
        "checks": {},
        "relationships": {},
    }
    headers_by_entity: dict[str, list[str]] = {}
    row_sets: dict[str, list[dict[str, str]]] = {}
    provenance_rows: list[list[object]] = []

    for source_rel, meta in CANONICAL.items():
        source = ROOT / source_rel
        destination = OUT / str(meta["dest"])
        copy_file(source, destination)
        headers, rows = read_csv(destination)
        headers_by_entity[str(meta["entity"])] = headers
        row_sets[str(meta["entity"])] = rows
        ids = [row[str(meta["id"])] for row in rows]
        blob = git_blob_sha(destination)
        checks = {
            "records": len(rows),
            "expected_records": meta["rows"],
            "git_blob_sha": blob,
            "expected_git_blob_sha": meta["blob"],
            "unique_ids": len(ids) == len(set(ids)),
            "id_pattern_ok": all(re.fullmatch(str(meta["pattern"]), value or "") for value in ids),
        }
        if not all([
            checks["records"] == checks["expected_records"],
            checks["git_blob_sha"] == checks["expected_git_blob_sha"],
            checks["unique_ids"],
            checks["id_pattern_ok"],
        ]):
            validation["status"] = "FAIL"
        validation["checks"][str(meta["dest"])] = checks  # type: ignore[index]
        provenance_rows.append([
            meta["dest"],
            "https://github.com/Ian-loc/vitrineciencia",
            source_rel,
            source_commit,
            blob,
            destination.stat().st_size,
            "renamed only; byte-identical",
            "2026-08-19",
        ])

    sources = row_sets["source"]
    products = row_sets["product"]
    distributions = row_sets["distribution"]
    source_ids = {row["resource_id"] for row in sources}
    product_ids = {row["product_id"] for row in products}
    distribution_product_ids = {row["product_id"] for row in distributions}
    relationships = {
        "all_products_reference_existing_source": all(row["resource_id"] in source_ids for row in products),
        "all_distributions_reference_existing_product": all(row["product_id"] in product_ids for row in distributions),
        "every_product_has_at_least_one_distribution": product_ids <= distribution_product_ids,
    }
    validation["relationships"] = relationships
    if not all(relationships.values()):
        validation["status"] = "FAIL"

    for source_rel, destination_rel in DOCUMENTS.items():
        copy_file(ROOT / source_rel, OUT / destination_rel)
    for source_rel, destination_rel in AUXILIARY.items():
        copy_file(ROOT / source_rel, OUT / destination_rel)

    write_data_dictionary(headers_by_entity)
    write_schema()

    with (OUT / "metadata" / "provenance.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "package_path", "source_repository", "source_path", "source_commit",
            "source_blob_sha", "source_size_bytes", "transformation", "snapshot_date",
        ])
        writer.writerows(provenance_rows)

    (OUT / "metadata" / "source_commit.txt").write_text(source_commit + "\n", encoding="utf-8")
    (OUT / "metadata" / "validation_report.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest_rows: list[list[object]] = []
    for path in sorted(item for item in OUT.rglob("*") if item.is_file() and item.name != "manifest.csv"):
        manifest_rows.append([path.relative_to(OUT).as_posix(), path.stat().st_size, sha256(path)])
    with (OUT / "metadata" / "manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "size_bytes", "sha256"])
        writer.writerows(manifest_rows)

    if validation["status"] != "PASS":
        fail("package validation failed; ZIP not created")

    DIST.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in OUT.rglob("*") if item.is_file()):
            archive.write(path, path.relative_to(DIST).as_posix())

    print(json.dumps({
        "status": "PASS",
        "version": VERSION,
        "source_commit": source_commit,
        "sources": len(sources),
        "products": len(products),
        "distributions": len(distributions),
        "package": str(OUT.relative_to(ROOT)),
        "zip": str(ZIP_PATH.relative_to(ROOT)),
        "zip_sha256": sha256(ZIP_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
