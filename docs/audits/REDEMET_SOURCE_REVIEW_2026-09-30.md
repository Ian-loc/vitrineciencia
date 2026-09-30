# Revisão de inclusão — REDEMET

**Data:** 2026-09-30  
**Escopo:** inclusão pós-core solicitada explicitamente pelo usuário  
**URL fornecida:** https://redemet.decea.mil.br/

## Decisão

Incluir a **Rede de Meteorologia do Comando da Aeronáutica (REDEMET)** como nova fonte/plataforma do catálogo vivo, com o identificador `DR0136`.

A entidade **não é tratada como um dataset único**. Nesta rodada também não são criados produtos, distribuições ou DataServices específicos. Isso evita converter a homepage institucional/operacional em uma distribuição de dados sem evidência suficiente.

## Identidade e proveniência

A URL fornecida está no domínio institucional `decea.mil.br` e é coerente com a identidade REDEMET/DECEA. Para a Vitrine, a proveniência é registrada como **Departamento de Controle do Espaço Aéreo (DECEA) / Comando da Aeronáutica** e a área científica principal como **Clima e Ciências Atmosféricas**.

## Limite factual desta rodada

A inspeção pública externa da plataforma não pôde ser recertificada nesta sessão. Portanto, não são promovidas como fatos atuais propriedades que exigiriam inspeção direta do portal, tais como:

- catálogo exato de produtos e mensagens disponíveis;
- extensão e persistência das séries históricas;
- formatos de exportação/download;
- existência e documentação de API ou outro acesso programático;
- necessidade de autenticação por rota;
- licença e condições de reutilização;
- cobertura espacial/temporal específica por produto.

No registro canônico, esses itens permanecem como **desconhecidos**, **a confirmar** ou descritos em nível genérico. O campo `last_verified=2026-09-30` registra a revisão do registro; ele não deve ser interpretado como comprovação de acesso aos dados.

## Classificação de acesso

Até recertificação externa, a regra pública aplicável é **E — BROKEN_UNCERTAIN / acesso a confirmar**. A homepage pode ser oferecida como “Acessar site”, mas não como “Acessar dados / download”.

A promoção futura para A, B ou C exige evidência material de uma das seguintes condições:

- **A:** arquivo/diretório/endpoint que entregue dados diretamente;
- **B:** página específica de dataset com mecanismo explícito de obtenção;
- **C:** API/serviço documentado como rota principal de consulta ou extração.

## Identificador

O novo registro usa `DR0136`, e não `DR0052`. O snapshot histórico imutável v1.0.0 já contém identidades próprias em `DR0052–DR0135`. Reutilizar um desses IDs para uma nova entidade quebraria a rastreabilidade entre releases.

## Critério de conclusão da próxima recertificação

A revisão fica completa quando forem verificadas no portal oficial: identidade dos objetos de dados, forma real de obtenção, cobertura e temporalidade, autenticação, formatos, licença/termos e eventual acesso programático. Só então devem ser criados Dataset/Distribution/DataService específicos na Vitrine, se existirem e forem úteis para descoberta científica.
