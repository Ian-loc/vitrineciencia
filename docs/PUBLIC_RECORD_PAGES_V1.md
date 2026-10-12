# Páginas públicas de registro — contrato v1

**Status:** implementado e publicado; contrato de transição para o modelo público v2  
**Atualização:** 12 de outubro de 2026  
**Unidade persistente:** Registro da Vitrine (`DR####`)  
**Rota:** `/registros/<resource_id em minúsculas>/`

## 1. O que está implementado

A Vitrine publica uma página persistente para cada um dos 58 registros vivos.

O build gera:

- `/registros/dr####/` — HTML;
- `/data/registros/dr####.json` — read model individual;
- `/data/public_records.json` — índice público completo.

HTML e JSON derivam do mesmo objeto.

Produtos, coleções, versões, distribuições, serviços, visualizadores e documentos ficam subordinados ao registro e não geram página própria por padrão.

## 2. Decisão que permanece válida

Não criar uma página pública para cada:

- dataset técnico;
- arquivo;
- formato;
- endpoint;
- versão;
- asset;
- cena;
- camada;
- pluma;
- documento.

A página do registro é uma superfície agregadora estável da curadoria da Vitrine.

## 3. Refinamento conceitual posterior ao v1

O v1 usa tipos públicos como “Iniciativa”, “Plataforma” ou “Base” diretamente no objeto do registro.

A análise posterior mostrou que é mais preciso separar:

```
Registro da Vitrine
        │ descreve
        ▼
Recurso catalogado
```

O `DR####` é o registro catalográfico mantido pela Vitrine.

O recurso externo pode ser uma iniciativa, plataforma, catálogo, infraestrutura, base, rede, observatório ou outro objeto científico/institucional.

Essa correção é alvo de `public-record-v2`.

**As URLs atuais não devem mudar.**

## 4. Estrutura atual das páginas

A versão v1 contém:

- Sobre este registro;
- Como acessar;
- O que você encontra aqui;
- Cobertura espacial e temporal;
- Produtos, coleções e versões;
- Possibilidades de uso em pesquisa;
- Cuidados e limitações;
- Proveniência;
- Condições de uso e licença;
- Referências e documentação;
- Curadoria da Vitrine.

Essa estrutura é funcional, mas ainda reflete parcialmente o esquema físico.

## 5. Estrutura desejada na próxima revisão

A página deverá convergir para cinco blocos:

1. **Visão geral** — o que é o recurso, para que serve, temas e abrangência;
2. **Dados e produtos disponíveis** — ofertas científicas reais, sem confundir arquivos e serviços;
3. **Como acessar** — download, página de dados, API, Earth Engine, viewer, catálogo ou documentação;
4. **Como interpretar** — cobertura, escala, temporalidade, metodologia, comparabilidade e limitações;
5. **Proveniência, condições e referências** — produtores, mantenedores, licenças, documentação e evidência.

“Sobre este registro na Vitrine” permanece ao final como bloco discreto de curadoria.

## 6. Cards e páginas

Com a existência das páginas individuais, os cards de `sources.html` não precisam repetir toda a ficha técnica.

Próxima mudança esperada:

- card = descoberta e triagem;
- página individual = compreensão e acesso;
- provedor externo = dado/documentação original.

O acordeão técnico dos cards deverá ser simplificado na origem em vez de depender de limpeza posterior por guardrails.

## 7. Rotas de acesso

No v1, as rotas são construídas principalmente a partir de:

- `homepage_url`;
- `data_access_url`;
- `access_documentation_url`;
- evidências;
- classificação A–E.

A próxima etapa deve transformar rotas em objetos canônicos próprios, permitindo múltiplas formas de acesso sem inferência no renderer.

A classe A–E continuará sendo uma **avaliação de acesso**, e não deve ser confundida com a ação principal da interface.

## 8. Produtos, versões e distribuições

O modelo físico `DR → DP → DD` permanece por compatibilidade.

No futuro:

- produto/oferta científica representa significado;
- versão/coleção representa estado citável/reprodutível;
- distribuição representa entrega concreta;
- DataService representa serviço de consulta/processamento;
- viewer e documentação mantêm papéis próprios.

Nada disso implica páginas adicionais por padrão.

## 9. Relação com a futura API

O v1 já materializa um read model estático.

O padrão planejado é `static-first / stale-while-revalidate`:

1. servir snapshot;
2. verificar freshness;
3. solicitar refresh assíncrono quando necessário;
4. validar mudanças;
5. promover estado aceito.

Endpoint conceitual futuro:

`GET /api/v1/records/{resource_id}`

Ele ainda não existe como serviço em produção.

## 10. Persistência e QA

Devem permanecer invariantes:

- uma página por DR vivo;
- canonical próprio;
- conteúdo primário disponível sem API externa;
- sitemap completo;
- JSON individual;
- build reprodutível;
- desconhecido nunca convertido em negativo;
- produtos apenas quando materialmente registrados;
- falha do provedor não indisponibiliza a página.

O contrato v2 deverá preservar essas propriedades.

Plano de evolução: `docs/WEB_API_EVOLUTION_PLAN.md`.
