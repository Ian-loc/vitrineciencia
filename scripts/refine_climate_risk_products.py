from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = '2026-08-14'

products_path = ROOT / 'data/data_products.csv'
dists_path = ROOT / 'data/product_distributions.csv'

products = products_path.read_text(encoding='utf-8').splitlines()
dists = dists_path.read_text(encoding='utf-8').splitlines()

assert any(x.startswith('DP000042,') for x in products)
assert any(x.startswith('DP000043,') for x in products)
assert any(x.startswith('DP000044,') for x in products)
assert any(x.startswith('DP000048,') for x in products)
assert not any(x.startswith('DP000073,') for x in products)
assert any(x.startswith('DD000050,') for x in dists)
assert any(x.startswith('DD000052,') for x in dists)
assert any(x.startswith('DD000053,') for x in dists)
assert any(x.startswith('DD000058,') for x in dists)
assert any(x.startswith('DD000059,') for x in dists)
assert not any(x.startswith('DD000089,') for x in dists)

repl_products = {
'DP000042,': 'DP000042,DR0004,Fator Médio de Emissão de CO₂ do Sistema Interligado Nacional,Fator Médio SIN,SIRENE — fator médio de emissão para inventários,dataset_series,"Série oficial de fatores médios de emissão de CO₂ da geração elétrica no Sistema Interligado Nacional destinada à quantificação das emissões associadas ao consumo/geração de eletricidade em inventários corporativos ou de outra natureza.",Carbon accounting | Energy systems | Climate mitigation,fator médio | CO2 | SIN | eletricidade | inventários corporativos,Sistema Interligado Nacional — Brasil,sim,sistema elétrico nacional | série temporal,SIN,arquivos históricos e ano-base 2026 disponíveis na página oficial,mensal e anual conforme arquivo,periódica; arquivos por ano-base,ativo,séries até 2026 verificadas,complete,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao,derivado,"Este estimando representa a média das emissões da geração do SIN e é adequado a inventários. Não deve ser substituído pelo fator de margem de operação usado em projetos de MDL. Registrar ano-base e eventuais correções publicadas pelo MCTI.",2026-08-14',
'DP000043,': 'DP000043,DR0003,Índices e Indicadores de Risco Climático AdaptaBrasil,AdaptaBrasil Risco,"Risco climático, ameaça, exposição e vulnerabilidade",indicator_family,"Sistema hierárquico de índices de risco de impacto climático organizado por setores e por componentes analíticos como ameaça, exposição e vulnerabilidade; a vulnerabilidade pode incluir sensibilidade e capacidade adaptativa conforme o indicador e a metodologia setorial.",Climate adaptation | Socioecological systems | Public policy | Risk assessment,risco climático | vulnerabilidade | exposição | ameaça | sensibilidade | capacidade adaptativa | setores | indicadores,Brasil; recortes territoriais variam por indicador,sim,município e outros recortes territoriais conforme indicador,varia conforme indicador,presente e cenários futuros conforme indicador,varia conforme indicador e cenário,por atualização metodológica e de dados,ativo,catálogo corrente de indicadores,family_level,https://adaptabrasil.mcti.gov.br/sobre/lista-de-indicadores,https://adaptabrasil.mcti.gov.br/sobre/glossario,derivado,"Preservar sempre a cadeia setor → risco/impacto → componente → indicador → cenário/período → unidade territorial. Índices agregam informações não diretamente comparáveis e não quantificam automaticamente perdas; dados brutos primários não estão integralmente disponíveis.",2026-08-14',
'DP000044,': 'DP000044,DR0005,Rede Observacional do CEMADEN,Rede CEMADEN,Dados observacionais para monitoramento de desastres naturais,dataset_series,"Dados observacionais das redes do CEMADEN, incluindo pluviômetros, estações hidrológicas, PCDs geotécnicas/Acqua e radares meteorológicos acessíveis pelo Mapa Interativo; as modalidades de download diferem entre tipos de equipamento.",Hydrology | Meteorology | Natural hazards | Environmental monitoring,pluviometria | hidrologia | radares | estações | desastres | CEMADEN,Brasil conforme implantação das redes,sim,estações e sensores | radar,pontual ou cobertura de radar conforme equipamento,pluviometria para download desde 2013; demais redes conforme implantação,subdiária; varia por equipamento,quase em tempo real para visualização; downloads históricos mensais conforme módulo,ativo,Mapa Interativo / rede observacional corrente,family_level,https://mapainterativo.cemaden.gov.br/,https://www.gov.br/cemaden/pt-br/paginas/historico-da-criacao-do-cemaden,primário,"Dados disponibilizados pelo Mapa Interativo são brutos e podem conter inconsistências; timestamps são registrados em UTC. O acesso histórico varia por rede: pluviometria possui download direto por período, enquanto PCDs hidrológicas/geotécnicas/Acqua podem exigir nome/e-mail e entrega por link.",2026-08-14',
'DP000048,': 'DP000048,DR0059,Projeções Climáticas no Brasil — modelos globais e regionais,PClima Projeções,Projeções de mudanças climáticas para o Brasil,dataset_series,"Conjuntos de simulações e projeções climáticas para o Brasil provenientes de modelos globais e regionais, com seleção por conjunto de dados, modelo, experimento, cenário, período, variável, frequência e recorte espacial.",Climate science | Climate impacts | Adaptation | Environmental modelling,projeções climáticas | CMIP5 | CMIP6 | Eta | BESM | HELIX | RCP | Brasil,Brasil,sim,grade de modelo | área | ponto conforme consulta,varia por modelo e conjunto,histórico e projeções até o final do século XXI conforme conjunto,anual | mensal | diária conforme variável/conjunto,por incorporação de conjuntos/modelos,ativo,"portal corrente — conjuntos CMIP5/CMIP6, HELIX, BESM e Eta/CPTEC/INPE",family_level,https://pclima.inpe.br/analise/,https://pclima.inpe.br/?page_id=183,derivado,"Projeções dependem de modelos, experimentos e cenários e não são previsões meteorológicas. Preservar conjunto/modelo/cenário/período/frequência e incerteza entre modelos. A documentação oficial exige citação institucional do Portal; uma licença específica de reutilização não foi localizada nesta auditoria.",2026-08-14'
}

