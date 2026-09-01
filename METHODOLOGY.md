# Metodologia de curadoria — Vitrine Ciência

**Status atual:** modelo físico legado preservado para compatibilidade; ontologia em auditoria desde 2026-09-01. As definições `Fonte → Produto → Distribuição` abaixo descrevem o schema histórico e não antecipam a ontologia final. Estado corrente: `docs/PROJECT_STATE.md`; workflow: `WORKFLOW_STATUS.md`.

## 1. Escopo

A Vitrine Ciência é um catálogo público de descoberta de fontes e produtos de dados relevantes ao Brasil. A curadoria organiza **fonte → produto → distribuição**, registra evidências e limitações e aponta para o provedor original. Não hospeda por padrão cópias integrais dos datasets.

## 2. Unidades de registro

### Fonte

Plataforma, portal, repositório, catálogo, programa, rede, observatório ou infraestrutura que permite descobrir ou acessar informação.

### Produto

Oferta materialmente distinta dentro de uma fonte por conteúdo, finalidade, método, cobertura, suporte/resolução, coleção/versão ou condição de acesso.

### Distribuição

Rota concreta para acessar o produto: download, API, serviço geoespacial, catálogo, aplicação ou mecanismo equivalente.

## 3. Elegibilidade territorial

O Brasil é a prioridade. São elegíveis:

- fontes brasileiras com utilidade científica, técnica ou educacional;
- fontes internacionais com cobertura sistemática ou parcial do Brasil;
- excepcionalmente, referências sem cobertura brasileira direta quando houver valor metodológico/comparativo claro.

A classificação P0–P3 organiza prioridade de curadoria e não mede qualidade.

## 4. Evidência

Prioridade:

1. página oficial do produtor;
2. documentação/metadados oficiais;
3. API ou catálogo oficial;
4. metodologia técnica;
5. licença/termos;
6. publicação científica primária quando necessária;
7. documentação técnica institucional;
8. fonte secundária apenas como apoio.

Cada evidência sustenta somente a afirmação que efetivamente contém. Homepage não comprova resolução; página de download não comprova licença; zoom não comprova resolução científica; atualização do portal não define periodicidade do dado.

## 5. Identificação do objeto

Antes de registrar:

1. identificar a fonte/provedor responsável;
2. decidir se o objeto é fonte, produto ou distribuição;
3. verificar se já existe entidade semanticamente equivalente;
4. determinar cobertura brasileira;
5. definir `enumeration_scope` apropriado;
6. registrar apenas propriedades sustentadas.

Catálogo ou API podem ser produtos na Vitrine quando constituem uma oferta materialmente distinta de descoberta/acesso e se enquadram em `product_kind`; isso não os transforma em observações científicas.

> **Regra transitória 2026-09-01:** os passos 1–2 acima são regras do schema legado. Para `DR0001–DR0051`, a classificação ontológica atual deve primeiro determinar o tipo real da entidade e registrar crosswalk antes de qualquer migração.

## 6. Natureza da informação

Sempre que relevante, descrição e limitações devem distinguir:

- observação/medição;
- registro administrativo;
- levantamento/censo;
- estimativa/modelagem;
- classificação;
- interpolação/agregação;
- índice/indicador derivado;
- previsão;
- serviço ou agregador.

Não converter diferenças metodológicas em equivalência sem evidência.

## 7. Espaço

Registrar cobertura, suporte e resolução no nível mais específico disponível. Distinguir:

- ponto, parcela, estação, município, bacia, polígono, célula raster etc.;
- suporte espacial do fenômeno;
- resolução nominal;
- escala cartográfica;
- precisão de coordenada;
- nível de zoom/visualização.

Zoom e tamanho de tile não são resolução científica.

## 8. Tempo

Distinguir:

- cobertura temporal;
- resolução temporal;
- janela de observação/agregação;
- frequência de atualização;
- data de verificação do registro.

Produto previsto, observado, reanalisado e atualizado administrativamente não são equivalentes.

## 9. Acesso e licença

Separar:

- **Site oficial** — identidade institucional ou página oficial principal da fonte (`homepage_url`);
- **Acessar dados** — página onde os dados podem ser pesquisados, visualizados, solicitados ou baixados (`data_access_url`);
- página do produto;
- acesso aos dados;
- metodologia;
- documentação da API;
- distribuição/endpoint;
- licença/termos.

A existência de API não implica gratuidade nem ausência de autenticação. Licença geral do site não é automaticamente licença de cada produto. Quando a licença varia, registrar a variabilidade ou orientar verificação no nível do produto/distribuição.

## 10. Estratégia de enumeração

- `complete` — conjunto relevante enumerado;
- `family_level` — aprofundamento por família;
- `external_index` — catálogo integral permanece externo;
- `representative_sample` — amostra explicitamente incompleta.

A estratégia evita falsa impressão de completude e impede cópia indiscriminada de megacatálogos.

## 11. Qualidade e incerteza

`desconhecido` não equivale a `ausente`. A curadoria deve explicitar, quando relevante:

- incerteza de acesso/licença;
- variação entre produtos;
- vieses de cobertura;
- limites de representatividade;
- diferenças entre observação e derivação;
- risco de interpretação incorreta.

`data/data_quality_report.json` resume preenchimento e lacunas; não é certificado de qualidade dos datasets externos.

## 12. Auditoria

Para cada alteração factual:

`registro atual → evidência oficial/primária → decisão campo a campo → alteração mínima → validação estrutural → diff audit → publicação/verificação quando aplicável`

“Verificado” significa confrontado com evidência na data indicada. Não garante disponibilidade futura.

## 13. Publicação

Os três CSVs são canônicos no schema físico vigente. JSONs e site são derivados deterministicamente. O build público exclui documentação operacional, scripts internos, auditorias e materiais históricos do Simbiotrama.

## 14. Relação com o Simbiotrama

PostgreSQL/PostGIS, releases relacionais, variáveis normalizadas, ativos e Instâncias 1–3 pertencem à história pré-separação ou ao projeto Simbiotrama. Não são etapas obrigatórias da metodologia ativa da Vitrine.

## 15. Princípio de suficiência

A Vitrine deve melhorar continuamente, mas não exige completude absoluta para publicar um snapshot tecnicamente defensável. Lacunas não críticas podem permanecer explícitas; auditoria é proporcional ao risco e deve servir à qualidade do produto, não substituir sua entrega.
