#!/usr/bin/env python3
"""Gera a camada pública concentrada e comparável da Vitrine Ciência.

A camada canônica permanece intacta. Os JSONs usados pela interface recebem:
- áreas públicas amplas e controladas;
- cópia das áreas detalhadas originais;
- classe normalizada de suporte espacial;
- classe normalizada de frequência de atualização;
- cópia dos textos descritivos originais para rastreabilidade.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "public-discovery-v0.1.json"
SOURCE_JSON = ROOT / "data" / "data_resources.json"
PRODUCT_JSON = ROOT / "data" / "data_products.json"


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text.casefold()).strip()


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split("|") if item.strip()]


def join_ordered(values: list[str], allowed_order: list[str]) -> str:
    seen = set(values)
    return " | ".join(item for item in allowed_order if item in seen)


def source_public_areas(value: str, schema: dict) -> list[str]:
    mapping = schema["source_area_groups"]
    broad = [mapping[item] for item in split_pipe(value) if item in mapping]
    return list(dict.fromkeys(broad))


def product_public_areas(product_value: str, source_value: str, schema: dict) -> list[str]:
    text = norm(product_value)
    matched: list[str] = []
    for area in schema["public_research_areas"]:
        terms = schema["product_area_terms"].get(area, [])
        if any(norm(term) in text for term in terms):
            matched.append(area)
    if not matched:
        matched = source_public_areas(source_value, schema)
    # Evita transformar cartões em listas extensas; até três eixos amplos são suficientes
    # para descoberta. Os termos detalhados continuam preservados separadamente.
    return matched[:3]


# Regras deliberadamente sem termos de apresentação como mapa, gráfico, tabela,
# prancha ou publicação. Esses termos descrevem a forma de apresentação, não o
# suporte espacial da informação.
SPATIAL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("ponto", ("ponto", "point", "coordenad")),
    ("estação ou local", ("estacao", "station", "posto de monitoramento", "local de monitoramento")),
    ("unidade amostral", ("parcela", "plot", "unidade amostral", "sample unit", "amostra")),
    ("célula raster", ("celula raster", "pixel", "raster")),
    ("grade", ("grade", "grid")),
    ("linha ou transecto", ("transect", "transecto", "trajeto", "linha amostral")),
    ("unidade administrativa", (
        "municipio", "municipal", "setor censitario", "distrito", "unidade federativa",
        "unidades da federacao", " uf ", "estado", "pais"
    )),
    ("região ou zona", (
        "regiao", "regional", "bioma", "zona", "area de estudo", "recorte territorial",
        "recortes territoriais", "agregacao territorial", "agregacoes territoriais",
        "unidades geomorfologicas", "unidade geomorfologica", "unidades de relevo",
        "unidades de vegetacao", "unidade de vegetacao", "unidades de solos", "unidade de solo",
        "recorte costeiro", "recortes costeiros", "recorte oceanico", "recortes oceanicos",
        "terra indigena", "terras indigenas", "unidade de conservacao", "unidades de conservacao",
        "area protegida", "areas protegidas"
    )),
    ("bacia ou corpo d'água", ("bacia", "curso d'agua", "corpo d'agua", "rio", "reservatorio", "lago", "hidrograf")),
    ("polígono ou feição", ("poligono", "polygon", "feicao", "imovel", "limite cadastral")),
    ("registro tabular sem geometria", ("sem geometria", "registro tabular", "registro cadastral")),
]


def spatial_support_classes(value: str, schema: dict) -> str:
    text = f" {norm(value)} "
    if "nao se aplica" in text:
        return "não se aplica"
    matched: list[str] = []
    for label, terms in SPATIAL_RULES:
        if any(term in text for term in terms):
            matched.append(label)
    if not matched and any(term in text for term in ("varia conforme", "dependente", "definida por", "conforme o produto", "conforme a camada")):
        matched.append("variável por produto")
    if not matched:
        matched.append("desconhecido")
    allowed = schema["spatial_support_classes"]
    invalid = [item for item in matched if item not in allowed]
    if invalid:
        raise SystemExit(f"ERRO: classe espacial inválida: {invalid}")
    return join_ordered(matched, allowed)


UPDATE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("quase em tempo real", ("quase em tempo real", "near real time", "near-real-time")),
    ("tempo real", ("tempo real", "real time", "real-time")),
    ("contínua", ("continua", "continuamente", "continuous")),
    ("diária", ("diaria", "diariamente", "daily")),
    ("semanal", ("semanal", "weekly")),
    ("mensal", ("mensal", "monthly")),
    ("trimestral", ("trimestral", "quarterly")),
    ("semestral", ("semestral", "semiannual", "semi-annual")),
    ("anual", ("anual", "anualmente", "annual")),
    ("plurianual", ("bienal", "bianual", "quinquenal", "decenal", "a cada dois anos", "a cada cinco anos", "cinco anos", "ten-year")),
    ("por edição ou evento", (
        "por edicao", "edicao especifica", "por evento", "por campanha", "por ciclo", "censitaria",
        "ano-base", "eventual", "por divulgacao", "por publicacao", "por levantamento", "por censo"
    )),
    ("sob demanda", ("sob demanda", "on demand")),
    ("irregular", ("irregular", "nao uniforme", "não uniforme")),
]


def update_frequency_class(value: str, schema: dict) -> str:
    text = norm(value)
    if "nao se aplica" in text:
        return "não se aplica"
    if any(term in text for term in ("sem atualizacao", "sem nova edicao")):
        return "sem atualização prevista"
    found: list[str] = []
    for label, terms in UPDATE_RULES:
        if any(norm(term) in text for term in terms):
            found.append(label)
    found = list(dict.fromkeys(found))
    if len(found) > 1:
        result = "múltipla"
    elif found:
        result = found[0]
    elif "periodic" in text or "periodica" in text or "periodico" in text:
        result = "periódica não especificada"
    elif any(term in text for term in ("nao definida", "sem periodicidade", "desconhecid", "nao inferida")):
        result = "desconhecida"
    else:
        result = "desconhecida"
    if result not in schema["update_frequency_classes"]:
        raise SystemExit(f"ERRO: classe de atualização inválida: {result}")
    return result


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if schema.get("status") != "stable":
        raise SystemExit("ERRO: public-discovery-v0.1 deve estar stable")

    sources = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    products = json.loads(PRODUCT_JSON.read_text(encoding="utf-8"))
    source_by_id = {source["resource_id"]: source for source in sources}

    for source in sources:
        detail = source.get("research_areas", "")
        grouped = source_public_areas(detail, schema)
        if not grouped:
            raise SystemExit(f"ERRO: fonte sem área pública: {source.get('resource_id')}")
        source["research_areas_detail"] = detail
        source["research_areas"] = " | ".join(grouped)

    for product in products:
        source = source_by_id.get(product.get("resource_id"))
        if source is None:
            raise SystemExit(f"ERRO: produto sem fonte durante classificação pública: {product.get('product_id')}")
        source_detail = source.get("research_areas_detail", source.get("research_areas", ""))
        area_detail = product.get("research_areas", "")
        grouped = product_public_areas(area_detail, source_detail, schema)
        if not grouped:
            raise SystemExit(f"ERRO: produto sem área pública: {product.get('product_id')}")

        product["research_areas_detail"] = area_detail
        product["research_areas"] = " | ".join(grouped)

        raw_support = product.get("spatial_support", "")
        product["spatial_support_detail"] = raw_support
        product["spatial_support"] = spatial_support_classes(raw_support, schema)

        raw_update = product.get("update_frequency", "")
        product["update_frequency_detail"] = raw_update
        product["update_frequency"] = update_frequency_class(raw_update, schema)

    SOURCE_JSON.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRODUCT_JSON.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    area_counts = Counter(area for product in products for area in split_pipe(product["research_areas"]))
    support_counts = Counter(product["spatial_support"] for product in products)
    update_counts = Counter(product["update_frequency"] for product in products)

    print(
        "OK: camada pública concentrada gerada — "
        f"{len(schema['public_research_areas'])} áreas amplas; "
        f"{len(products)} produtos com suporte e atualização normalizados."
    )
    print("Áreas públicas:")
    for area in schema["public_research_areas"]:
        print(f"- {area}: {area_counts.get(area, 0)}")
    print(f"Suporte desconhecido: {support_counts.get('desconhecido', 0)}")
    print(f"Atualização desconhecida: {update_counts.get('desconhecida', 0)}")


if __name__ == "__main__":
    main()
