(() => {
  "use strict";

  const LABELS = {
    PLATFORM: "Plataforma", SPATIAL_DATA_INFRASTRUCTURE: "Infraestrutura de dados espaciais",
    INFORMATION_SYSTEM: "Sistema de informação", MONITORING_CENTER: "Centro de monitoramento",
    DATA_CATALOG: "Catálogo de dados", DATA_INFRASTRUCTURE: "Infraestrutura de dados",
    DATA_PRODUCTION_INITIATIVE: "Iniciativa de produção de dados", DATA_PLATFORM: "Plataforma de dados",
    MONITORING_PROGRAM: "Programa de monitoramento", BIODIVERSITY_DATA_NETWORK: "Rede de dados de biodiversidade",
    THEMATIC_DATABASE: "Base de dados temática", OFFICIAL_REGISTER: "Cadastro oficial",
    OBSERVATIONAL_DATABASE: "Base de dados observacionais", DATA_CATALOG_AND_PROCESSING_PLATFORM: "Catálogo e plataforma de processamento",
    DATA_EXTRACTION_SERVICE: "Serviço de extração de dados", DATA_CATALOG_AND_SERVICE: "Catálogo e serviço de dados",
    CLIMATE_DATASET_COLLECTION: "Coleção de dados climáticos", CONSERVATION_DATA_PLATFORM: "Plataforma de dados de conservação",
    SPECIES_ASSESSMENT_DATABASE: "Base de avaliações de espécies", BIODIVERSITY_DATA_INFRASTRUCTURE: "Infraestrutura de dados de biodiversidade",
    CITIZEN_SCIENCE_DATA_PLATFORM: "Plataforma de dados de ciência cidadã", RESEARCH_DATA_REPOSITORY_AND_PLATFORM: "Repositório e plataforma de dados de pesquisa",
    ECOLOGICAL_OBSERVATORY: "Observatório ecológico", DATA_REPOSITORY_FEDERATION: "Federação de repositórios de dados",
    RESEARCH_DATA_REPOSITORY: "Repositório de dados de pesquisa", RESEARCH_DATA_REPOSITORY_AND_PUBLISHER: "Repositório e publicador de dados",
    CITIZEN_SCIENCE_PLATFORM: "Plataforma de ciência cidadã", CURATED_DATA_GUIDE: "Guia curado de dados",
    MODELED_SOIL_DATA_SYSTEM: "Sistema de dados modelados de solos", SOIL_PROFILE_DATABASE_AND_SERVICE: "Base e serviço de perfis de solo",
    PUBLISHING_SOFTWARE: "Software de publicação", INTEGRATED_BIODIVERSITY_DATABASE: "Base integrada de biodiversidade",
    OBSERVATION_NETWORK: "Rede de observação", OBSERVATION_NETWORK_AND_DATA_COLLECTION: "Rede de observação e coleção de dados",
    DATA_VISUALIZATION_PLATFORM: "Plataforma de visualização de dados", EMISSIONS_DATABASE: "Base de dados de emissões",
    FEDERATED_DATA_INFRASTRUCTURE: "Infraestrutura federada de dados", RESEARCH_NETWORK_AND_METADATA_INFRASTRUCTURE: "Rede de pesquisa e infraestrutura de metadados",
    RESEARCH_DATA_ARCHIVE: "Arquivo de dados de pesquisa", BIBLIOMETRIC_DATABASE: "Base de dados bibliométrica"
  };

  let registry = new Map();

  function decorate(card) {
    if (card.dataset.semanticDecorated === "true") return;
    const item = registry.get(card.dataset.resourceId);
    const title = card.querySelector(".card-title");
    if (!item || !title) return;

    const semantic = document.createElement("div");
    semantic.className = "semantic-role-line";
    semantic.setAttribute("aria-label", "O que este registro representa");
    const role = document.createElement("span");
    role.className = "semantic-role-badge";
    role.textContent = LABELS[item.entity_type] || item.entity_type.replaceAll("_", " ").toLowerCase();
    semantic.appendChild(role);
    title.appendChild(semantic);
    card.dataset.semanticDecorated = "true";
  }

  function decorateAll() {
    document.querySelectorAll("#list .card[data-resource-id]").forEach(decorate);
  }

  async function init() {
    try {
      const response = await fetch("data/static_core_51_progress.json", {cache: "no-store"});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      registry = new Map((payload.records || []).map(item => [item.resource_id, item]));
      const list = document.querySelector("#list");
      if (!list) return;
      decorateAll();
      new MutationObserver(decorateAll).observe(list, {childList: true});
    } catch (error) {
      console.error("Falha ao carregar papéis semânticos do núcleo", error);
    }
  }

  document.addEventListener("DOMContentLoaded", init, {once: true});
})();
