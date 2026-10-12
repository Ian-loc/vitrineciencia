# Metodologia de curadoria — Vitrine Ciência

**Status:** vigente  
**Atualização:** 12 de outubro de 2026

## 1. Escopo

A Vitrine Ciência é um catálogo científico curado de descoberta e acesso a dados relevantes ao Brasil.

Ela organiza informação suficiente para que o usuário compreenda:

- o que é o recurso;
- que dados/produtos oferece;
- onde e quando se aplicam;
- como acessá-los;
- quem os produz, mantém ou publica;
- quais limitações e condições de uso precisam ser consideradas.

A Vitrine não hospeda, por padrão, cópias integrais dos datasets externos.

## 2. Unidade pública e unidade descrita

A unidade persistente da interface é o **Registro da Vitrine** (`DR####`).

O registro descreve um **Recurso catalogado** externo.

O recurso pode ser iniciativa, programa, plataforma, catálogo, infraestrutura, base, coleção, rede, observatório, guia ou outro objeto justificável pela evidência.

Essa distinção deverá ser explicitada estruturalmente no modelo público v2.

## 3. Produtos, versões e distribuições

### Produto/oferta científica

É uma oferta materialmente distinta por significado, finalidade, método, cobertura, variável, série ou condição científica relevante.

### Versão/coleção

É um estado distinguível quando a mudança importa para citação, comparação ou reprodutibilidade.

### Distribuição

É uma forma concreta de entrega do conteúdo.

### Serviço de dados

É um mecanismo de consulta, extração ou processamento. Não é automaticamente um novo produto.

### Viewer/documentação

São superfícies de visualização ou explicação e não devem ser confundidas com distribuição sem evidência.

## 4. Princípio de granularidade mínima suficiente

Criar nova entidade apenas quando a distinção melhora materialmente:

- descoberta;
- interpretação;
- proveniência;
- versionamento;
- reprodutibilidade;
- acesso.

Formato, arquivo, tile, banda, endpoint ou página alternativa não criam produto por conveniência.

## 5. Elegibilidade territorial

O Brasil é a prioridade.

São elegíveis:

- recursos brasileiros;
- recursos internacionais com cobertura sistemática;
- recursos com cobertura parcial relevante;
- referências comparativas excepcionalmente justificadas.

A classificação P0–P3 organiza cobertura/prioridade, não qualidade.

## 6. Evidência

Ordem preferencial:

1. página oficial do produtor;
2. documentação/metadados oficiais;
3. API/catálogo oficial;
4. metodologia técnica;
5. licença/termos;
6. publicação científica primária;
7. documentação institucional;
8. fonte secundária apenas como apoio.

Cada evidência sustenta somente a afirmação que efetivamente demonstra.

## 7. Identificação antes do registro

Antes de criar ou alterar uma entrada:

1. identificar o objeto real;
2. identificar agentes e papéis;
3. verificar duplicação;
4. determinar relevância territorial;
5. identificar ofertas científicas relevantes;
6. separar versões e formas de acesso;
7. registrar somente propriedades sustentadas;
8. escolher a granularidade mínima suficiente.

## 8. Natureza da informação

Distinguir, quando relevante:

- observação/medição;
- registro administrativo;
- levantamento/censo;
- estimativa/modelagem;
- classificação;
- interpolação;
- índice/indicador;
- previsão;
- agregação;
- serviço.

Não converter diferenças metodológicas em equivalência.

## 9. Espaço

Distinguir:

- cobertura;
- suporte espacial;
- resolução;
- escala cartográfica;
- precisão;
- zoom/visualização.

Zoom e tile não são resolução científica.

## 10. Tempo

Distinguir:

- cobertura temporal;
- resolução temporal;
- janela de observação;
- frequência de atualização;
- data de emissão/versão;
- atualização informada pelo provedor;
- verificação pela Vitrine;
- alteração do registro interno.

Essas datas não são equivalentes.

## 11. Acesso

Separar:

- site oficial;
- página de dados;
- download direto;
- API/DataService;
- visualizador;
- catálogo;
- metodologia;
- documentação de acesso;
- licença/termos.

HTTP 200 não comprova acesso.

A autoridade estrutural atual das rotas é `data/access_routes.json`. Os campos legados abaixo permanecem sincronizados durante a migração, mas o read model v2 não precisa mais inferir o papel de cada URL a partir deles.

No schema físico legado, os dois papéis mínimos continuam documentados explicitamente:

- **Site oficial** (`homepage_url`) — identidade institucional ou página oficial principal do recurso;
- **Acessar dados** (`data_access_url`) — melhor rota cadastrada para descobrir, consultar, solicitar ou obter os dados, cuja função concreta é qualificada pela auditoria de acesso.

A existência de API não implica gratuidade, autorização para harvesting ou licença de redistribuição.

## 12. Licença e atribuição

Licença deve ser registrada no nível mais específico conhecido.

Condições do site, produto, distribuição e serviço podem divergir.

Quando a licença varia, declarar a variabilidade e orientar o usuário ao nível correto.

## 13. Proveniência

Evitar reduzir proveniência a um único “responsável”.

Papéis relevantes incluem:

- produtor;
- mantenedor;
- publicador;
- host;
- distribuidor;
- responsável metodológico.

Esses papéis deverão ser estruturados progressivamente.

A autoridade inicial é `data/provenance_assertions.json`. O baseline preserva `owner_or_manager` como afirmação agrupada e não separa automaticamente organizações a partir de barras, ponto e vírgula ou conjunções. Papéis mais específicos exigem evidência.

A autoridade inicial de versões/coleções é `data/product_versions.json`. O modelo distingue versão explicitamente nomeada, edição/ano e estados descritivos como catálogo corrente, serviço corrente ou configuração de acesso; estes últimos não devem ser apresentados como versões citáveis.

## 14. Estratégia de enumeração

- `complete`;
- `family_level`;
- `external_index`;
- `representative_sample`.

O objetivo é evitar falsa completude e a cópia indiscriminada de megacatálogos.

## 15. Qualidade e incerteza

`desconhecido` não equivale a `não`.

A curadoria deve explicitar:

- incerteza de acesso;
- variação entre produtos;
- limitações metodológicas;
- vieses de cobertura;
- comparabilidade entre versões;
- licenças variáveis;
- restrições de autenticação.

## 16. Auditoria

Fluxo mínimo de alteração factual:

`estado atual → evidência → decisão → alteração mínima → validação → diff → publicação/verificação`

“Verificado” significa confrontado com evidência na data indicada. Não garante disponibilidade futura.

## 17. Publicação

Os CSVs e matrizes de auditoria permanecem canônicos no schema físico atual.

HTML e JSON são derivados.

A página pública não deve ser corrigida manualmente em desacordo com a fonte canônica.

## 18. Federação futura

Automação deve seguir:

`fetch → raw/staging → normalize → deduplicate → classify → verify → diff → curation gate → publish`

Nenhum resultado bruto de API é publicado diretamente.

O catálogo público continua legível se o provedor estiver indisponível.

## 19. Revalidação

A futura revalidação sob demanda deve respeitar freshness/TTL, cooldown, autenticação e rate limits.

Abrir uma página não implica uma requisição externa obrigatória.

## 20. Princípio de suficiência

A Vitrine não exige completude absoluta para publicar um registro defensável.

É preferível explicitar uma lacuna do que inventar precisão.

Referências operacionais:

- `docs/PROJECT_STATE.md`;
- `WORKFLOW_STATUS.md`;
- `CODEBOOK.md`;
- `docs/WEB_API_EVOLUTION_PLAN.md`.
