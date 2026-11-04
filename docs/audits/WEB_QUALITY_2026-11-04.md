# Manutenção de qualidade da interface — 04/11/2026

Escopo: correções do cliente estático e clareza documental. PR: https://github.com/Ian-loc/vitrineciencia/pull/287.

## Correções

- A inicial anunciava 51 no acesso ao catálogo apesar de carregar 58 fontes. Contadores agora são preenchidos no build, inclusive sem JavaScript, e atualizados pelo cliente.
- A contagem de obtenção usava somente a auditoria do núcleo histórico. Passa a consultar `data/access_routes.json`: 41 recursos com rota principal A/B, entre os 58 atuais.
- Navegação padronizada: Explorar dados; Dados detalhados; Sobre a Vitrine; Sobre o acervo.
- Territórios e tipos de informação agrupados somente para descoberta. Os textos canônicos originais e ressalvas permanecem nos cards; parâmetros legados continuam aceitos. Contagens de informação não duplicam fontes com termos sinônimos.
- Inicial e catálogo usam a mesma escolha do destino de acesso rápido. Documentação não substitui uma rota de acesso existente; a FJP deixa de apontar ao PDF de evidência como se fosse o site de acesso.
- Limitações dos itens detalhados podem ser abertas no próprio card. O subconjunto explicita suas duas origens e a presença de conjuntos, catálogos e serviços.
- O panorama distingue gratuidade e existência de uma rota para obter dados.

## Verificação

As quatro etapas locais de `pages.yml` foram executadas: corpus/derivados, interface, build/compatibilidade e fronteira pública. As 58 URLs, 11 offerings e 19 distribuições foram preservadas.

`validate_discovery_quality.cjs` verifica contagens derivadas, destinos de acesso, agrupamentos, compatibilidade de filtros e rótulos de navegação. O workflow visual inclui consulta das limitações, filtro Minas Gerais, combinação com mapas, recarga e limpeza em desktop/tablet/celular. Resultados e imagens ficam vinculados ao PR.

Não se trata de recertificação integral das 58 fontes externas. Valores científicos, identidades, licenças, release e DOI não foram modificados.

## Drive

O índice do espelho recebe este registro de manutenção, preservando a data e o escopo da comparação integral de 12/10. A planilha e CSVs não precisam ser regenerados porque as tabelas canônicas não mudaram. O histórico permanece preservado e identificado no índice.
