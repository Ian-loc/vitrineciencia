# Vitrine Ciência — roadmap de analytics privacy-first

Status: **PLANNED / NOT IMPLEMENTED**  
Timezone operacional: `America/Sao_Paulo`  
Escopo: `Ian-loc/vitrineciencia`  

## Objetivo

Adicionar, em etapa futura e separada do catálogo científico, uma camada de analytics que permita compreender o uso da Vitrine sem transformar o site em uma superfície de rastreamento individual.

A sequência aprovada é:

**privacy-first analytics → histórico agregado de longo prazo → visão interna de uso → pequeno painel público agregado**.

Nenhum tracker, cookie, beacon, fingerprint ou armazenamento de visitante é autorizado por este documento. A instrumentação só pode começar depois do gate A0.

## Princípios obrigatórios

1. **Minimização** — coletar somente métricas necessárias para avaliar uso, descoberta e acesso aos conteúdos da Vitrine.
2. **Sem identidade individual** — não versionar, exportar ou armazenar no repositório IP, identificador pessoal, fingerprint, sessão individual ou sequência de navegação individualizada.
3. **Sem cookies não essenciais por padrão** — qualquer exceção exige justificativa, documentação e decisão humana explícita.
4. **Privado ≠ público** — métricas operacionais privadas e derivados públicos devem ser tratados como produtos diferentes.
5. **Geografia agregada** — país pode ser considerado quando fornecido de forma agregada e segura; cidade, coordenada ou geografia fina não fazem parte do escopo padrão.
6. **Supressão de células pequenas** — métricas públicas por país, origem ou categoria devem omitir combinações de baixa frequência capazes de facilitar reidentificação.
7. **Reversibilidade** — remover analytics não pode afetar catálogo, busca, filtros, comparação, downloads ou disponibilidade da Pages.
8. **Sem alteração científica** — analytics nunca modifica os CSV/JSON canônicos nem entra na lógica de classificação das fontes/produtos.
9. **Definições explícitas** — pageview, visitante, sessão, download, clique externo e demais métricas precisam de definição antes de qualquer série histórica.
10. **Mudança metodológica registrada** — troca de provedor ou definição deve criar quebra documentada na série, nunca continuidade artificial.

## A0 — contrato de privacidade e seleção do provedor

### Trabalho

- definir exatamente quais métricas são necessárias;
- definir eventos permitidos e proibidos;
- comparar soluções privacy-first e, se pertinente, opção self-hosted;
- avaliar cookies, IP, hashing, fingerprinting, retenção, exportação, jurisdição, custo, disponibilidade da API e possibilidade de desativação;
- definir texto público de privacidade e mecanismo de opt-out quando aplicável;
- decidir como serão tratados bloqueadores de rastreamento e perda amostral sem apresentar métricas como contagem censitária absoluta;
- registrar a decisão arquitetural antes de inserir qualquer script no site.

### Gate A0

Nenhuma instrumentação entra no artefato Pages antes de:

- política de coleta aprovada;
- provedor ou arquitetura aprovados;
- retenção definida;
- exportação agregada testável definida;
- revisão humana explícita.

## A1 — instrumentação mínima

### Métricas candidatas

Somente após A0, considerar:

- pageviews;
- visitantes únicos segundo definição documentada do provedor;
- páginas mais acessadas;
- referrers/origem geral de tráfego;
- país agregado, se disponível sem retenção de localização individual;
- classe de dispositivo/browser em agregação ampla;
- downloads dos CSVs públicos;
- cliques de saída para fonte/produto original;
- uso agregado de áreas, filtros e comparação;
- uso de busca apenas como evento agregado, sem persistir automaticamente texto livre digitado pelo usuário.

### Eventos explicitamente fora do escopo padrão

- IP armazenado ou exportado;
- IDs persistentes de usuário;
- fingerprint de navegador/dispositivo;
- gravação de sessão;
- heatmap individual;
- cidade/coordenada;
- sequência individual de cliques;
- conteúdo integral de consultas de busca;
- qualquer dado inserido pelo usuário em formulário futuro.

### Gate A1

