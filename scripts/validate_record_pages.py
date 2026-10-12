#!/usr/bin/env python3
"""Valida as páginas públicas renderizadas a partir do public-record-v2."""
from __future__ import annotations

import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
CANONICAL = ROOT / "data" / "data_resources.csv"
PUBLIC_RECORDS = SITE / "data" / "v2" / "public_records.json"
INDIVIDUAL = SITE / "data" / "v2" / "registros"
SCHEMA = ROOT / "schema" / "public-record-v2.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = ""
        self.body_schema = ""
        self.h1 = 0
        self.main = 0
        self.ids: list[str] = []
        self.canonical: list[str] = []
        self.og_url: list[str] = []
        self.title_text = ""
        self.record_sections = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "body":
            self.body_schema = values.get("data-public-record-schema", "")
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if tag == "section" and "record-section" in (values.get("class") or "").split():
            self.record_sections += 1
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "link" and "canonical" in (values.get("rel") or "").split():
            if values.get("href"):
                self.canonical.append(values["href"])
        if tag == "meta" and values.get("property") == "og:url" and values.get("content"):
            self.og_url.append(values["content"])
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text += data


def canonical_ids() -> list[str]:
    with CANONICAL.open(encoding="utf-8-sig", newline="") as handle:
        return [row["resource_id"] for row in csv.DictReader(handle)]


if not PUBLIC_RECORDS.exists():
    fail("data/v2/public_records.json ausente do artefato público")

records = json.loads(PUBLIC_RECORDS.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
ids = canonical_ids()
record_ids = [item.get("record", {}).get("id") for item in records]

if len(records) != len(ids):
    fail(f"public-record-v2: {len(records)} registros; esperado {len(ids)}")
if set(record_ids) != set(ids):
    fail("IDs do public-record-v2 divergem do catálogo canônico")
if len(record_ids) != len(set(record_ids)):
    fail("public-record-v2 contém IDs duplicados")

resource_types = set(schema.get("resource_types", {}))
required_sections = {
    "visao-geral",
    "dados-produtos",
    "acesso",
    "interpretacao",
    "proveniencia-referencias",
    "curadoria",
}
required_labels = (
    "Visão geral",
    "Dados e produtos disponíveis",
    "Como acessar",
    "Como interpretar",
    "Proveniência, condições e referências",
    "Sobre este registro na Vitrine",
)

html_ids: set[str] = set()
json_ids: set[str] = set()
offering_count = 0
distribution_count = 0

for item in records:
    record = item["record"]
    resource = item["resource"]
    rid = record["id"]
    rid_lower = rid.lower()

    if item.get("schema_version") != schema.get("schema_version"):
        fail(f"{rid}: schema_version divergente")
    if resource.get("local_id") == rid:
        fail(f"{rid}: identidade de registro e recurso não está separada")
    if record.get("resource_ref") != resource.get("local_id"):
        fail(f"{rid}: resource_ref não aponta para o recurso")
    if (resource.get("type") or {}).get("id") not in resource_types:
        fail(f"{rid}: tipo de recurso inválido")
    expected_url = f"https://ian-loc.github.io/vitrineciencia/registros/{rid_lower}/"
    if record.get("public_url") != expected_url:
        fail(f"{rid}: URL pública inesperada")

    routes = item.get("access_routes") or []
    resource_routes = [r for r in routes if r.get("target_type") == "resource"]
    if sum(bool(r.get("primary")) for r in resource_routes) != 1:
        fail(f"{rid}: deve existir exatamente uma rota principal no nível do recurso")
    for route in routes:
        route_url = str(route.get("url") or "")
        if route_url and not route_url.startswith("https://"):
            fail(f"{rid}: rota não HTTPS: {route_url}")
        if route.get("target_type") not in {"resource", "offering"}:
            fail(f"{rid}: target_type de rota inválido")
        if not route.get("route_id") or not route.get("target_id"):
            fail(f"{rid}: rota sem identidade/alvo")

    offerings = item.get("offerings") or []
    offering_ids = {o.get("offering_id") for o in offerings}
    offering_count += len(offerings)
    distribution_routes = [r for r in routes if r.get("route_type") == "distribution"]
    distribution_count += len(distribution_routes)
    for route in distribution_routes:
        if route.get("target_id") not in offering_ids:
            fail(f"{rid}: distribuição aponta para offering inexistente: {route.get('target_id')}")

    page = SITE / "registros" / rid_lower / "index.html"
    payload = INDIVIDUAL / f"{rid_lower}.json"
    if not page.exists() or page.stat().st_size == 0:
        fail(f"{rid}: página HTML ausente")
    if not payload.exists() or payload.stat().st_size == 0:
        fail(f"{rid}: JSON v2 individual ausente")
    if json.loads(payload.read_text(encoding="utf-8")) != item:
        fail(f"{rid}: JSON v2 individual diverge do agregado")
    json_ids.add(rid)

    content = page.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(content)

    if parser.lang != "pt-BR":
        fail(f"{rid}: lang deve ser pt-BR")
    if parser.body_schema != "public-record-v2":
        fail(f"{rid}: HTML não declara public-record-v2")
    if parser.h1 != 1 or parser.main != 1:
        fail(f"{rid}: página deve ter um h1 e um main")
    if parser.record_sections != 5:
        fail(f"{rid}: página deve conter exatamente cinco blocos públicos principais")
    if parser.canonical != [expected_url] or parser.og_url != [expected_url]:
        fail(f"{rid}: canonical/og:url divergentes")
    if resource["name"] not in parser.title_text:
        fail(f"{rid}: título HTML não contém o nome do recurso")

    duplicates = {value for value in parser.ids if parser.ids.count(value) > 1}
    if duplicates:
        fail(f"{rid}: IDs HTML duplicados: {sorted(duplicates)}")
    missing = required_sections - set(parser.ids)
    if missing:
        fail(f"{rid}: seções públicas ausentes: {sorted(missing)}")
    for token in required_labels:
        if token not in content:
            fail(f"{rid}: rótulo público obrigatório ausente: {token}")

    if "Tipo público do registro" in content:
        fail(f"{rid}: semântica v1 ainda exposta no HTML")
    if "Produtos, coleções e versões descritos em detalhe" in content:
        fail(f"{rid}: estrutura v1 ainda exposta no HTML")
    if re.search(
        r">\s*(unknown|access role|entity type|source origin|dataset page|CatalogRecord|offering_id|resource_ref)\s*<",
        content,
        flags=re.I,
    ):
        fail(f"{rid}: vocabulário interno exposto")

    html_ids.add(rid)

if html_ids != set(ids) or json_ids != set(ids):
    fail("cobertura HTML/JSON v2 diverge dos IDs canônicos")
if offering_count != 11:
    fail(f"offerings detalhadas nas páginas: {offering_count}; esperado 11")
if distribution_count != 19:
    fail(f"distribuições nas páginas: {distribution_count}; esperado 19")

sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
for item in records:
    if f"<loc>{item['record']['public_url']}</loc>" not in sitemap:
        fail(f"{item['record']['id']}: URL ausente do sitemap")

print(
    f"OK: {len(records)} páginas public-record-v2 em cinco blocos + "
    f"{len(records)} JSONs v2; {offering_count} offerings e "
    f"{distribution_count} distribuições vinculadas; sitemap completo"
)
