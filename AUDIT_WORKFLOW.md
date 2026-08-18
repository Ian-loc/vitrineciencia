# Workflow de verificação do catálogo — Vitrine Ciência

## Governança

As três tabelas CSV da `main` são a autoridade. JSONs/site são derivados; Drive é histórico/espelho. Auditoria serve à correção e manutenção do produto, não cria uma autoridade paralela.

## Tipos de auditoria

### Fonte

Verificar:

1. nome, identidade, função e responsável;
2. homepage e rota de acesso;
3. cobertura Brasil e classificação P0–P3;
4. tipos gerais de conteúdo;
5. acesso programático, autenticação e condições;
6. licença no nível que puder ser sustentado;
7. cobertura/resolução/temporalidade apenas quando generalizáveis;
8. evidência representativa e limitações;
9. data de verificação.

### Produto

Verificar:

1. identidade e fonte pai;
2. `product_kind` e `enumeration_scope`;
3. descrição e natureza primária/derivada;
4. cobertura e suporte/resolução;
5. cobertura temporal, resolução temporal e atualização;
6. coleção/versão quando relevante;
7. metodologia e limitações;
8. ao menos uma distribuição válida.

### Distribuição

Verificar:

- URL;
- formato;
- protocolo;
- ferramenta;
- gratuidade;
- autenticação;
- condições;
- licença/atribuição;
- suporte a recorte;
- data de verificação.

## Evidência

Use a fonte mais específica e autoritativa disponível. Uma única página não deve sustentar automaticamente identidade, API, licença, resolução, método e atualização.

Prioridade: documentação oficial → metadados/API oficiais → metodologia/termos → publicação científica primária quando necessária → apoio secundário.

## Decisões

- `manter` — evidência sustenta o valor;
- `corrigir` — evidência sustenta valor diferente;
- `desconhecido/não localizado` — evidência insuficiente;
- `variável` — propriedade não é homogênea no nível representado;
- `fundir/alias/tombstone` — duplicidade material comprovada, com preservação de rastreabilidade;
- `descontinuado/arquivado` — estado sustentado pela fonte.

## Controle automático

```bash
python3 scripts/validate_brazil_scope.py
python3 scripts/validate_product_catalog.py
python3 scripts/build_catalog.py
python3 scripts/audit_link_roles.py --write
python3 scripts/validate_vitrine.py
python3 scripts/build_site_artifact.py
```

Testes de frontend/JavaScript e QA visual são adicionados quando a mudança puder afetar a superfície pública.

## Frequência orientativa

- por pull request: integridade e diff;
- periodicamente: links, autenticação, acesso e disponibilidade;
- por mudança observada: licença, versão, endpoint, responsável ou cobertura;
- por lote de expansão: identidade, duplicidade e classificação territorial;
- antes de release: auditoria focal nos erros materiais e consistência documental.

Não é necessário reauditar todos os registros em toda rodada.

## Interpretação de respostas HTTP

401/403/429 ou bloqueio de robôs não provam indisponibilidade ao usuário. Diferenciar autenticação, quota, WAF/anti-bot e recurso realmente removido.

## Critério de encerramento

Uma auditoria é concluída quando o risco material do escopo foi resolvido ou explicitamente documentado, os validadores aplicáveis passam e não há evidência de que novas verificações mudariam materialmente a decisão naquele momento.
