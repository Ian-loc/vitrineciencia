#!/usr/bin/env python3
import csv, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'data/data_products.csv'
D=ROOT/'data/product_distributions.csv'
TODAY='2026-08-15'

def read(path):
    with path.open(encoding='utf-8', newline='') as f:
        r=csv.DictReader(f); return r.fieldnames, list(r)
def write(path, fields, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)

pf, products=read(P); df, dists=read(D)
assert len(products)==126, len(products)
assert len(dists)==142, len(dists)
assert products[-1]['product_id']=='DP000126'
assert dists[-1]['distribution_id']=='DD000142'
assert not any(x['product_id'] in {'DP000127','DP000128','DP000129'} for x in products)
assert not any(x['distribution_id'] in {'DD000143','DD000144','DD000145'} for x in dists)

new_products=[
{
'product_id':'DP000127','resource_id':'DR0074','product_name':'Hidroquímica — cartas e mapas temáticos do IBGE','product_acronym':'Hidroquímica IBGE','product_family':'Mapas Ambientais — Hidroquímica','product_kind':'dataset_series','product_description':'Família de cartas e mapas hidroquímicos do IBGE sobre qualidade química de águas subterrâneas e superficiais, incluindo cartas temáticas 1:250.000 e produtos estaduais ou regionais em outras escalas.','research_areas':'Hydrology | Geosciences | Environmental mapping | GIS','keywords':'hidroquímica | água subterrânea | água superficial | potabilidade | irrigação | aquíferos | IBGE','geographic_coverage':'Brasil — cobertura parcial conforme carta, estado ou região; produtos documentados incluem Nordeste','covers_brazil':'sim','spatial_support':'cartas temáticas | polígonos e feições vetoriais | mapas regionais','spatial_resolution':'varia por produto; catálogo temático inclui 1:250.000 e mapas regionais documentados em 1:2.500.000','temporal_coverage':'levantamentos e análises físico-químicas de diferentes períodos; produtos regionais publicados ao menos em 2007–2014','temporal_resolution':'por levantamento/edição','update_frequency':'irregular','product_status':'ativo','version_or_collection':'coleção de cartas e mapas hidroquímicos; edições variáveis','enumeration_scope':'family_level','product_page_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/geologia.html','methodology_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/geologia.html','primary_or_derived':'derivado','limitations':'Não tratar a família como mosaico nacional homogêneo nem assumir escala única. A página temática lista Hidroquímica 1:250.000, enquanto produtos regionais documentados do Nordeste foram publicados em 1:2.500.000; preservar recorte, escala, data, tipo de manancial, fonte analítica e edição efetivamente usados.','last_verified':TODAY},
{
'product_id':'DP000128','resource_id':'DR0060','product_name':'Coleções Biológicas do IBGE','product_acronym':'Coleções Biológicas IBGE','product_family':'Acervos biológicos institucionais','product_kind':'catalog','product_description':'Portal e conjunto de acervos biológicos mantidos pelo IBGE, reunindo os herbários IBGE e RADAMBRASIL e a Coleção Zoológica da Reserva Ecológica do IBGE, com registros taxonômicos, procedência, ambiente e dados de coleta.','research_areas':'Biodiversity | Conservation biology | Ecology | Environmental data science','keywords':'coleções biológicas | herbário | coleção zoológica | espécimes | taxonomia | SiBBr | biodiversidade | IBGE','geographic_coverage':'Brasil e proveniências adicionais conforme acervo e espécime','covers_brazil':'sim','spatial_support':'registro de espécime/lote | localidade de coleta | coleção institucional','spatial_resolution':'varia por registro e qualidade da georreferência/procedência','temporal_coverage':'acervos históricos e contemporâneos; período varia por subcoleção e espécime','temporal_resolution':'evento de coleta/registro quando disponível','update_frequency':'irregular conforme incorporação e digitalização do acervo','product_status':'ativo','version_or_collection':'portal de Coleções Biológicas; página institucional lançada em 2024','enumeration_scope':'external_index','product_page_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/39450-colecoes-biologicas.html','methodology_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/39450-colecoes-biologicas.html','primary_or_derived':'primário','limitations':'Acervos, subcoleções e níveis de digitalização não são homogêneos. Registros disponíveis no SiBBr devem preservar identificador, coleção, taxonomia, procedência, data e qualidade da georreferência; acesso digital não implica que todo o acervo físico esteja digitalizado.','last_verified':TODAY},
{
'product_id':'DP000129','resource_id':'DR0074','product_name':'Potencial de Agressividade Climática na Amazônia Legal — 2014','product_acronym':'Agressividade Climática Amazônia 2014','product_family':'Mapas Ambientais Série Brasil','product_kind':'map_layer_collection','product_description':'Mapa temático do IBGE que integra variáveis climáticas com características de relevo e cobertura vegetal para classificar o potencial de agressividade climática na Amazônia Legal em classes alta, média e baixa e respectivos fatores.','research_areas':'Climate science | Environmental mapping | Amazon studies | Territorial analysis','keywords':'agressividade climática | Amazônia Legal | chuva | deficiência hídrica | relevo | vegetação | IBGE','geographic_coverage':'Amazônia Legal brasileira','covers_brazil':'parcial','spatial_support':'mapa temático | polígonos vetoriais','spatial_resolution':'escala 1:5.000.000','temporal_coverage':'dados climatológicos e pluviométricos de 1960–1990; publicação 2014','temporal_resolution':'síntese climatológica histórica','update_frequency':'por edição; atualização posterior não inferida','product_status':'ativo','version_or_collection':'mapa publicado em 2014; referência climática 1960–1990','enumeration_scope':'complete','product_page_url':'https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/14702-asi-ibge-mapeia-potencial-de-agressividade-climatica-na-amazonia','methodology_url':'https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/14702-asi-ibge-mapeia-potencial-de-agressividade-climatica-na-amazonia','primary_or_derived':'derivado','limitations':'Produto histórico de pequena escala baseado em dados de 326 estações no período 1960–1990 e outras fontes. Não representa risco climático atual, projeção futura ou série meteorológica; não extrapolar suas classes para decisões locais sem dados mais recentes e de maior detalhe.','last_verified':TODAY}
]
for row in new_products:
    assert set(row)==set(pf), (set(pf)-set(row), set(row)-set(pf))
