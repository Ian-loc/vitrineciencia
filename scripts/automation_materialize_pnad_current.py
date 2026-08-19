from pathlib import Path
import csv, io

P=Path('data/data_products.csv')
D=Path('data/product_distributions.csv')

def read_header(path):
    with path.open(encoding='utf-8', newline='') as f:
        return next(csv.reader(f))

def patch_row(path, key, keyval, updates):
    header=read_header(path)
    idx={k:i for i,k in enumerate(header)}
    lines=path.read_text(encoding='utf-8').splitlines(True)
    found=False
    out=[]
    for line in lines:
        row=next(csv.reader([line]))
        if row and row[idx[key]]==keyval:
            for k,v in updates.items(): row[idx[k]]=v
            s=io.StringIO(newline='')
            csv.writer(s,lineterminator='\n').writerow(row)
            line=s.getvalue(); found=True
        out.append(line)
    if not found: raise SystemExit(f'missing {keyval}')
    path.write_text(''.join(out),encoding='utf-8')

def append_dict(path, record):
    header=read_header(path)
    txt=path.read_text(encoding='utf-8')
    ids={r[0] for r in csv.reader(txt.splitlines()) if r}
    if record[header[0]] in ids: raise SystemExit(f"duplicate id {record[header[0]]}")
    s=io.StringIO(newline='')
    w=csv.DictWriter(s,fieldnames=header,lineterminator='\n')
    w.writerow({k:record.get(k,'') for k in header})
    if txt and not txt.endswith('\n'): txt+='\n'
    path.write_text(txt+s.getvalue(),encoding='utf-8')

# Guard the verified baseline so IDs are never reused across concurrent work.
with P.open(encoding='utf-8',newline='') as f: products=list(csv.DictReader(f))
with D.open(encoding='utf-8',newline='') as f: dists=list(csv.DictReader(f))
if len(products)!=754 or len(dists)!=785:
    raise SystemExit(f'baseline moved: products={len(products)} distributions={len(dists)}')
if any(x['product_id'] in {'DP000759','DP000760'} for x in products): raise SystemExit('new product IDs occupied')
if any(x['distribution_id'] in {'DD000790','DD000791'} for x in dists): raise SystemExit('new distribution IDs occupied')

patch_row(P,'product_id','DP000310',{
    'temporal_coverage':'série nacional desde 2000; edição mais recente materialmente verificada: junho de 2026',
    'version_or_collection':'série corrente; metodologia 6ª ed. 2023; junho de 2026 materialmente verificado',
    'limitations':'População-alvo inclui empresas varejistas formalmente constituídas com 20 ou mais pessoas ocupadas segundo os critérios da pesquisa. Os resultados são índices, não níveis absolutos de vendas; ajuste sazonal e revisões devem ser preservados. O calendário conjuntural oficial do IBGE registra junho/2026 como divulgado em 13/08/2026.',
    'last_verified':'2026-08-18'
})
patch_row(D,'distribution_id','DD000331',{
    'notes':'A edição de junho/2026 é materialmente sustentada pelo calendário conjuntural oficial do IBGE, com divulgação em 13/08/2026; preservar revisões, ajuste sazonal e o plano tabular.',
    'last_verified':'2026-08-18'
})