for i, line in enumerate(products):
    for prefix, replacement in repl_products.items():
        if line.startswith(prefix):
            products[i] = replacement

products.append('DP000073,DR0004,Fatores de Emissão da Margem de Operação do SIN — método da análise de despacho,Margem de Operação SIN,SIRENE — fatores de emissão para MDL,dataset_series,"Série oficial dos fatores de emissão de CO₂ da margem de operação do Sistema Interligado Nacional calculados pelo método da análise de despacho para estimar emissões deslocadas e reduções certificadas em projetos no âmbito do Mecanismo de Desenvolvimento Limpo.",Carbon accounting | Energy systems | Climate mitigation | CDM,fator de emissão | margem de operação | dispatch analysis | MDL | SIN | CO2,Sistema Interligado Nacional — Brasil,sim,sistema elétrico nacional | série temporal,SIN,anos-base 2006–2026 disponíveis na página oficial,horária | diária | mensal conforme arquivo e ano-base,por ano-base e correções,ativo,método da análise de despacho | Tool 07 UNFCCC | séries até 2026,complete,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/cgcl/paginas/metodo-da-analise-de-despacho,derivado,"Este estimando representa a margem de operação/energia deslocada e sua finalidade oficial é a quantificação de reduções certificadas em projetos de MDL. Não é intercambiável com o fator médio usado em inventários. A partir de janeiro de 2025 a base ONS foi ampliada sem alteração da metodologia; registrar ano-base e correções.",2026-08-14')

