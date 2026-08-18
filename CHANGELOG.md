# Histórico de mudanças

O projeto segue versionamento semântico. A `main` pode avançar entre releases; itens ainda não congelados permanecem em **Não lançado**.

## Não lançado

### Consolidação e expansão — 10 a 18 de agosto de 2026

- contrato público estabilizado em três tabelas: fonte → produto → distribuição;
- catálogo ampliado para **125 fontes, 756 produtos e 787 distribuições** no snapshot de 18/08/2026;
- expansão Brasil-primeiro com novas fontes institucionais e produtos de clima, saúde, energia, sensoriamento remoto, governança fundiária, educação e outros domínios;
- classificação territorial P0–P3 mantida como camada curatorial vinculada às fontes;
- aprofundamento da camada de produtos e distribuições sem aumento do schema 34/24/15;
- inclusão de serviços e produtos OpenWeather com acesso/licença registrados no nível mais específico verificável;
- fortalecimento da validação relacional, papéis de links, build isolado, QA visual e smoke pós-deploy;
- documentação de DOI/release atualizada para tratar a Vitrine como **Dataset** curado e manter `CITATION.cff` em `unreleased` até snapshot explicitamente congelado;
- Drive reafirmado como espelho/histórico derivado; workbook legado reconhecido como não sincronizado com o catálogo atual;
- documentação ativa realinhada em 18/08/2026 para remover referências operacionais obsoletas a 51 fontes, migração para 38 campos e PostgreSQL/PostGIS como destino da Vitrine;
- materiais relacionais anteriores à separação reclassificados como histórico/proveniência do Simbiotrama.

### Separação estrutural — Vitrine Ciência × Simbiotrama — 9 de agosto de 2026

- repositório consolidado como **Vitrine Ciência** (`Ian-loc/vitrineciencia`);
- Vitrine estabelecida como produto público estático independente;
- Simbiotrama passou a possuir repositório próprio `Ian-loc/simbiotrama`;
- PR #70 incorporado à `main` no commit `36211e96edc86fa0e2bb31c703141cd7c5df5480`;
- URL canônica: `https://ian-loc.github.io/vitrineciencia/`;
- workflow de Pages desacoplado de PostgreSQL/PostGIS e jobs do Simbiotrama;
- artefato público limitado à superfície da Vitrine;
- materiais históricos do Simbiotrama preservados sem autoridade operacional sobre a Vitrine.

### Histórico pré-separação

Antes de 09/08/2026, este repositório também abrigou desenvolvimento do Simbiotrama/Simbioscópio, incluindo propostas de PostgreSQL/PostGIS, Instâncias 1–3, roadmaps relacionais, migrações e contratos de comparabilidade. Esses registros permanecem no histórico por proveniência, mas não representam o escopo ativo da Vitrine.

## 0.7.0 — 18 de julho de 2026

- `data/data_resources.csv` consolidado como fonte canônica inicial;
- esquema de fontes ampliado para 34 campos;
- baseline inicial de 51 fontes revisado;
- incorporadas evidências acadêmicas, técnicas e oficiais representativas;
- separados download, acesso programático, protocolos e autenticação;
- adicionadas páginas de catálogo, análise, método e citação;
- adicionados metodologia, codebook, licenças e `CITATION.cff`.

## 0.6.0 — 18 de julho de 2026

- definida a autoridade inicial do CSV no GitHub;
- ampliado o esquema de fontes de 22 para 26 campos;
- revisadas identidade, utilidade, limitações, links e acesso;
- adicionadas validação automática e geração do JSON público.

> Nota: versões 0.6/0.7 e o baseline de 51 fontes são marcos históricos. A `main` atual permanece `unreleased` para a próxima release científica formal.
