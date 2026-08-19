#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / 'data' / 'data_products.csv'
DISTS = ROOT / 'data' / 'product_distributions.csv'
VERIFIED = '2026-08-19'

PRODUCT_ROWS = [
    {
        'product_name':'Transações correntes — mensal — saldo','product_acronym':'Transações correntes','product_family':'Balanço de Pagamentos — BPM6','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo de transações correntes do balanço de pagamentos, agregando balança comercial de bens, serviços, renda primária e renda secundária segundo a metodologia BPM6.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'balanço de pagamentos | transações correntes | conta corrente | setor externo | BPM6 | SGS | Banco Central',
        'geographic_coverage':'Brasil; relações econômicas com não residentes','covers_brazil':'sim','spatial_support':'série temporal nacional de transações com o exterior','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 1995–presente conforme metadados oficiais','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 22701 — série corrente','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/22701-transacoes-correntes---mensal---saldo',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/22701-transacoes-correntes---mensal---saldo','primary_or_derived':'derivado',
        'limitations':'Saldo agregado do balanço de pagamentos, não fluxo financeiro de uma única categoria. A decomposição entre bens, serviços, renda primária e renda secundária, revisões e convenções BPM6 devem ser preservadas; valor líquido não identifica por si só causa econômica.'
    },
    {
        'product_name':'Balança comercial — Balanço de Pagamentos — mensal — saldo','product_acronym':'Balança comercial BP','product_family':'Balanço de Pagamentos — BPM6','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo da balança comercial de bens no balanço de pagamentos, registrando transações internacionais de bens segundo os conceitos do BPM6.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'balança comercial | bens | exportações | importações | balanço de pagamentos | BPM6 | SGS | Banco Central',
        'geographic_coverage':'Brasil; transações de bens com não residentes','covers_brazil':'sim','spatial_support':'série temporal nacional de transações com o exterior','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 1995–presente conforme metadados oficiais','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 22707 — série corrente','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/22707-balanca-comercial---balanco-de-pagamentos---mensal---saldo',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/22707-balanca-comercial---balanco-de-pagamentos---mensal---saldo','primary_or_derived':'derivado',
        'limitations':'A balança de bens do balanço de pagamentos segue conceitos BPM6 e não deve ser presumida idêntica, sem reconciliação metodológica, às estatísticas aduaneiras de comércio exterior. Saldo líquido não substitui exportações e importações brutas.'
    },
    {
        'product_name':'Investimentos diretos no país — IDP — mensal — líquido','product_acronym':'IDP líquido','product_family':'Balanço de Pagamentos — investimento direto','product_kind':'dataset_series',
        'product_description':'Série mensal do fluxo líquido de investimento direto no país, referente a passivos de residentes brasileiros diante de não residentes em relações de controle ou influência significativa, incluindo participação no capital e operações intercompanhia.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'investimento direto no país | IDP | investimento estrangeiro direto | capital | operações intercompanhia | BPM6 | Banco Central',
        'geographic_coverage':'Brasil; relações de investimento direto com não residentes','covers_brazil':'sim','spatial_support':'série temporal nacional de fluxos financeiros','spatial_resolution':'não espacial',
        'temporal_coverage':'série mensal; início conforme metadados oficiais do BCB','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 22885 — série corrente','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/22885-investimentos-diretos-no-pais---idp---mensal---liquido',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/22885-investimentos-diretos-no-pais---idp---mensal---liquido','primary_or_derived':'derivado',
        'limitations':'Fluxo líquido de investimento direto segundo BPM6; não equivale a estoque de capital estrangeiro, valor de mercado de empresas ou investimento produtivo físico observado. Participação no capital e operações intercompanhia têm comportamentos próprios.'
    },
    {
        'product_name':'Investimentos diretos no exterior — IDE — mensal — líquido','product_acronym':'IDE líquido','product_family':'Balanço de Pagamentos — investimento direto','product_kind':'dataset_series',
        'product_description':'Série mensal do fluxo líquido de investimento direto no exterior, referente a ativos externos detidos por residentes brasileiros em relações de controle ou influência significativa, incluindo participação no capital e operações intercompanhia.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'investimento direto no exterior | IDE | ativos externos | capital | operações intercompanhia | BPM6 | Banco Central',
        'geographic_coverage':'Brasil; investimentos de residentes em não residentes','covers_brazil':'sim','spatial_support':'série temporal nacional de fluxos financeiros','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 1995–presente conforme metadados oficiais','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 22865 — série corrente','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/22865-investimentos-diretos-no-exterior---ide---mensal---liquido',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/22865-investimentos-diretos-no-exterior---ide---mensal---liquido','primary_or_derived':'derivado',
        'limitations':'Fluxo líquido de investimento direto de residentes no exterior; não equivale a estoque de ativos externos, valor de mercado ou investimento físico realizado. Ingressos e saídas e os instrumentos de capital/intercompanhia devem ser analisados separadamente quando necessário.'
    },
    {
        'product_name':'Taxa média de juros do crédito com recursos livres — pessoas físicas — total','product_acronym':'Juros crédito livre PF','product_family':'Estatísticas monetárias e de crédito','product_kind':'dataset_series',
        'product_description':'Taxa média de juros das novas operações de crédito com recursos livres contratadas por pessoas físicas no Sistema Financeiro Nacional, ponderada pelo valor das concessões.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'crédito | taxa de juros | pessoas físicas | recursos livres | concessões | SFN | Banco Central',
        'geographic_coverage':'Brasil','covers_brazil':'sim','spatial_support':'série temporal nacional de novas operações de crédito','spatial_resolution':'não espacial',
        'temporal_coverage':'março de 2011–presente','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 20740 — percentual ao ano','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/20740-taxa-media-de-juros-das-operacoes-de-credito-com-recursos-livres---pessoas-fisicas---total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/20740-taxa-media-de-juros-das-operacoes-de-credito-com-recursos-livres---pessoas-fisicas---total','primary_or_derived':'derivado',
        'limitations':'Taxa ponderada pelas concessões de novas operações com recursos livres; não é taxa de estoque da carteira, custo efetivo de um tomador individual ou taxa de crédito direcionado. Composição de modalidades e concessões influencia a média.'
    },
    {
        'product_name':'Taxa média de juros do crédito com recursos livres — pessoas jurídicas — total','product_acronym':'Juros crédito livre PJ','product_family':'Estatísticas monetárias e de crédito','product_kind':'dataset_series',
        'product_description':'Taxa média de juros das novas operações de crédito com recursos livres contratadas por pessoas jurídicas no Sistema Financeiro Nacional, ponderada pelo valor das concessões.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'crédito | taxa de juros | pessoas jurídicas | recursos livres | concessões | SFN | Banco Central',
        'geographic_coverage':'Brasil','covers_brazil':'sim','spatial_support':'série temporal nacional de novas operações de crédito','spatial_resolution':'não espacial',
        'temporal_coverage':'março de 2011–presente','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 20718 — percentual ao ano','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/20718-taxa-media-de-juros-das-operacoes-de-credito-com-recursos-livres---pessoas-juridicas---total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/20718-taxa-media-de-juros-das-operacoes-de-credito-com-recursos-livres---pessoas-juridicas---total','primary_or_derived':'derivado',
        'limitations':'Taxa ponderada pelas concessões de novas operações com recursos livres; não é custo efetivo de qualquer empresa específica, taxa do estoque da carteira ou taxa de crédito direcionado. A composição das modalidades contratadas afeta a média.'
    },
    {
        'product_name':'Saldo de dívida externa — total','product_acronym':'Dívida externa total','product_family':'Crédito ampliado e dívida','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo em final de período da dívida externa abrangida pelas estatísticas de crédito ampliado do Banco Central, composta por operações de crédito e títulos de dívida segundo o escopo metodológico da série.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'dívida externa | crédito ampliado | empréstimos | títulos de dívida | setor externo | SGS | Banco Central',
        'geographic_coverage':'Brasil; obrigações com credores externos conforme escopo da série','covers_brazil':'sim','spatial_support':'série temporal nacional de saldo financeiro','spatial_resolution':'não espacial',
        'temporal_coverage':'série mensal; início conforme metadados oficiais','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 28192 — série corrente','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/28192-saldo-de-divida-externa-total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/28192-saldo-de-divida-externa-total','primary_or_derived':'derivado',
        'limitations':'Saldo de fim de período em milhões de reais segundo o escopo de crédito ampliado; não equivale automaticamente a dívida externa bruta em qualquer outra publicação ou conceito internacional sem reconciliação metodológica. Fluxos e saldos não são intercambiáveis.'
    },
    {
        'product_name':'Saldo de crédito ampliado concedido a empresas e famílias — total','product_acronym':'Crédito ampliado empresas e famílias','product_family':'Crédito ampliado e dívida','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo de crédito ampliado concedido a empresas e famílias, incorporando operações de crédito e títulos de dívida segundo a abrangência definida pelo Banco Central.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'crédito ampliado | empresas | famílias | empréstimos | financiamentos | títulos de dívida | SGS | Banco Central',
        'geographic_coverage':'Brasil','covers_brazil':'sim','spatial_support':'série temporal nacional de saldo financeiro','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 2013–presente','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 28203 — série corrente; metadados revisados em 08/06/2026','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/28203-saldo-de-credito-ampliado-concedido-a-empresas-e-familias-total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/28203-saldo-de-credito-ampliado-concedido-a-empresas-e-familias-total','primary_or_derived':'derivado',
        'limitations':'Crédito ampliado é conceito mais amplo que empréstimos bancários tradicionais e inclui componentes como títulos de dívida conforme metodologia. O saldo não representa concessões do mês, número de tomadores ou endividamento líquido após ativos.'
    },
    {
        'product_name':'Saldo de crédito ampliado concedido a empresas — total','product_acronym':'Crédito ampliado empresas','product_family':'Crédito ampliado e dívida','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo de crédito ampliado concedido a empresas, agregando operações de crédito e títulos de dívida segundo o escopo definido pelo Banco Central.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'crédito ampliado | empresas | crédito empresarial | títulos de dívida | SGS | Banco Central',
        'geographic_coverage':'Brasil','covers_brazil':'sim','spatial_support':'série temporal nacional de saldo financeiro','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 2013–presente','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 28846 — série corrente; metadados publicados em 08/06/2026','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/28846-saldo-de-credito-ampliado-concedido-a-empresas-total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/28846-saldo-de-credito-ampliado-concedido-a-empresas-total','primary_or_derived':'derivado',
        'limitations':'Saldo agregado de crédito ampliado empresarial; não equivale a concessões mensais, crédito bancário estrito, dívida líquida ou condição financeira de uma empresa individual. Componentes devem ser preservados quando houver decomposição analítica.'
    },
    {
        'product_name':'Saldo de crédito ampliado concedido a famílias — total','product_acronym':'Crédito ampliado famílias','product_family':'Crédito ampliado e dívida','product_kind':'dataset_series',
        'product_description':'Série mensal do saldo de crédito ampliado concedido a famílias, agregando operações de crédito e instrumentos de dívida conforme o escopo definido pelo Banco Central.',
        'research_areas':'Economics | Finance | Public policy | Data infrastructure','keywords':'crédito ampliado | famílias | crédito às famílias | endividamento | SGS | Banco Central',
        'geographic_coverage':'Brasil','covers_brazil':'sim','spatial_support':'série temporal nacional de saldo financeiro','spatial_resolution':'não espacial',
        'temporal_coverage':'janeiro de 2013–presente','temporal_resolution':'mensal','update_frequency':'mensal','product_status':'ativo',
        'version_or_collection':'SGS código 28858 — série corrente; metadados publicados em 2026','enumeration_scope':'complete','product_page_url':'https://dadosabertos.bcb.gov.br/dataset/28858-saldo-de-credito-ampliado-concedido-a-familias-total',
        'methodology_url':'https://dadosabertos.bcb.gov.br/dataset/28858-saldo-de-credito-ampliado-concedido-a-familias-total','primary_or_derived':'derivado',
        'limitations':'Saldo agregado de crédito ampliado às famílias; não é concessão mensal, renda, capacidade de pagamento, número de famílias devedoras ou dívida líquida. A abrangência é definida pelos instrumentos incluídos na metodologia do crédito ampliado.'
    },
]


