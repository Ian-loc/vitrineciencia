#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "data_products.csv"
DISTS = ROOT / "data" / "product_distributions.csv"

product_rows = [
    [
        "DP000108", "DR0073", "Geografia do Brasil — série de estudos geográficos do IBGE", "Geografia do Brasil",
        "Geografia do Brasil", "catalog",
        "Série de estudos geográficos produzida pelo IBGE desde a década de 1950 para interpretar as macrorregiões e as transformações socioespaciais do território brasileiro; a edição mais recente confirmada nesta auditoria é Brasil – uma visão geográfica e ambiental no início do século XXI, publicada em 2016.",
        "Human geography | Environmental geography | Territorial analysis | Socioecological systems",
        "geografia do Brasil | macrorregiões | território | dinâmica socioespacial | ambiente | cidades | espaço rural | IBGE",
        "Brasil; recortes macrorregionais e nacionais conforme edição", "sim",
        "síntese geográfica e publicação por edição", "não se aplica como resolução espacial única",
        "década de 1950–2016 nas edições confirmadas pela página oficial", "por edição histórica", "irregular",
        "ativo", "série histórica; edição mais recente confirmada 2016", "external_index",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15786-brasil-uma-visao-geografica-e-ambiental-no-inicio-do-seculo-xxi.html?lang=pt-BR",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15786-brasil-uma-visao-geografica-e-ambiental-no-inicio-do-seculo-xxi.html?lang=pt-BR",
        "agregador",
        "É uma série de sínteses geográficas e publicações, não um dataset observacional homogêneo. Temas, recortes, fontes e métodos variam entre edições; a edição de 2016 não deve ser tratada como retrato atual do território.",
        "2026-08-15",
    ],
    [
        "DP000109", "DR0052", "Regiões Fitoecológicas e Outras Áreas do Brasil — revisão técnica 2026", "Regiões Fitoecológicas 2026",
        "Macrocaracterização dos Recursos Naturais do Brasil", "map_layer_collection",
        "Revisão técnica publicada pelo IBGE em 20/03/2026 do Mapa de Regiões Fitoecológicas e Outras Áreas do Brasil, regionalizando o território segundo grandes tipos de vegetação e outras áreas representadas na classificação fitogeográfica.",
        "Vegetation science | Biogeography | Ecology | Environmental mapping",
        "regiões fitoecológicas | vegetação | fitogeografia | florestas | formações campestres | macrocaracterização | IBGE",
        "Brasil", "sim", "regiões e outras áreas cartografadas", "escala e precisão devem ser verificadas nos arquivos e metadados da revisão 2026",
        "revisão publicada em 20/03/2026; representa uma regionalização cartográfica, não uma série temporal de cobertura", "por revisão cartográfica", "por revisão; frequência futura não inferida",
        "ativo", "revisão técnica 2026 — divulgada em 20/03/2026", "complete",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "https://www.ibge.gov.br/calendario/geocientificos",
        "derivado",
        "Região fitoecológica é uma regionalização/classificação de vegetação e não deve ser confundida com cobertura e uso da terra observados em uma data específica. A escala e a legenda da revisão 2026 devem ser preservadas no uso analítico.",
        "2026-08-15",
    ],
    [
        "DP000110", "DR0060", "Fauna Ameaçada de Extinção — série cartográfica 2006–2009", "Fauna Ameaçada 2006–2009",
        "Biodiversidade — IBGE", "dataset_series",
        "Série cartográfica histórica do IBGE sobre fauna brasileira ameaçada de extinção, iniciada em 2006 e concluída em 2009 com mapas temáticos por grandes grupos taxonômicos; a edição de 2009 localiza 238 espécies e subespécies de invertebrados aquáticos e peixes com base na lista do Ibama de 2004.",
        "Biodiversity | Conservation biology | Biogeography | Environmental mapping",
        "fauna ameaçada | risco de extinção | IBAMA 2004 | biodiversidade | distribuição geográfica | mapas | IBGE",
        "Brasil", "sim", "distribuição cartográfica de espécies por grupos taxonômicos", "1:5.000.000 na edição 2009; verificar cada mapa da série",
        "série 2006–2009; lista de referência do Ibama 2004 na edição 2009", "por edição/mapa", "série concluída em 2009",
        "arquivado", "série cartográfica 2006–2009; edição final 2009", "complete",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/15810-fauna-ameacada-de-extincao.html",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/15810-fauna-ameacada-de-extincao.html",
        "derivado",
        "Produto histórico baseado em listas de ameaça e fontes disponíveis à época. Não representa o estado atual de ameaça, abundância ou ocorrência das espécies e não deve ser comparado diretamente a avaliações recentes sem harmonização taxonômica e metodológica.",
        "2026-08-15",
    ],
]

dist_rows = [
    [
        "DD000124", "DP000108", "Geografia do Brasil — página da série e acesso à publicação 2016",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15786-brasil-uma-visao-geografica-e-ambiental-no-inicio-do-seculo-xxi.html?lang=pt-BR",
        "publicação digital; formato do arquivo deve ser confirmado no link de acesso", "HTTPS / HTTP download", "navegador web",
        "sim", "não", "consulta pública pela página oficial e acesso à publicação", "licença específica do arquivo não localizada nesta auditoria; observar termos do IBGE", "desconhecido",
        "por edição/publicação", "A página oficial funciona como índice da série e identifica a edição de 2016; não confundir a página agregadora com um dataset único.", "2026-08-15",
    ],
    [
        "DD000125", "DP000109", "Regiões Fitoecológicas e Outras Áreas 2026 — acesso institucional",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "mapa e arquivos geoespaciais associados; formatos devem ser confirmados na edição", "HTTPS / HTTP download", "navegador web",
        "sim", "não", "consulta e downloads públicos pela coleção Macrocaracterização do IBGE", "licença específica dos arquivos não localizada nesta auditoria; observar termos do IBGE", "desconhecido",
        "por edição/produto", "O calendário geocientífico oficial confirma a divulgação em 20/03/2026; formato e escala devem ser lidos nos arquivos/metadados da revisão e não inferidos do calendário.", "2026-08-15",
    ],
    [
        "DD000126", "DP000110", "Fauna Ameaçada de Extinção — downloads e publicações históricas",
        "https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/15810-fauna-ameacada-de-extincao.html",
        "mapas e publicações; formatos variam por edição", "HTTPS / HTTP download", "navegador web",
        "sim", "não", "downloads públicos pela página oficial; acesso organizado por edição", "licença específica dos arquivos não localizada nesta auditoria; observar termos do IBGE", "desconhecido",
        "por edição e grupo taxonômico", "A página oficial mantém downloads da série histórica. A edição 2009 é escala 1:5.000.000 e usa a lista do Ibama de 2004; não interpretar como status contemporâneo.", "2026-08-15",
    ],
]


def existing_ids(path: Path, id_field: str) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return {row[id_field] for row in csv.DictReader(fh)}


def append_rows(path: Path, rows: list[list[str]], id_field: str) -> None:
    current = existing_ids(path, id_field)
    incoming = [row[0] for row in rows]
    collisions = current.intersection(incoming)
    if collisions:
        raise SystemExit(f"ID collision in {path}: {sorted(collisions)}")
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerows(rows)


append_rows(PRODUCTS, product_rows, "product_id")
append_rows(DISTS, dist_rows, "distribution_id")
print("Materialized 3 IBGE products and 3 distributions append-only.")
