#!/usr/bin/env python3
"""Valida as páginas públicas de registro geradas em _site."""
from __future__ import annotations

import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
CANONICAL = ROOT / "data" / "data_resources.csv"
PUBLIC_RECORDS = SITE / "data" / "public_records.json"
SCHEMA = ROOT / "schema" / "public-record-v1.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = ""
        self.h1 = 0
        self.main = 0
        self.ids: list[str] = []
        self.canonical: list[str] = []
        self.og_url: list[str] = []
        self.title_text = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
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
    fail("data/public_records.json ausente do artefato público")
records = json.loads(PUBLIC_RECORDS.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
ids = canonical_ids()
record_ids = [item.get("resource_id") for item in records]

if len(records) != len(ids):
    fail(f"public_records.json: {len(records)} registros; esperado {len(ids)}")
if set(record_ids) != set(ids):
    fail("IDs de public_records.json divergem do catálogo canônico")
if len(record_ids) != len(set(record_ids)):
    fail("public_records.json contém IDs duplicados")

public_types = set(schema.get("public_record_types", {}))
required_sections = {
    "sobre", "acesso", "conteudos", "cobertura", "produtos",
    "uso-em-pesquisa", "limitacoes", "proveniencia",
    "condicoes-de-uso", "referencias", "curadoria",
}

html_ids: set[str] = set()
json_ids: set[str] = set()
product_count = 0
distribution_count = 0

for record in records:
    rid = record["resource_id"]
    rid_lower = rid.lower()
    if record.get("schema_version") != schema.get("schema_version"):
        fail(f"{rid}: schema_version divergente")
    type_id = (record.get("public_record_type") or {}).get("id")
    if type_id not in public_types:
        fail(f"{rid}: tipo público inválido: {type_id}")
    if record.get("url") != f"https://ian-loc.github.io/vitrineciencia/registros/{rid_lower}/":
        fail(f"{rid}: URL pública inesperada")

    routes = (record.get("access") or {}).get("routes") or []
    if sum(bool(item.get("primary")) for item in routes) != 1:
        fail(f"{rid}: deve existir exatamente uma rota principal")
    for route in routes:
        route_url = str(route.get("url") or "")
        if route_url:
            if not route_url.startswith("https://"):
                fail(f"{rid}: rota não HTTPS: {route.get('url')}")
        elif not (route.get("primary") and route.get("access_class") == "E"):
            fail(f"{rid}: rota sem URL só é permitida para acesso principal E")
        if not route.get("roles"):
            fail(f"{rid}: rota sem papel declarado")
        if not route.get("label"):
            fail(f"{rid}: rota sem rótulo público")

    products = record.get("products") or []
    product_count += len(products)
    distribution_count += sum(len(item.get("distributions") or []) for item in products)

    page = SITE / "registros" / rid_lower / "index.html"
    payload = SITE / "data" / "registros" / f"{rid_lower}.json"
    if not page.exists() or page.stat().st_size == 0:
        fail(f"{rid}: página HTML ausente")
    if not payload.exists() or payload.stat().st_size == 0:
        fail(f"{rid}: JSON individual ausente")

    public_json = json.loads(payload.read_text(encoding="utf-8"))
    if public_json.get("resource_id") != rid:
        fail(f"{rid}: JSON individual pertence a outro registro")
    json_ids.add(rid)

    content = page.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(content)
    if parser.lang != "pt-BR":
        fail(f"{rid}: lang deve ser pt-BR")
    if parser.h1 != 1 or parser.main != 1:
        fail(f"{rid}: página deve ter um h1 e um main")
    expected_url = record["url"]
    if parser.canonical != [expected_url] or parser.og_url != [expected_url]:
        fail(f"{rid}: canonical/og:url divergentes")
    if record["title"] not in parser.title_text:
        fail(f"{rid}: título HTML não contém o nome do registro")
    duplicates = {item for item in parser.ids if parser.ids.count(item) > 1}
    if duplicates:
        fail(f"{rid}: IDs HTML duplicados: {sorted(duplicates)}")
    if not required_sections.issubset(set(parser.ids)):
        missing = sorted(required_sections - set(parser.ids))
        fail(f"{rid}: seções públicas ausentes: {missing}")
    for token in (
        "Sobre este registro", "Como acessar", "O que você encontra aqui",
        "Produtos, coleções e releases", "Cuidados e limitações",
        "Condições de uso e licença", "Curadoria da Vitrine",
    ):
        if token not in content:
            fail(f"{rid}: rótulo público obrigatório ausente: {token}")
    if re.search(r">\s*(unknown|access role|entity type|source origin|dataset page)\s*<", content, flags=re.I):
        fail(f"{rid}: rótulo interno em inglês exposto")
    html_ids.add(rid)

if html_ids != set(ids) or json_ids != set(ids):
    fail("cobertura HTML/JSON diverge dos IDs canônicos")
if product_count != 11:
    fail(f"produtos detalhados nas páginas: {product_count}; esperado 11")
if distribution_count != 19:
    fail(f"distribuições detalhadas nas páginas: {distribution_count}; esperado 19")

sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
for record in records:
    if f"<loc>{record['url']}</loc>" not in sitemap:
        fail(f"{record['resource_id']}: URL ausente do sitemap")

print(
    f"OK: {len(records)} páginas de registro + {len(records)} JSONs individuais; "
    f"{product_count} produtos e {distribution_count} distribuições vinculados; sitemap completo"
)