- CI verde;
- smoke pós-deploy verde;
- impacto de performance medido;
- navegação funciona com analytics bloqueado;
- política pública consistente com a implementação;
- inspeção confirma que nenhum dado pessoal foi adicionado a arquivos versionados/logs do projeto.

## A2 — histórico agregado de longo prazo

A retenção histórica deve ser desenhada antes da primeira exportação.

### Regra central

**Guardar agregados, não logs brutos de visitantes.**

### Estrutura mínima sugerida

Um snapshot periódico pode conter, conforme disponibilidade e política aprovada:

- `period_start` / `period_end`;
- pageviews agregados;
- visitantes agregados;
- downloads agregados;
- cliques externos agregados;
- páginas/áreas mais acessadas em categorias estáveis;
- referrers em categorias agregadas;
- países após aplicação do limiar de supressão;
- versão da definição das métricas;
- versão/provedor da instrumentação.

### Requisitos de retenção

- GitHub Actions artifacts não podem ser o único armazenamento de longo prazo;
- o destino durável precisa ser definido e testado antes de chamar o histórico de consolidado;
- dados privados de operação não devem ser incluídos automaticamente no artefato `_site`;
- qualquer derivado público deve passar por um passo explícito de agregação/supressão;
- deve existir teste de restauração/leitura da série histórica.

### Gate A2

- exportação reproduzível;
- retenção durável comprovada;
- esquema documentado;
- minimização auditada;
- nenhuma informação individual no snapshot;
- histórico não interfere no deploy da Vitrine.

## A3 — visão interna de uso

Criar uma visão operacional, inicialmente privada, capaz de responder de forma longitudinal:

- como o uso da Vitrine varia no tempo;
- quais páginas e áreas são mais utilizadas;
- quais produtos/fontes recebem mais cliques de saída;
- quais arquivos são mais baixados;
- quais origens gerais encaminham usuários à Vitrine;
- de quais países vêm acessos agregados, quando disponível e seguro;
- quais mudanças de interface alteram descoberta/uso.

### Regra interpretativa

Analytics mede **interação observada**, não qualidade científica, impacto causal, identidade, instituição, intenção ou perfil do visitante.

## A4 — pequeno painel público agregado

Somente após existir histórico suficiente, definições estáveis e auditoria de privacidade, considerar um painel discreto na interface pública.

### Conteúdo elegível

Poucos indicadores de fácil interpretação, por exemplo:

- visualizações/visitas em período claramente definido;
- visitantes agregados quando metodologicamente comparáveis;
- número de países após supressão de baixa frequência;
- conteúdos ou áreas mais acessados em categorias amplas;
- downloads agregados.

### Conteúdo proibido no painel público

- IP;
- cidade;
- sessão individual;
- usuário;
- sequência de navegação;
- consulta de busca livre;
- browser/dispositivo raro;
- combinação de dimensões com baixa frequência;
- ranking que revele atividade potencialmente individual.

### Princípio visual

O painel público deve ser **pequeno e secundário**. Ele não pode competir com a missão principal: encontrar e comparar fontes e produtos de dados científicos.

## Ordem operacional no workflow da Vitrine

Este roadmap entra **depois do fechamento do QA visual e da estabilidade do deploy atual**.

Ordem:

1. concluir QA visual/publicação;
2. congelar estado funcional da interface;
3. executar A0;
4. implementar A1 em PR próprio;
5. validar comportamento e privacidade em produção;
6. implementar A2 em PR/pacote próprio;
7. acumular histórico suficiente;
8. implementar A3;
9. somente então avaliar A4.

Nenhum pacote downstream deve contornar o gate do predecessor.

## Critérios de qualidade transversais

- timestamps operacionais em `America/Sao_Paulo`;
- analytics assíncrono e não bloqueante;
- falha do provedor não pode quebrar o site;
- nenhuma dependência de analytics no build dos dados científicos;
- toda métrica pública deve informar período e definição;
- toda quebra metodológica deve ser registrada;
- documentação do provedor não substitui teste material da implementação;
- smoke test deve confirmar que a Vitrine funciona com e sem resposta do serviço de analytics.

## Estado atual

**PLANNED / NOT IMPLEMENTED.**

Este documento registra a inclusão do analytics no workflow planejado. Ele não autoriza ativação, coleta ou publicação de métricas antes dos gates definidos acima.