append_dict(P,{
'product_id':'DP000759','resource_id':'DR0093','product_name':'PNAD Contínua — divulgação mensal — junho de 2026','product_acronym':'PNADC Mensal 06/2026','product_family':'PNAD Contínua — mercado de trabalho','product_kind':'dataset_series','product_description':'Divulgação mensal da PNAD Contínua para o trimestre móvel encerrado em junho de 2026, com indicadores de força de trabalho, ocupação, desocupação, subutilização e rendimentos produzidos a partir da amostra domiciliar contínua do IBGE.','research_areas':'Demography | Labour | Social statistics | Public policy','keywords':'PNAD Contínua | mercado de trabalho | ocupação | desocupação | subutilização | rendimento | trimestre móvel | junho 2026 | IBGE','geographic_coverage':'Brasil; recortes adicionais conforme tabelas oficiais da PNAD Contínua','covers_brazil':'sim','spatial_support':'estimativas agregadas de pesquisa domiciliar amostral','spatial_resolution':'Brasil e demais recortes oficialmente divulgados conforme indicador/tabela','temporal_coverage':'trimestre móvel encerrado em junho de 2026; série histórica da PNAD Contínua','temporal_resolution':'trimestre móvel com divulgação mensal','update_frequency':'mensal','product_status':'ativo','version_or_collection':'junho de 2026 — divulgado em 30/07/2026','enumeration_scope':'complete','product_page_url':'https://www.ibge.gov.br/estatisticas/sociais/trabalho/9171-pesquisa-nacional-por-amostra-de-domicilios-continua-mensal.html','methodology_url':'https://metadados.ibge.gov.br/consulta/estatisticos/operacoes-estatisticas/B5','primary_or_derived':'derivado','limitations':'A divulgação mensal refere-se a um trimestre móvel, não a observações isoladas do mês de junho. As estimativas derivam de desenho amostral complexo e exigem pesos, conceitos e revisões oficiais; não representam registro administrativo individual nem contagem censitária. Comparações com a divulgação trimestral devem respeitar janelas temporais e planos de tabulação distintos.','last_verified':'2026-08-18'
})
append_dict(P,{
'product_id':'DP000760','resource_id':'DR0093','product_name':'PNAD Contínua — divulgação trimestral — 2º trimestre de 2026','product_acronym':'PNADC Trimestral 2T2026','product_family':'PNAD Contínua — mercado de trabalho','product_kind':'dataset_series','product_description':'Divulgação trimestral da PNAD Contínua referente a abril–junho de 2026, com estimativas de mercado de trabalho e características da população em idade de trabalhar para os recortes territoriais previstos no plano da pesquisa.','research_areas':'Demography | Labour | Social statistics | Public policy | Regional development','keywords':'PNAD Contínua | mercado de trabalho | trimestre | 2º trimestre 2026 | ocupação | desocupação | rendimento | Unidades da Federação | IBGE','geographic_coverage':'Brasil; Grandes Regiões, Unidades da Federação e demais recortes divulgados no plano trimestral','covers_brazil':'sim','spatial_support':'estimativas agregadas de pesquisa domiciliar amostral','spatial_resolution':'Brasil, Grandes Regiões, UFs e outros recortes oficialmente divulgados conforme tabela','temporal_coverage':'abril a junho de 2026; série trimestral da PNAD Contínua','temporal_resolution':'trimestre civil','update_frequency':'trimestral','product_status':'ativo','version_or_collection':'2º trimestre de 2026 — divulgado em 14/08/2026','enumeration_scope':'complete','product_page_url':'https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pesquisa-nacional-por-amostra-de-domicilios-continua-trimestral.html','methodology_url':'https://metadados.ibge.gov.br/consulta/estatisticos/operacoes-estatisticas/B5','primary_or_derived':'derivado','limitations':'Estimativas trimestrais derivam de pesquisa amostral complexa e não são contagens censitárias nem registros administrativos. Recortes territoriais e precisão variam segundo indicador; intervalos/coeficientes de variação e revisões devem ser considerados. A janela abril–junho não deve ser confundida com a divulgação mensal de trimestre móvel sem verificar a referência temporal.','last_verified':'2026-08-18'
})

append_dict(D,{
'distribution_id':'DD000790','product_id':'DP000759','distribution_name':'IBGE — PNAD Contínua Mensal — junho de 2026','access_url':'https://www.ibge.gov.br/estatisticas/sociais/trabalho/9171-pesquisa-nacional-por-amostra-de-domicilios-continua-mensal.html','format':'SIDRA | XLSX | ODS | PDF | HTML conforme recurso oficial','access_protocol':'HTTPS / SIDRA','access_tool':'navegador web | SIDRA','free_download':'sim','authentication_required':'não','access_conditions':'acesso público; observar desenho amostral, notas técnicas e política de revisão','license':'licença específica dos arquivos não determinada nesta auditoria','provider_attribution_required':'sim','subset_support':'por período, indicador e recorte territorial conforme tabela','notes':'A referência mensal é o trimestre móvel encerrado em junho de 2026, divulgado em 30/07/2026; não interpretar como estimativa referente apenas ao mês de junho.','last_verified':'2026-08-18'
})
append_dict(D,{
'distribution_id':'DD000791','product_id':'DP000760','distribution_name':'IBGE — PNAD Contínua Trimestral — 2º trimestre de 2026','access_url':'https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pesquisa-nacional-por-amostra-de-domicilios-continua-trimestral.html','format':'SIDRA | XLSX | ODS | PDF | HTML conforme recurso oficial','access_protocol':'HTTPS / SIDRA','access_tool':'navegador web | SIDRA','free_download':'sim','authentication_required':'não','access_conditions':'acesso público; observar desenho amostral, precisão e política de revisão','license':'licença específica dos arquivos não determinada nesta auditoria','provider_attribution_required':'sim','subset_support':'por trimestre, indicador e recorte territorial conforme tabela','notes':'Refere-se ao trimestre civil abril–junho de 2026, divulgado em 14/08/2026. Preservar diferenças de janela e abrangência em relação à divulgação mensal por trimestre móvel.','last_verified':'2026-08-18'
})

print('materialized PMC refresh + DP000759-DP000760 + DD000790-DD000791')
