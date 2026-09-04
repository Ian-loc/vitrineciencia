(() => {
  "use strict";

  const LABELS = {
    PLATFORM:"Plataforma", SPATIAL_DATA_INFRASTRUCTURE:"Infraestrutura de dados espaciais", INFORMATION_SYSTEM:"Sistema de informação", MONITORING_CENTER:"Centro de monitoramento", DATA_CATALOG:"Catálogo de dados", DATA_INFRASTRUCTURE:"Infraestrutura de dados", DATA_PRODUCTION_INITIATIVE:"Iniciativa de produção de dados", DATA_PLATFORM:"Plataforma de dados", MONITORING_PROGRAM:"Programa de monitoramento", BIODIVERSITY_DATA_NETWORK:"Rede de dados de biodiversidade", THEMATIC_DATABASE:"Base de dados temática", OFFICIAL_REGISTER:"Cadastro oficial", OBSERVATIONAL_DATABASE:"Base de dados observacionais", DATA_CATALOG_AND_PROCESSING_PLATFORM:"Catálogo e plataforma de processamento", DATA_EXTRACTION_SERVICE:"Serviço de extração de dados", DATA_CATALOG_AND_SERVICE:"Catálogo e serviço de dados", CLIMATE_DATASET_COLLECTION:"Coleção de dados climáticos", CONSERVATION_DATA_PLATFORM:"Plataforma de dados de conservação", SPECIES_ASSESSMENT_DATABASE:"Base de avaliações de espécies", BIODIVERSITY_DATA_INFRASTRUCTURE:"Infraestrutura de dados de biodiversidade", CITIZEN_SCIENCE_DATA_PLATFORM:"Plataforma de dados de ciência cidadã", RESEARCH_DATA_REPOSITORY_AND_PLATFORM:"Repositório e plataforma de dados de pesquisa", ECOLOGICAL_OBSERVATORY:"Observatório ecológico", DATA_REPOSITORY_FEDERATION:"Federação de repositórios de dados", RESEARCH_DATA_REPOSITORY:"Repositório de dados de pesquisa", RESEARCH_DATA_REPOSITORY_AND_PUBLISHER:"Repositório e publicador de dados", CITIZEN_SCIENCE_PLATFORM:"Plataforma de ciência cidadã", CURATED_DATA_GUIDE:"Guia curado de dados", MODELED_SOIL_DATA_SYSTEM:"Sistema de dados modelados de solos", SOIL_PROFILE_DATABASE_AND_SERVICE:"Base e serviço de perfis de solo", PUBLISHING_SOFTWARE:"Software de publicação", INTEGRATED_BIODIVERSITY_DATABASE:"Base integrada de biodiversidade", OBSERVATION_NETWORK:"Rede de observação", OBSERVATION_NETWORK_AND_DATA_COLLECTION:"Rede de observação e coleção de dados", DATA_VISUALIZATION_PLATFORM:"Plataforma de visualização de dados", EMISSIONS_DATABASE:"Base de dados de emissões", FEDERATED_DATA_INFRASTRUCTURE:"Infraestrutura federada de dados", RESEARCH_NETWORK_AND_METADATA_INFRASTRUCTURE:"Rede de pesquisa e infraestrutura de metadados", RESEARCH_DATA_ARCHIVE:"Arquivo de dados de pesquisa", BIBLIOMETRIC_DATABASE:"Base de dados bibliométrica"
  };

  const ACCESS = {
    A:"Download / arquivo de dados",
    B:"Página específica para obter dados",
    C:"API / serviço de dados",
    D:"Visualização ou documentação",
    E:"Acesso em revisão"
  };

  let registry = new Map();
  let accessRegistry = new Map();

  function decorate() {
    document.querySelectorAll("#list .card[data-resource-id]").forEach(card => {
      const item = registry.get(card.dataset.resourceId);
      if (!item) return;
      const accessRole = accessRegistry.get(card.dataset.resourceId) || "E";
      const description = card.querySelector(".description");
      if (description && !card.querySelector(".semantic-role-line")) {
        const line = document.createElement("p");
        line.className = "semantic-role-line";
        const strong = document.createElement("strong");
        strong.textContent = "O que este registro é: ";
        line.append(strong, document.createTextNode(LABELS[item.entity_type] || item.entity_type.replaceAll("_", " ").toLowerCase()));
        description.insertAdjacentElement("beforebegin", line);
      }

      const facts = card.querySelector(".discovery-facts");
      if (facts) {
        [...facts.querySelectorAll("div")].forEach(row => {
          const dt = row.querySelector("dt");
          const dd = row.querySelector("dd");
          if (dt?.textContent.trim() === "Distribuição / acesso" && dd) {
            const expected = `${accessRole} · ${ACCESS[accessRole] || "Acesso não classificado"}`;
            if (dd.textContent !== expected) dd.textContent = expected;
            if (dd.dataset.accessAuthority !== "static_core_51_access_audit") {
              dd.dataset.accessAuthority = "static_core_51_access_audit";
            }
          }
        });
      }

      if (item.note && !card.querySelector(".semantic-scope-note")) {
        const actions = card.querySelector(".card-actions");
        if (actions) {
          const note = document.createElement("p");
          note.className = "semantic-scope-note";
          note.textContent = item.note;
          actions.insertAdjacentElement("beforebegin", note);
        }
      }
    });
  }

  async function init() {
    try {
      const [semanticResponse, accessResponse] = await Promise.all([
        fetch("data/static_core_51_progress.json", {cache:"no-store"}),
        fetch("data/static_core_51_access_audit.json", {cache:"no-store"})
      ]);
      if (!semanticResponse.ok) throw new Error(`semantic HTTP ${semanticResponse.status}`);
      if (!accessResponse.ok) throw new Error(`access HTTP ${accessResponse.status}`);
      const semanticPayload = await semanticResponse.json();
      const accessPayload = await accessResponse.json();
      registry = new Map((semanticPayload.records || []).map(item => [item.resource_id, item]));
      accessRegistry = new Map((accessPayload.records || []).map(item => [item.resource_id, item.access_role]));
      const list = document.querySelector("#list");
      if (!list) return;
      decorate();
      new MutationObserver(decorate).observe(list, {childList:true});
    } catch (error) {
      console.error("Falha ao carregar as camadas semântica e de acesso verificadas", error);
    }
  }

  document.addEventListener("DOMContentLoaded", init, {once:true});
})();
