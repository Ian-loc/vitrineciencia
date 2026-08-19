#!/usr/bin/env python3
from __future__ import annotations

import csv, io, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TODAY = "2026-08-19"

RESOURCE_FIELDS = ["resource_id","resource_name","acronym","official_identity","description","homepage_url","data_access_url","research_areas","keywords","data_product_types","data_formats","visualization_types","geographic_coverage","covers_brazil","spatial_resolution","temporal_coverage","temporal_resolution","data_sources","free_download","access_conditions","programmatic_access","access_protocols","authentication_required","access_documentation_url","license","institutional_status","owner_or_manager","academic_uses","limitations","academic_evidence_type","academic_evidence_url","academic_evidence_note","verification_url","last_verified"]
PRODUCT_FIELDS = ["product_id","resource_id","product_name","product_acronym","product_family","product_kind","product_description","research_areas","keywords","geographic_coverage","covers_brazil","spatial_support","spatial_resolution","temporal_coverage","temporal_resolution","update_frequency","product_status","version_or_collection","enumeration_scope","product_page_url","methodology_url","primary_or_derived","limitations","last_verified"]
DIST_FIELDS = ["distribution_id","product_id","distribution_name","access_url","format","access_protocol","access_tool","free_download","authentication_required","access_conditions","license","provider_attribution_required","subset_support","notes","last_verified"]


def read_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def append_rows(path: Path, fields, rows):
    if not rows:
        return
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if list(reader.fieldnames or []) != fields:
            raise SystemExit(f"header mismatch: {path}")
    sio = io.StringIO(newline="")
    w = csv.DictWriter(sio, fieldnames=fields, lineterminator="\n")
    for row in rows:
        if set(row) != set(fields):
            missing=set(fields)-set(row); extra=set(row)-set(fields)
            raise SystemExit(f"row schema mismatch {path}: missing={missing} extra={extra}")
        w.writerow(row)
    raw = path.read_bytes()
    prefix = b"" if not raw or raw.endswith(b"\n") else b"\n"
    with path.open("ab") as f:
        f.write(prefix + sio.getvalue().encode("utf-8"))


def next_id(rows, key, prefix, width):
    m = max(int(re.fullmatch(prefix + r"(\d+)", r[key]).group(1)) for r in rows)
    return f"{prefix}{m+1:0{width}d}"

resources_path = DATA / "data_resources.csv"
products_path = DATA / "data_products.csv"
dists_path = DATA / "product_distributions.csv"
resources = read_rows(resources_path)
products = read_rows(products_path)
dists = read_rows(dists_path)

existing_source_names = {r["resource_name"].casefold() for r in resources}
existing_product_urls = {r["product_page_url"].rstrip("/").casefold() for r in products}

new_sources = []
source_ids = {}

