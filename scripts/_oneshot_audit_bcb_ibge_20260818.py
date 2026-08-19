#!/usr/bin/env python3
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "data_products.csv"
DISTS = ROOT / "data" / "product_distributions.csv"
TODAY = "2026-08-18"


def parse_line(line):
    return next(csv.reader([line]))


def encode_row(row):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(row)
    return buf.getvalue()


def update_csv_row(path, id_col, id_value, updates):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    header = parse_line(lines[0])
    idx = {name: i for i, name in enumerate(header)}
    found = False
    out = [lines[0]]
    for line in lines[1:]:
        row = parse_line(line.rstrip("\r\n"))
        if row[idx[id_col]] == id_value:
            found = True
            for key, value in updates.items():
                row[idx[key]] = value
            out.append(encode_row(row))
        else:
            out.append(line)
    if not found:
        raise SystemExit(f"missing {id_col}={id_value}")
    path.write_text("".join(out), encoding="utf-8", newline="")


def append_dict_rows(path, rows, id_col):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    header = parse_line(lines[0])
    existing_rows = [parse_line(x) for x in lines[1:] if x]
    existing_ids = {r[header.index(id_col)] for r in existing_rows}
    # Duplicate guard by product page/access URL where available.
    if "product_page_url" in header:
        uidx = header.index("product_page_url")
        existing_urls = {r[uidx] for r in existing_rows if r[uidx]}
        for d in rows:
            if d[id_col] in existing_ids:
                raise SystemExit(f"duplicate id {d[id_col]}")
            if d.get("product_page_url") in existing_urls:
                raise SystemExit(f"duplicate product_page_url {d['product_page_url']}")
    else:
        for d in rows:
            if d[id_col] in existing_ids:
                raise SystemExit(f"duplicate id {d[id_col]}")
    if text and not text.endswith("\n"):
        text += "\n"
    text += "".join(encode_row([d.get(col, "") for col in header]) for d in rows)
    path.write_text(text, encoding="utf-8", newline="")


def max_numeric_id(path, col):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return max(int(r[col][2:]) for r in rows)


# 1) Factually promote PAC 2024 after official IBGE scheduling/publication evidence.
update_csv_row(PRODUCTS, "product_id", "DP000308", {
    "product_name": "Pesquisa Anual de Comércio — 2024",
    "product_acronym": "PAC 2024",
    "temporal_coverage": "ano de referência 2024; série histórica anual",
    "version_or_collection": "edição 2024 — divulgada em 29/07/2026",
    "limitations": "Pesquisa amostral de empresas comerciais formalmente constituídas; não representa comércio informal. A edição 2024 foi divulgada pelo IBGE em 29/07/2026. Comparações exigem observar CNAE, plano tabular, desenho amostral e política de revisão.",
    "last_verified": TODAY,
})
update_csv_row(DISTS, "distribution_id", "DD000329", {
    "distribution_name": "PAC 2024 — SIDRA, tabelas e publicação digital",
    "notes": "Edição 2024 oficialmente divulgada em 29/07/2026; preservar plano tabular, notas metodológicas e política de revisão da pesquisa.",
    "last_verified": TODAY,
})

p0 = max_numeric_id(PRODUCTS, "product_id") + 1
d0 = max_numeric_id(DISTS, "distribution_id") + 1

def pid(n): return f"DP{p0+n:06d}"
def did(n): return f"DD{d0+n:06d}"

