# Direção científica — Vitrine Ciência

**Status:** vigente  
**Atualização:** 1º de setembro de 2026

## Missão

A Vitrine Ciência deve facilitar a descoberta e o acesso a **dados científicos úteis**, sobretudo ecológicos, ambientais e socioecológicos relevantes ao Brasil, sem reproduzir desnecessariamente a complexidade interna dos provedores.

A Vitrine é uma camada de descoberta, curadoria e encaminhamento. Não é, por padrão, repositório integral dos dados externos nem plataforma destinada a esmiuçar cada recurso técnico disponível.

## Ordem de descoberta

A experiência pública deve priorizar:

**pergunta científica → fenômeno/processo → território → tempo/escala → dataset/coleção utilizável → forma de acesso → provedor/proveniência**.

Busca livre não é o mecanismo principal. Filtros controlados e termos científicos consistentes têm prioridade.

## Modelo conceitual em revisão

A estrutura histórica `Fonte → Produto → Distribuição` não é assumida como ontologia final.

A auditoria dos 51 registros legados deve separar, quando aplicável:

- instituição/provedor;
- programa/iniciativa;
- plataforma;
- catálogo/repositório;
- infraestrutura de dados;
- dataset/coleção;
- distribuição;
- serviço de dados/API;
- portal/visualizador.

Um mesmo sistema pode desempenhar vários papéis, mas esses papéis devem ser explicitados em relações, não comprimidos sob o rótulo genérico `fonte`.

## Princípios científicos

1. **Utilidade antes de granularidade.** A Vitrine deve orientar o usuário ao dado útil, não multiplicar microprodutos técnicos sem ganho real de descoberta.
2. **Dado ≠ serviço ≠ visualização ≠ documentação.** Esses objetos devem permanecer distintos.
3. **Proveniência explícita.** O provedor e a documentação original permanecem referências primárias.
4. **Acesso verificável.** Um link só é tratado como acesso a dados quando efetivamente conduz a download, dataset, serviço de extração ou rota equivalente comprovada.
5. **Sem inferência silenciosa.** Ausência de evidência permanece desconhecida ou em revisão.
6. **Granularidade mínima suficiente.** Nova entidade científica apenas quando a distinção melhora materialmente descoberta, interpretação ou acesso.
7. **Escopo Brasil.** Fontes nacionais e internacionais são relevantes quando oferecem dados úteis sobre o Brasil; origem não é nota de qualidade.
8. **Curadoria antes de automação.** APIs podem acelerar descoberta e atualização, mas não decidem sozinhas o que deve ser publicado.

## Federação: posição atual

A arquitetura federada é objetivo de consolidação, não estado implementado. A ordem correta é:

**auditoria ontológica 51/51 → Integration Registry → pipeline comum → MapBiomas Alerta → pilotos heterogêneos → publicação controlada**.

Dados científicos permanecem, em regra, nos provedores; a Vitrine deve armazenar o necessário para descoberta, proveniência, curadoria e acesso.

## Critério de sucesso

A Vitrine é satisfatória quando um usuário consegue partir de um fenômeno/processo, localizar um dataset adequado, entender provedor/cobertura essencial e chegar a uma rota real de acesso aos dados; e quando o mantenedor consegue reconstruir o catálogo e distinguir claramente publicado, quarentena e motivo da decisão.