if "mapa das organizações da sociedade civil — ipea".casefold() not in existing_source_names:
    rid = next_id(resources + new_sources, "resource_id", "DR", 4)
    source_ids["mosc"] = rid
    new_sources.append({
        "resource_id": rid,
        "resource_name": "Mapa das Organizações da Sociedade Civil — Ipea",
        "acronym": "Mapa das OSC / MOSC",
        "official_identity": "Instituto de Pesquisa Econômica Aplicada — Mapa das Organizações da Sociedade Civil",
        "description": "Plataforma pública colaborativa para dados, microdados, indicadores e informações sobre organizações da sociedade civil brasileiras, suas características, projetos, recursos e participação social.",
        "homepage_url": "https://mapaosc.ipea.gov.br/",
        "data_access_url": "https://mapaosc.ipea.gov.br/base-dados",
        "research_areas": "Planejamento Territorial e Políticas Públicas | Infraestruturas e Ciência de Dados",
        "keywords": "organizações da sociedade civil | OSC | terceiro setor | associações | fundações | participação social | recursos públicos | Ipea",
        "data_product_types": "microdados | cadastros | projetos | indicadores | API | análises",
        "data_formats": "CSV | XLSX | XLS | ZIP | JSON | visualização web",
        "visualization_types": "mapa | tabelas | indicadores | painéis | perfis organizacionais",
        "geographic_coverage": "Brasil — organizações da sociedade civil em todo o território nacional",
        "covers_brazil": "sim",
        "spatial_resolution": "organização/CNPJ e recortes territoriais agregados conforme produto",
        "temporal_coverage": "cadastros e séries históricas; base principal corrente com coleta agosto/2026",
        "temporal_resolution": "registro | mensal | anual | conforme produto",
        "data_sources": "Receita Federal/CNPJ | RAIS | CNIS | CEBAS | SIAFI | bases públicas oficiais | informações autodeclaradas pelas OSCs",
        "free_download": "sim",
        "access_conditions": "downloads públicos e consultas web; conteúdos públicos podem ser republicados/divulgados com citação conforme Termos de Uso; uso comercial dos conteúdos hospedados é proibido",
        "programmatic_access": "sim",
        "access_protocols": "HTTPS | REST API | downloads de arquivos",
        "authentication_required": "não",
        "access_documentation_url": "https://mapaosc.ipea.gov.br/api/api/documentation",
        "license": "Termos de Uso MOSC versão 2025/03/20: republicação/divulgação de conteúdo público permitida com fonte, título, autor e data de acesso; uso comercial dos conteúdos hospedados proibido",
        "institutional_status": "público",
        "owner_or_manager": "Instituto de Pesquisa Econômica Aplicada — Ipea",
        "academic_uses": "Pesquisa sobre terceiro setor, organizações sociais, participação social, mercado de trabalho nas OSCs, financiamento público, redes territoriais, transparência e políticas públicas.",
        "limitations": "A base combina registros administrativos de múltiplas fontes e informações autodeclaradas. Situação cadastral, completude e atualidade variam por campo e organização; presença no Mapa não comprova atividade substantiva, qualidade, regularidade ou impacto da OSC.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://mapaosc.ipea.gov.br/metodologia",
        "academic_evidence_note": "A metodologia oficial documenta critérios de identificação das OSCs, fontes administrativas, autodeclaração, limpeza dos dados e limitações analíticas; a página de bases disponibiliza microdados e dicionário com coleta de agosto de 2026.",
        "verification_url": "https://mapaosc.ipea.gov.br/base-dados",
        "last_verified": TODAY,
    })
else:
    source_ids["mosc"] = next(r["resource_id"] for r in resources if r["resource_name"].casefold()=="mapa das organizações da sociedade civil — ipea".casefold())

if "atlas da violência — ipea".casefold() not in existing_source_names:
    rid = next_id(resources + new_sources, "resource_id", "DR", 4)
    source_ids["violencia"] = rid
    new_sources.append({
        "resource_id": rid,
        "resource_name": "Atlas da Violência — Ipea",
        "acronym": "Atlas da Violência",
        "official_identity": "Instituto de Pesquisa Econômica Aplicada — Atlas da Violência",
        "description": "Plataforma de séries, mapas e publicações sobre violência e segurança pública no Brasil, incluindo indicadores de homicídios e análises territoriais produzidas pelo Ipea e parceiros.",
        "homepage_url": "https://www.ipea.gov.br/atlasviolencia/",
        "data_access_url": "https://www.ipea.gov.br/atlasviolencia/dados-series/158",
        "research_areas": "Planejamento Territorial e Políticas Públicas | Infraestruturas e Ciência de Dados",
        "keywords": "violência | homicídios | segurança pública | mortalidade | crime | municípios | Ipea",
        "data_product_types": "séries | indicadores | mapas | publicações | análises",
        "data_formats": "visualização web | tabelas | PDF | formatos variáveis conforme série",
        "visualization_types": "mapas | gráficos | séries | publicações",
        "geographic_coverage": "Brasil — nacional, UFs e municípios conforme série/publicação",
        "covers_brazil": "sim",
        "spatial_resolution": "Brasil | UF | município conforme série",
        "temporal_coverage": "séries históricas e edições anuais; varia conforme indicador",
        "temporal_resolution": "anual e conforme série",
        "data_sources": "SIM/Ministério da Saúde | registros de segurança pública | fontes oficiais e indicadores derivados documentados pelo Ipea",
        "free_download": "parcial",
        "access_conditions": "consulta pública; formatos e download variam por série e publicação",
        "programmatic_access": "desconhecido",
        "access_protocols": "HTTPS | consulta web | downloads conforme recurso",
        "authentication_required": "não",
        "access_documentation_url": "",
        "license": "uso público; publicações do Ipea permitem reprodução com citação sob os termos do item; verificar termos de cada série/recurso",
        "institutional_status": "público",
        "owner_or_manager": "Instituto de Pesquisa Econômica Aplicada — Ipea / parceiros do Atlas da Violência",
        "academic_uses": "Epidemiologia da violência, segurança pública, desigualdades territoriais, mortalidade por causas externas, avaliação de políticas e estudos municipais/regionais.",
        "limitations": "Indicadores combinam fontes e métodos distintos. Homicídios registrados e homicídios estimados não são intercambiáveis; qualidade do SIM, mortes violentas por causa indeterminada, cobertura territorial e revisões metodológicas devem ser preservadas por série e edição.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://www.ipea.gov.br/atlasviolencia/",
        "academic_evidence_note": "O portal oficial reúne busca de séries de dados e publicações; o Ipea documenta a qualidade e limitações dos dados de mortes violentas e publica edições metodologicamente identificadas do Atlas.",
        "verification_url": "https://www.ipea.gov.br/atlasviolencia/",
        "last_verified": TODAY,
    })