repl_dists = {
'DD000050,': 'DD000050,DP000042,SIRENE — Fator médio para inventários,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao,XLSX | notas técnicas,HTTP download,planilha | script,sim,não,acesso público,CC BY-ND 3.0 informado no conteúdo gov.br consultado,sim,ano-base | mês conforme arquivo,"Fator médio destinado a inventários corporativos ou de outra natureza; há arquivo 2026 e correções históricas publicadas. Não usar como fator de margem de operação.",2026-08-14',
'DD000052,': 'DD000052,DP000044,CEMADEN — dados pluviométricos,https://mapainterativo.cemaden.gov.br/download/download_form.php,arquivo de dados mensal,HTTP download,navegador | planilha | script,sim,não,"download por UF/município, mês e ano; confirmação de segurança/CAPTCHA; sem autenticação de conta",uso não comercial e atribuição CEMADEN conforme notas institucionais,sim,UF | município | estação | mês,"Pluviometria disponível para download desde 2013; registros em UTC. A documentação atual permite download direto após seleção e confirmação de segurança.",2026-08-14',
'DD000053,': 'DD000053,DP000044,"CEMADEN — PCDs hidrológicas, geotécnicas e Acqua",https://mapainterativo.cemaden.gov.br/,arquivos mensais,HTTP download,navegador | planilha,sim,não,"seleção por UF/município, mês e ano; formulário com nome/e-mail e confirmação de segurança; link de download enviado por e-mail",uso não comercial e atribuição CEMADEN conforme notas institucionais,sim,UF | município | equipamento | mês,"As modalidades de PCDs hidrológicas, geotécnicas e Acqua usam formulário e entrega do link por e-mail; isso é uma condição de entrega, não autenticação de conta. Registros em UTC.",2026-08-14',
'DD000058,': 'DD000058,DP000048,PClima — visualizador e download,https://pclima.inpe.br/analise/,dados de projeção | mapas | PNG | formatos selecionáveis,HTTP web/download,navegador | análise climática,sim,não,consulta e download públicos pela interface,"licença específica não localizada; documentação requer citação: dados e mapas extraídos do Portal de Mudanças Climáticas no Brasil do INPE/MCTI",sim,conjunto | modelo | experimento | cenário | variável | frequência | período | área/ponto,"A interface permite seleção explícita dos parâmetros científicos; preservar essa combinação em qualquer reutilização.",2026-08-14',
'DD000059,': 'DD000059,DP000048,PClima — API e pacote Python,https://pclima.inpe.br/analise/API/,CSV | NetCDF | comandos Wget/cURL | JSON de parâmetros,API | HTTPS | Wget | cURL,script | cliente HTTP | pacote Python apipclima,sim,sim,"cadastro no primeiro uso; token obrigatório; confirmação de e-mail para habilitar download","licença específica não localizada; citação institucional do Portal requerida",sim,conjunto | modelo | experimento | cenário | variável | frequência | ano/mês | bbox/ponto/área definida,"Documentação oficial informa frequências anual, mensal e diária e geração de chamadas Wget/cURL/JSON; o token autentica o usuário da API.",2026-08-14'
}

for i, line in enumerate(dists):
    for prefix, replacement in repl_dists.items():
        if line.startswith(prefix):
            dists[i] = replacement

dists.append('DD000089,DP000073,SIRENE — Margem de Operação do SIN / análise de despacho,https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao,XLSX | notas técnicas | referência metodológica UNFCCC,HTTP download,planilha | script,sim,não,acesso público,CC BY-ND 3.0 informado no conteúdo gov.br consultado,sim,ano-base | hora/dia/mês conforme arquivo,"Série 2006–2026; finalidade oficial associada a MDL/RCE. A base ONS foi ampliada em janeiro de 2025 mantendo a metodologia; registrar correções publicadas por ano-base.",2026-08-14')

products_path.write_text('\n'.join(products) + '\n', encoding='utf-8')
dists_path.write_text('\n'.join(dists) + '\n', encoding='utf-8')

ptxt = products_path.read_text(encoding='utf-8')
dtxt = dists_path.read_text(encoding='utf-8')
assert ptxt.count('DP000073,') == 1
assert dtxt.count('DD000089,') == 1
assert 'Fator Médio de Emissão de CO₂' in ptxt
assert 'Margem de Operação do SIN' in ptxt
assert 'sem autenticação de conta' in dtxt
assert 'token obrigatório' in dtxt