products.extend(new_products)

new_dists=[
{'distribution_id':'DD000143','product_id':'DP000127','distribution_name':'Hidroquímica IBGE — página temática e cartas/mapas','access_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/geologia.html','format':'cartas temáticas | PDF | vetores/Shapefile conforme produto e edição','access_protocol':'HTTP web | HTTP download','access_tool':'navegador web | SIG','free_download':'sim','authentication_required':'não','access_conditions':'acesso público conforme carta/mapa disponível; selecionar recorte e edição','license':'licença específica não inferida; observar termos de uso do IBGE e metadados do arquivo','provider_attribution_required':'sim','subset_support':'por carta, estado, região ou produto quando disponibilizado','notes':'A página temática lista Hidroquímica 1:250.000; produtos regionais do Nordeste também foram disponibilizados em PDF e vetor em 1:2.500.000. Não generalizar escala ou cobertura.','last_verified':TODAY},
{'distribution_id':'DD000144','product_id':'DP000128','distribution_name':'Coleções Biológicas do IBGE — portal e acesso SiBBr','access_url':'https://www.ibge.gov.br/geociencias/informacoes-ambientais/biodiversidade/39450-colecoes-biologicas.html','format':'registros de coleção | metadados | imagens | links para dados no SiBBr','access_protocol':'HTTP web | serviços externos vinculados','access_tool':'navegador web | SiBBr','free_download':'parcial','authentication_required':'não','access_conditions':'consulta pública; parte do acervo zoológico possui dados digitais no SiBBr e o acesso físico depende de agendamento','license':'verificar licença e termos no registro/portal de distribuição correspondente','provider_attribution_required':'sim','subset_support':'por coleção, subcoleção e registro conforme sistema de acesso','notes':'Aves e Mamíferos estão informatizados e disponíveis via SiBBr; outros segmentos têm níveis de digitalização distintos. O portal também descreve os herbários institucionais.','last_verified':TODAY},
{'distribution_id':'DD000145','product_id':'DP000129','distribution_name':'Potencial de Agressividade Climática na Amazônia Legal — mapa e vetor','access_url':'https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/14702-asi-ibge-mapeia-potencial-de-agressividade-climatica-na-amazonia','format':'PDF | Shapefile','access_protocol':'HTTP web | download institucional referenciado','access_tool':'navegador web | SIG','free_download':'sim','authentication_required':'não','access_conditions':'acesso público aos produtos digitais documentados pelo IBGE','license':'licença específica não inferida; observar termos de uso do IBGE e metadados do arquivo','provider_attribution_required':'sim','subset_support':'não documentado','notes':'Produto em escala 1:5.000.000; o release oficial documenta PDF e shape e a referência climática 1960–1990. URLs FTP históricas podem exigir navegação pelo acervo atual do IBGE.','last_verified':TODAY}
]
for row in new_dists:
    assert set(row)==set(df), (set(df)-set(row), set(row)-set(df))
dists.extend(new_dists)
write(P,pf,products); write(D,df,dists)
assert len(products)==129 and len(dists)==145
assert len({r['product_id'] for r in products})==len(products)
assert len({r['distribution_id'] for r in dists})==len(dists)
product_ids={r['product_id'] for r in products}
assert all(r['product_id'] in product_ids for r in dists)

commands=[
['python','scripts/validate_brazil_scope.py'],
['python','scripts/validate_product_catalog.py'],
['python','scripts/build_catalog.py'],
['python','scripts/audit_link_roles.py','--write'],
['python','scripts/audit_link_roles.py'],
['python','scripts/validate_vitrine.py'],
]
for cmd in commands:
    print('+',' '.join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True)
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('MATERIALIZED 74 sources / 129 products / 145 distributions')