else:
    source_ids["violencia"] = next(r["resource_id"] for r in resources if r["resource_name"].casefold()=="atlas da violência — ipea".casefold())

append_rows(resources_path, RESOURCE_FIELDS, new_sources)

# Products. Use product URLs as duplicate guards, except several MOSC products legitimately share the same base page.
next_product_num = max(int(p["product_id"][2:]) for p in products) + 1
next_dist_num = max(int(d["distribution_id"][2:]) for d in dists) + 1
new_products=[]; new_dists=[]

def add_product(source_key, name, acronym, family, kind, description, keywords, coverage, spatial_support, spatial_resolution, temporal_coverage, temporal_resolution, update_frequency, status, version, enum_scope, page, methodology, pod, limitations, dist_name, access_url, fmt, protocol, tool, free_download, auth, access_conditions, license, attribution, subset, notes):
    global next_product_num, next_dist_num
    # guard by exact name rather than URL because MOSC publishes multiple data products on one official download page
    if any(p["product_name"].casefold()==name.casefold() for p in products+new_products):
        return
    pid=f"DP{next_product_num:06d}"; next_product_num += 1
    did=f"DD{next_dist_num:06d}"; next_dist_num += 1
    rid=source_ids[source_key]
    new_products.append({
        "product_id":pid,"resource_id":rid,"product_name":name,"product_acronym":acronym,"product_family":family,"product_kind":kind,
        "product_description":description,"research_areas":"Planejamento Territorial e Políticas Públicas | Infraestruturas e Ciência de Dados","keywords":keywords,
        "geographic_coverage":coverage,"covers_brazil":"sim","spatial_support":spatial_support,"spatial_resolution":spatial_resolution,
        "temporal_coverage":temporal_coverage,"temporal_resolution":temporal_resolution,"update_frequency":update_frequency,"product_status":status,
        "version_or_collection":version,"enumeration_scope":enum_scope,"product_page_url":page,"methodology_url":methodology,"primary_or_derived":pod,
        "limitations":limitations,"last_verified":TODAY,
    })
    new_dists.append({
        "distribution_id":did,"product_id":pid,"distribution_name":dist_name,"access_url":access_url,"format":fmt,"access_protocol":protocol,"access_tool":tool,
        "free_download":free_download,"authentication_required":auth,"access_conditions":access_conditions,"license":license,"provider_attribution_required":attribution,
        "subset_support":subset,"notes":notes,"last_verified":TODAY,
    })