def read_rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def max_id(rows, field, prefix):
    vals=[]
    for r in rows:
        v=r[field]
        if v.startswith(prefix):
            try: vals.append(int(v[len(prefix):]))
            except ValueError: pass
    return max(vals) if vals else 0

products=read_rows(PRODUCTS)
dists=read_rows(DISTS)
pfields=list(products[0].keys())
dfields=list(dists[0].keys())
existing_urls={p['product_page_url'].rstrip('/') for p in products}
existing_names={p['product_name'] for p in products}
next_p=max_id(products,'product_id','DP')+1
next_d=max_id(dists,'distribution_id','DD')+1
added=[]

with PRODUCTS.open('a', encoding='utf-8', newline='') as pf, DISTS.open('a', encoding='utf-8', newline='') as df:
    pw=csv.DictWriter(pf, fieldnames=pfields, lineterminator='\n')
    dw=csv.DictWriter(df, fieldnames=dfields, lineterminator='\n')
    for spec in PRODUCT_ROWS:
        url=spec['product_page_url'].rstrip('/')
        if url in existing_urls or spec['product_name'] in existing_names:
            continue
        pid=f'DP{next_p:06d}'; did=f'DD{next_d:06d}'
        next_p+=1; next_d+=1
        row={k:'' for k in pfields}
        row.update(spec)
        row['product_id']=pid; row['resource_id']='DR0126'; row['last_verified']=VERIFIED
        pw.writerow(row)
        dist={k:'' for k in dfields}
        dist.update({
            'distribution_id':did,'product_id':pid,
            'distribution_name':spec['product_name']+' — dados e API SGS',
            'access_url':spec['product_page_url'],
            'format':'JSON | CSV | HTML | WSDL',
            'access_protocol':'HTTPS | BCData/SGS REST | SOAP',
            'access_tool':'navegador web | script | cliente HTTP',
            'free_download':'sim','authentication_required':'não',
            'access_conditions':'acesso público; consultas programáticas sujeitas aos parâmetros e limites documentados pelo BCB',
            'license':'Open Data Commons Open Database License (ODbL)',
            'provider_attribution_required':'sim',
            'subset_support':'por código da série e intervalo temporal conforme serviço',
            'notes':'O portal fornece metadados e recursos JSON/CSV/HTML e, quando aplicável, WSDL do SGS. Preservar código, unidade, periodicidade, revisões e metodologia da série.',
            'last_verified':VERIFIED,
        })
        dw.writerow(dist)
        existing_urls.add(url); existing_names.add(spec['product_name']); added.append((pid,did,spec['product_name']))

print('ADDED', len(added), added)
if not added:
    raise SystemExit('No eligible new products: all canonical URLs/names already present')