new_products = [
{
"product_id": pid(0), "resource_id": "DR0126", "product_name": "Expectativas de Mercado — Sistema Expectativas / Focus", "product_acronym": "Expectativas de Mercado", "product_family": "Expectativas macroeconômicas", "product_kind": "dataset_series",
"product_description": "Estatísticas calculadas a partir das expectativas informadas por instituições participantes do Sistema Expectativas de Mercado para inflação, PIB, produção industrial, câmbio, Selic, variáveis fiscais e setor externo, com recursos por horizonte e indicador.",
"research_areas": "Economics | Finance | Public policy | Data infrastructure", "keywords": "expectativas de mercado | Focus | inflação | PIB | Selic | câmbio | OData | Banco Central", "geographic_coverage": "Brasil; indicadores macroeconômicos nacionais", "covers_brazil": "sim", "spatial_support": "agregações estatísticas por indicador, horizonte e data de referência", "spatial_resolution": "não espacial", "temporal_coverage": "série histórica; início varia por indicador e recurso", "temporal_resolution": "diária nas estatísticas; horizontes mensais, trimestrais, anuais e Selic conforme recurso", "update_frequency": "estatísticas calculadas diariamente; divulgação regular pelo BCB", "product_status": "ativo", "version_or_collection": "conjunto corrente; metadados atualizados em 16/06/2026", "enumeration_scope": "complete", "product_page_url": "https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado", "methodology_url": "https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado", "primary_or_derived": "derivado", "limitations": "Expectativas declaradas por instituições participantes não são previsões oficiais do BCB nem valores realizados. Preservar indicador, horizonte, estatística, data de referência e regras Top 5; a composição de respondentes pode variar.", "last_verified": TODAY,
},
{
"product_id": pid(1), "resource_id": "DR0126", "product_name": "Taxa de juros — Selic — série diária", "product_acronym": "Selic", "product_family": "Política monetária e mercado monetário", "product_kind": "dataset_series",
"product_description": "Série diária da taxa média ajustada das operações compromissadas de um dia útil lastreadas em títulos públicos federais custodiados no Selic, divulgada pelo Banco Central no SGS.",
"research_areas": "Economics | Finance | Public policy | Data infrastructure", "keywords": "Selic | taxa de juros | política monetária | mercado monetário | SGS | Banco Central", "geographic_coverage": "Brasil", "covers_brazil": "sim", "spatial_support": "série temporal nacional", "spatial_resolution": "não espacial", "temporal_coverage": "série diária; início conforme metadados oficiais do SGS", "temporal_resolution": "diária", "update_frequency": "diária", "product_status": "ativo", "version_or_collection": "SGS código 11 — série corrente", "enumeration_scope": "complete", "product_page_url": "https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic", "methodology_url": "https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic", "primary_or_derived": "derivado", "limitations": "A Selic é uma taxa média de operações específicas do mercado monetário e não equivale automaticamente à meta Selic definida pelo Copom, a taxas bancárias ao tomador ou ao custo de capital de agentes específicos. Preservar unidade e convenção temporal da série.", "last_verified": TODAY,
},
{
"product_id": pid(2), "resource_id": "DR0126", "product_name": "Reservas internacionais — conceito caixa — total — diária", "product_acronym": "Reservas — caixa", "product_family": "Setor externo e reservas internacionais", "product_kind": "dataset_series",
"product_description": "Série diária do total de reservas internacionais no conceito caixa, isto é, ativos externos prontamente disponíveis e controlados pelo Banco Central para necessidades do balanço de pagamentos, intervenção cambial e finalidades relacionadas.",
"research_areas": "Economics | Finance | Public policy | Data infrastructure", "keywords": "reservas internacionais | conceito caixa | setor externo | balanço de pagamentos | SGS | Banco Central", "geographic_coverage": "Brasil", "covers_brazil": "sim", "spatial_support": "série temporal nacional", "spatial_resolution": "não espacial", "temporal_coverage": "série histórica diária; período conforme metadados oficiais", "temporal_resolution": "diária", "update_frequency": "diária", "product_status": "ativo", "version_or_collection": "SGS código 13621 — série corrente", "enumeration_scope": "complete", "product_page_url": "https://dadosabertos.bcb.gov.br/dataset/13621-reservas-internacionais---conceito-caixa---total---diaria", "methodology_url": "https://dadosabertos.bcb.gov.br/dataset/13621-reservas-internacionais---conceito-caixa---total---diaria", "primary_or_derived": "derivado", "limitations": "O conceito caixa possui definição própria e não deve ser intercambiado com o conceito liquidez. Variações da série não identificam isoladamente sua causa econômica. Consultas diárias JSON/CSV estão sujeitas aos limites de período documentados pelo BCB.", "last_verified": TODAY,
},
{
"product_id": pid(3), "resource_id": "DR0126", "product_name": "Reservas internacionais — conceito liquidez — total — diária", "product_acronym": "Reservas — liquidez", "product_family": "Setor externo e reservas internacionais", "product_kind": "dataset_series",
"product_description": "Série diária do total de reservas internacionais no conceito liquidez publicada pelo Banco Central, distinta da série no conceito caixa e sujeita à definição metodológica específica do BCB.",
"research_areas": "Economics | Finance | Public policy | Data infrastructure", "keywords": "reservas internacionais | conceito liquidez | setor externo | balanço de pagamentos | SGS | Banco Central", "geographic_coverage": "Brasil", "covers_brazil": "sim", "spatial_support": "série temporal nacional", "spatial_resolution": "não espacial", "temporal_coverage": "série histórica diária; período conforme metadados oficiais", "temporal_resolution": "diária", "update_frequency": "diária", "product_status": "ativo", "version_or_collection": "SGS código 13982 — série corrente", "enumeration_scope": "complete", "product_page_url": "https://dadosabertos.bcb.gov.br/dataset/13982-reservas-internacionais---conceito-liquidez---total---diaria", "methodology_url": "https://dadosabertos.bcb.gov.br/dataset/13982-reservas-internacionais---conceito-liquidez---total---diaria", "primary_or_derived": "derivado", "limitations": "O conceito liquidez não é sinônimo do conceito caixa; selecionar a série coerente com a pergunta analítica. Variações não identificam isoladamente causalidade econômica. Consultas diárias JSON/CSV estão sujeitas aos limites de período documentados pelo BCB.", "last_verified": TODAY,
},
{
"product_id": pid(4), "resource_id": "DR0126", "product_name": "Índice de Atividade Econômica do Banco Central — IBC-Br", "product_acronym": "IBC-Br", "product_family": "Indicadores de atividade econômica", "product_kind": "dataset_series",
"product_description": "Indicador mensal contemporâneo da atividade econômica nacional produzido pelo Banco Central e disponibilizado como série temporal no SGS.",
"research_areas": "Economics | Finance | Public policy | Data infrastructure", "keywords": "IBC-Br | atividade econômica | índice | conjuntura | SGS | Banco Central", "geographic_coverage": "Brasil", "covers_brazil": "sim", "spatial_support": "série temporal nacional", "spatial_resolution": "não espacial", "temporal_coverage": "01/01/2003–presente conforme metadados do conjunto", "temporal_resolution": "mensal", "update_frequency": "mensal", "product_status": "ativo", "version_or_collection": "SGS código 24363 — série corrente; metadados atualizados em 08/04/2026", "enumeration_scope": "complete", "product_page_url": "https://dadosabertos.bcb.gov.br/dataset/24363-indice-de-atividade-economica-do-banco-central---ibc-br", "methodology_url": "https://dadosabertos.bcb.gov.br/dataset/24363-indice-de-atividade-economica-do-banco-central---ibc-br", "primary_or_derived": "derivado", "limitations": "O IBC-Br é indicador de atividade econômica e não deve ser tratado como o próprio PIB ou como estimativa territorial detalhada. Revisões, ajuste sazonal e transformações devem ser preservados conforme a série usada.", "last_verified": TODAY,
},
]
append_dict_rows(PRODUCTS, new_products, "product_id")