mosc_page="https://mapaosc.ipea.gov.br/base-dados"; mosc_method="https://mapaosc.ipea.gov.br/metodologia"
terms="Termos de Uso MOSC 2025/03/20: conteúdo público pode ser republicado/divulgado com fonte, título, autor e data de acesso; uso comercial dos conteúdos hospedados é proibido"
add_product("mosc","Mapa das OSC — Base Principal das Organizações da Sociedade Civil","MOSC Base Principal","microdados das OSCs","dataset","Microdados individualizados da totalidade das OSCs identificadas pelo Mapa, incluindo organizações ativas e baixadas e variáveis cadastrais, CNAE, matriz/filial e data de fechamento quando disponível.","OSC | CNPJ | terceiro setor | associações | fundações | microdados | CNAE","Brasil — organizações da sociedade civil", "organização/CNPJ", "registro organizacional; endereço e georreferenciamento quando disponível", "base corrente com informação histórica de abertura/fechamento; coleta agosto/2026", "registro organizacional", "mensal para disponibilização da base; fontes subjacentes têm ciclos próprios", "ativo", "coleta agosto/2026; envio agosto/2026", "complete", mosc_page, mosc_method, "misto", "A classificação de OSC depende dos critérios metodológicos do Mapa e das fontes administrativas. A base inclui ativas e baixadas; situação cadastral não prova atividade substantiva. Informações autodeclaradas e de fontes auxiliares podem ter completude desigual.", "Base Principal MOSC — CSV e dicionário", "https://mapaosc.ipea.gov.br/download/20260806_MOSC_baseDivulgacao.csv", "CSV", "HTTPS download", "navegador web | cliente HTTP", "sim", "não", "download público; usar o dicionário e citar o Mapa/Ipea", terms, "sim", "arquivo completo; filtros após download", "A página oficial informa coleta e envio em agosto/2026 e oferece dicionário XLSX separado.")
add_product("mosc","Mapa das OSC — Base de Projetos das OSCs","MOSC Projetos","projetos e parcerias das OSCs","dataset","Base para download com informações de projetos, atividades e programas associados às OSCs, permitindo cruzamentos por organização e atributos do projeto quando preenchidos.","OSC | projetos | parcerias | recursos públicos | terceiro setor","Brasil — projetos associados às OSCs registradas", "OSC × projeto", "registro administrativo/autodeclarado; localização conforme campo disponível", "histórico conforme registros de projetos", "evento/projeto", "conforme atualização da plataforma", "ativo", "base corrente auditada em agosto/2026", "complete", mosc_page, mosc_method, "misto", "A presença de um projeto na base depende das fontes integradas e/ou preenchimento da OSC; ausência não significa ausência de atuação. Valores, datas, beneficiários e status podem ser incompletos ou autodeclarados.", "Base de projetos das OSCs", mosc_page, "XLSX", "HTTPS download via página", "navegador web", "sim", "não", "download público pela página Base de Dados", terms, "sim", "arquivo completo; cruzamentos por OSC/projeto após download", "A página oficial disponibiliza a base de projetos separadamente da base principal.")
add_product("mosc","Mapa das OSC — Áreas e Subáreas de Atuação","MOSC Áreas/Subáreas","classificação temática das OSCs","dataset","Base que relaciona cada OSC às áreas e subáreas de atuação registradas na plataforma, para análise temática e territorial do terceiro setor.","OSC | áreas de atuação | subáreas | classificação | terceiro setor","Brasil — OSCs com áreas/subáreas registradas", "OSC × área/subárea", "registro categórico por organização", "estado corrente/histórico conforme atualização", "registro", "conforme atualização da plataforma", "ativo", "base corrente auditada em agosto/2026", "complete", mosc_page, mosc_method, "misto", "Áreas podem derivar de classificação administrativa e informações da própria OSC; categorias não representam intensidade, qualidade ou exclusividade de atuação e podem estar ausentes.", "Base de áreas e subáreas das OSCs", "https://mapaosc.ipea.gov.br/download/area_subarea.xlsx", "XLSX", "HTTPS download", "navegador web", "sim", "não", "download público", terms, "sim", "arquivo completo", "Arquivo oficial separado da base principal; interpretar segundo metodologia e glossário do Mapa.")
add_product("mosc","Mapa das OSC — Conselhos e Conferências","MOSC Participação Social","participação social das OSCs","dataset","Base que associa OSCs a conselhos de políticas públicas e conferências registradas na plataforma, apoiando estudos de participação social institucionalizada.","OSC | conselhos | conferências | participação social | governança","Brasil — OSCs e instâncias participativas registradas", "OSC × conselho/conferência", "registro relacional; território conforme instância", "histórico conforme registros", "evento/participação", "conforme atualização da plataforma", "ativo", "base corrente auditada em agosto/2026", "complete", mosc_page, mosc_method, "misto", "Registro de participação não prova influência, frequência, representatividade ou continuidade; completude depende das fontes e do preenchimento disponível.", "Base de conselhos e conferências das OSCs", mosc_page, "XLS", "HTTPS download via página", "navegador web", "sim", "não", "download público pela página Base de Dados", terms, "sim", "arquivo completo", "A página oficial disponibiliza esta relação em arquivo próprio e descreve participação social como bloco metodológico distinto.")
add_product("mosc","Mapa das OSC — Recursos das Organizações","MOSC Recursos","recursos financeiros declarados das OSCs","dataset","Base para download com informações sobre fontes e valores de recursos associados às OSCs conforme registros disponíveis na plataforma.","OSC | recursos | financiamento | transferências | terceiro setor","Brasil — OSCs com informação de recursos", "OSC × ano/fonte de recurso", "registro financeiro por organização", "histórico conforme declaração e fontes integradas", "anual/registro", "conforme atualização da plataforma", "ativo", "base corrente auditada em agosto/2026", "complete", mosc_page, mosc_method, "misto", "Parte das informações de recursos pode ser autodeclarada ou derivar de sistemas administrativos específicos; ausência de valor não significa receita zero e valores não representam necessariamente demonstrações contábeis auditadas.", "Base de recursos das OSCs", mosc_page, "XLS", "HTTPS download via página", "navegador web", "sim", "não", "download público pela página Base de Dados", terms, "sim", "arquivo completo", "A página oficial descreve a base como informações referentes à declaração de cada OSC sobre seus recursos.")
add_product("mosc","Mapa das OSC — API pública","MOSC API","API do Mapa das OSCs","data_service","Serviço programático documentado pelo Mapa das OSC para consulta de informações disponibilizadas pela plataforma.","OSC | API | dados abertos | integração | terceiro setor","Brasil — conteúdo disponibilizado pela API do Mapa", "consulta por endpoint e parâmetros da API", "conforme recurso retornado", "corrente e histórico conforme endpoint", "requisição", "conforme atualização do serviço", "ativo", "documentação API auditada em 2026-08-19", "complete", "https://mapaosc.ipea.gov.br/api/api/documentation", mosc_method, "serviço", "Endpoints, campos, paginação e estabilidade devem ser verificados na documentação vigente. A API não torna automaticamente completos ou equivalentes os dados provenientes das diferentes fontes integradas pelo Mapa.", "Mapa das OSC — documentação/serviço API", "https://mapaosc.ipea.gov.br/api/api/documentation", "JSON conforme endpoint", "HTTPS | REST API", "cliente HTTP | navegador web", "sim", "não", "acesso público conforme documentação", terms, "sim", "conforme parâmetros/endpoints", "Swagger oficial do serviço disponível na própria plataforma.")
add_product("mosc","Perfil das Organizações da Sociedade Civil no Brasil 2016–2025","Perfil OSC 2016–2025","síntese analítica do Mapa das OSC","indicator_family","Relatório de pesquisa que atualiza o perfil das OSCs brasileiras para 2016–2025 com base no Mapa das OSC e subsidia análises da comunidade de pesquisa e políticas públicas.","OSC | perfil | 2016-2025 | terceiro setor | indicadores | Ipea","Brasil", "agregados nacionais e territoriais conforme relatório", "agregado analítico", "2016–2025", "anual/intervalos conforme indicador", "edição de relatório", "ativo", "relatório publicado em 2025; período 2016–2025", "complete", "https://mapaosc.ipea.gov.br/post/192/o-perfil-das-organizacoes-da-sociedade-civil-no-brasil-2016-2025", mosc_method, "derivado", "É uma síntese analítica derivada da base do Mapa; indicadores herdam critérios de classificação, cobertura e revisões das fontes, e não substituem os microdados para análises que exigem granularidade organizacional.", "Relatório Perfil das OSC 2016–2025", "https://mapaosc.ipea.gov.br/post/192/o-perfil-das-organizacoes-da-sociedade-civil-no-brasil-2016-2025", "HTML | relatório web", "HTTPS", "navegador web", "sim", "não", "acesso público; citar Ipea/Mapa das OSC", terms, "sim", "por seções/indicadores do relatório", "A página oficial de 01/11/2025 identifica o relatório como atualização do perfil das OSCs e aponta para a publicação completa.")