new_dists = [
{
"distribution_id": did(0), "product_id": pid(0), "distribution_name": "BCB — Expectativas de Mercado — API/OData", "access_url": "https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado", "format": "API | OData | JSON | CSV | HTML", "access_protocol": "HTTPS | API | OData", "access_tool": "Olinda / Portal de Dados Abertos BCB", "free_download": "sim", "authentication_required": "não", "access_conditions": "acesso público; preservar filtros, horizonte, indicador e documentação do recurso", "license": "Open Data Commons Open Database License (ODbL)", "provider_attribution_required": "sim", "subset_support": "por indicador, horizonte, data de referência e estatística conforme endpoint", "notes": "Inclui recursos mensais, trimestrais, anuais, Selic e Top 5. O serviço de instituições individuais foi desativado por risco de quebra de confidencialidade.", "last_verified": TODAY,
},
{
"distribution_id": did(1), "product_id": pid(1), "distribution_name": "BCB — Taxa Selic — SGS/BCData", "access_url": "https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic", "format": "JSON | CSV | WSDL | HTML", "access_protocol": "HTTPS | API | SGS", "access_tool": "SGS / Portal de Dados Abertos BCB", "free_download": "sim", "authentication_required": "não", "access_conditions": "acesso público; consultas diárias JSON/CSV exigem filtros e respeitam limites documentados", "license": "Open Data Commons Open Database License (ODbL)", "provider_attribution_required": "sim", "subset_support": "por período/data", "notes": "Série SGS código 11. Preservar unidade, convenção temporal e diferença conceitual entre taxa efetiva e meta Selic.", "last_verified": TODAY,
},
{
"distribution_id": did(2), "product_id": pid(2), "distribution_name": "BCB — Reservas internacionais — conceito caixa — SGS/BCData", "access_url": "https://dadosabertos.bcb.gov.br/dataset/13621-reservas-internacionais---conceito-caixa---total---diaria", "format": "JSON | CSV | WSDL | HTML", "access_protocol": "HTTPS | API | SGS", "access_tool": "SGS / Portal de Dados Abertos BCB", "free_download": "sim", "authentication_required": "não", "access_conditions": "acesso público; consultas diárias JSON/CSV exigem filtros e respeitam limites documentados", "license": "Open Data Commons Open Database License (ODbL)", "provider_attribution_required": "sim", "subset_support": "por período/data", "notes": "Série SGS código 13621. Não combinar automaticamente com o conceito liquidez; consultas por período seguem os limites correntes do serviço.", "last_verified": TODAY,
},
{
"distribution_id": did(3), "product_id": pid(3), "distribution_name": "BCB — Reservas internacionais — conceito liquidez — SGS/BCData", "access_url": "https://dadosabertos.bcb.gov.br/dataset/13982-reservas-internacionais---conceito-liquidez---total---diaria", "format": "JSON | CSV | WSDL | HTML", "access_protocol": "HTTPS | API | SGS", "access_tool": "SGS / Portal de Dados Abertos BCB", "free_download": "sim", "authentication_required": "não", "access_conditions": "acesso público; consultas diárias JSON/CSV exigem filtros e respeitam limites documentados", "license": "Open Data Commons Open Database License (ODbL)", "provider_attribution_required": "sim", "subset_support": "por período/data", "notes": "Série SGS código 13982. Preservar a definição específica de liquidez e não substituí-la pela série conceito caixa.", "last_verified": TODAY,
},
{
"distribution_id": did(4), "product_id": pid(4), "distribution_name": "BCB — IBC-Br — SGS/BCData", "access_url": "https://dadosabertos.bcb.gov.br/dataset/24363-indice-de-atividade-economica-do-banco-central---ibc-br", "format": "JSON | CSV | WSDL | HTML", "access_protocol": "HTTPS | API | SGS", "access_tool": "SGS / Portal de Dados Abertos BCB", "free_download": "sim", "authentication_required": "não", "access_conditions": "acesso público; preservar código, unidade e metadados da série", "license": "Open Data Commons Open Database License (ODbL)", "provider_attribution_required": "sim", "subset_support": "por período/data", "notes": "Série SGS código 24363, mensal desde janeiro de 2003. Indicador de atividade econômica; não é o próprio PIB.", "last_verified": TODAY,
},
]
append_dict_rows(DISTS, new_dists, "distribution_id")

print(f"PAC updated; appended products {pid(0)}..{pid(4)} and distributions {did(0)}..{did(4)}")