add_product("violencia","Atlas da Violência — Dados e Séries","Atlas Violência Dados","séries e indicadores de violência","federated_catalog","Catálogo interativo de séries e mapas sobre violência e segurança pública no Brasil, reunindo indicadores com fontes, conceitos e recortes territoriais próprios.","violência | homicídios | segurança pública | mortalidade | séries temporais","Brasil — nacional, UFs e municípios conforme série", "Brasil | UF | município conforme série", "agregado territorial conforme indicador", "séries históricas; período varia por indicador", "principalmente anual; varia por série", "conforme atualização das fontes e do Atlas", "ativo", "portal Atlas da Violência v2.8 auditado em 2026-08-19", "external_index", "https://www.ipea.gov.br/atlasviolencia/", "https://repositorio.ipea.gov.br/items/d0ddf95d-f03c-4160-872f-f1fc43b1da54", "agregador", "Não tratar séries distintas como homogêneas. Homicídios registrados no SIM, homicídios estimados, mortes violentas por causa indeterminada e registros de segurança pública têm definições e vieses próprios; preservar fonte, período, recorte e método.", "Atlas da Violência — consulta de dados e séries", "https://www.ipea.gov.br/atlasviolencia/", "visualização web | tabelas conforme série", "HTTPS", "navegador web", "parcial", "não", "consulta pública; download varia conforme série", "verificar termos da série/fonte original; publicações Ipea permitem reprodução com citação conforme item", "sim", "por série, território e período conforme interface", "O portal oficial apresenta busca de séries de dados; cada série deve conservar sua fonte e metodologia.")
add_product("violencia","Atlas da Violência 2025 — Retrato dos municípios brasileiros e dinâmica regional do crime organizado","Atlas Violência 2025 Municípios","Atlas da Violência — edição municipal 2025","indicator_family","Relatório institucional com ano-base 2023 que analisa violência letal, homicídios estimados por município/região, desigualdades territoriais e dinâmica regional do crime organizado.","violência | homicídios estimados | municípios | crime organizado | segurança pública | 2023","Brasil — municípios, regiões e capitais conforme análise", "município | região | capital", "agregado municipal/regional", "ano-base 2023; séries históricas adicionais conforme capítulo", "anual/por edição", "edição de relatório", "ativo", "Atlas da Violência 2025 — ano-base 2023", "complete", "https://repositorio.ipea.gov.br/collections/6f2ea994-fdfe-496b-8b21-4a0175c4bd8e", "https://repositorio.ipea.gov.br/items/d0ddf95d-f03c-4160-872f-f1fc43b1da54", "derivado", "Homicídios estimados incluem imputação de homicídios ocultos entre mortes violentas de causa indeterminada; não equivalem aos homicídios registrados no SIM. A modelagem, qualidade do registro e incerteza devem ser preservadas em comparações municipais e temporais.", "Atlas da Violência 2025 — publicação institucional", "https://repositorio.ipea.gov.br/collections/6f2ea994-fdfe-496b-8b21-4a0175c4bd8e", "PDF | página de repositório", "HTTPS", "navegador web", "sim", "não", "acesso aberto no Repositório do Conhecimento do Ipea; citar autores, edição e fonte", "reprodução permitida nos termos do item do Repositório Ipea; verificar restrições específicas da obra", "sim", "por capítulos/tabelas/mapas da publicação", "A coleção oficial do repositório lista a publicação Atlas da Violência 2025, publicada em novembro de 2025, com ano-base 2023.")

append_rows(products_path, PRODUCT_FIELDS, new_products)
append_rows(dists_path, DIST_FIELDS, new_dists)

# Add new Brazilian sources to P0 registry.
prio_path = DATA / "brazil_scope_priorities.json"
prio = json.loads(prio_path.read_text(encoding="utf-8"))
p0 = next(t for t in prio["tiers"] if t["priority_tier"] == "P0")
for src in new_sources:
    if src["resource_id"] not in p0["resource_ids"]:
        p0["resource_ids"].append(src["resource_id"])
p0["resource_ids"] = sorted(p0["resource_ids"], key=lambda x:int(x[2:]))
prio["reviewed_at"] = TODAY
prio_path.write_text(json.dumps(prio, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

# Rebuild and validate all derived state.
cmds = [
    ["python3","scripts/validate_brazil_scope.py"],
    ["python3","scripts/validate_product_catalog.py"],
    ["python3","scripts/build_catalog.py"],
    ["python3","scripts/audit_link_roles.py","--write"],
    ["python3","scripts/validate_vitrine.py"],
    ["python3","scripts/build_site_artifact.py"],
    ["git","diff","--check"],
]
for cmd in cmds:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)

# Consolidated read-back.
rr=read_rows(resources_path); pp=read_rows(products_path); dd=read_rows(dists_path)
for src in new_sources:
    assert sum(r["resource_id"]==src["resource_id"] for r in rr)==1
for p in new_products:
    assert sum(r["product_id"]==p["product_id"] for r in pp)==1
    assert sum(r["product_id"]==p["product_id"] for r in dd)>=1
assert len({r["resource_id"] for r in rr})==len(rr)
assert len({r["product_id"] for r in pp})==len(pp)
assert len({r["distribution_id"] for r in dd})==len(dd)
print(f"READBACK resources={len(rr)} products={len(pp)} distributions={len(dd)} added_sources={len(new_sources)} added_products={len(new_products)} added_distributions={len(new_dists)}")
print("NEW_SOURCE_IDS", [r["resource_id"] for r in new_sources])
print("NEW_PRODUCT_IDS", [r["product_id"] for r in new_products])
print("NEW_DISTRIBUTION_IDS", [r["distribution_id"] for r in new_dists])
