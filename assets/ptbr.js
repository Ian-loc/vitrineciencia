(() => {
  "use strict";

  /*
   * Localização editorial da interface pública da Vitrine Ciência.
   *
   * Regra: a interface, as taxonomias e os termos editoriais da Vitrine são
   * apresentados em português (Brasil). Nomes oficiais de fontes, bases,
   * produtos, serviços, instituições, formatos e protocolos permanecem no
   * idioma adotado pelo provedor quando fazem parte da identidade do recurso.
   * Os valores canônicos dos arquivos CSV/JSON não são alterados aqui.
   */

  const AREA_LABELS = {
    "Agriculture": "Agricultura",
    "Agriculture and livestock": "Agricultura e pecuária",
    "Agriculture and Livestock": "Agricultura e pecuária",
    "Atmospheric science": "Ciências atmosféricas",
    "Biodiversity": "Biodiversidade",
    "Carbon cycle": "Ciclo do carbono",
    "Climate": "Clima",
    "Climate science": "Ciências do clima",
    "Conservation": "Conservação",
    "Data publishing": "Publicação de dados",
    "Demography": "Demografia",
    "Earth and environmental sciences": "Ciências da Terra e ambientais",
    "Earth science": "Ciências da Terra",
    "Ecology": "Ecologia",
    "Economics": "Economia",
    "Ecosystem services": "Serviços ecossistêmicos",
    "Environmental data science": "Ciência de dados ambientais",
    "Environmental monitoring": "Monitoramento ambiental",
    "Environmental science": "Ciências ambientais",
    "Fire ecology": "Ecologia do fogo",
    "Forest ecology": "Ecologia florestal",
    "Forestry": "Ciências florestais",
    "Geography": "Geografia",
    "Geology": "Geologia",
    "Geomorphology": "Geomorfologia",
    "Geospatial computing": "Computação geoespacial",
    "Geospatial information science": "Ciência da informação geoespacial",
    "Geospatial machine learning": "Aprendizado de máquina geoespacial",
    "Hydrology": "Hidrologia",
    "Land use and land cover": "Uso da terra e cobertura do solo",
    "Landscape ecology": "Ecologia da paisagem",
    "Marine ecology": "Ecologia marinha",
    "Natural hazards": "Riscos naturais",
    "Oceanography": "Oceanografia",
    "Protected areas": "Áreas protegidas",
    "Public health": "Saúde pública",
    "Remote sensing": "Sensoriamento remoto",
    "Restoration ecology": "Ecologia da restauração",
    "Savanna ecology": "Ecologia de savanas",
    "Social sciences": "Ciências sociais",
    "Soil science": "Ciência do solo",
    "Socioeconomics": "Socioeconomia",
    "Spatial analysis": "Análise espacial",
    "Species distribution": "Distribuição de espécies",
    "Statistics": "Estatística",
    "Topography": "Topografia",
    "Urban ecology": "Ecologia urbana",
    "Urban studies": "Estudos urbanos",
    "Vegetation dynamics": "Dinâmica da vegetação",
    "Water resources": "Recursos hídricos",
    "Wetland ecology": "Ecologia de áreas úmidas"
  };

  const KIND_LABELS = {
    "Dataset": "Conjunto de dados",
    "Série de datasets": "Série de conjuntos de dados",
    "dataset": "Conjunto de dados",
    "datasets": "Conjuntos de dados",
    "dataset_series": "Série de conjuntos de dados",
    "image_collection": "Coleção de imagens",
    "tiles": "Blocos cartográficos (tiles)",
    "data_service": "Serviço de dados",
    "catalog": "Catálogo",
    "federated_catalog": "Catálogo federado",
    "model_output": "Saída de modelo",
    "query_result": "Resultado de consulta",
    "survey_series": "Série de levantamentos",
    "table": "Tabela"
  };

  const TERM_LABELS = {
    "dataset": "conjunto de dados",
    "datasets": "conjuntos de dados",
    "dataset series": "série de conjuntos de dados",
    "data service": "serviço de dados",
    "data services": "serviços de dados",
    "metadata": "metadados",
    "catalog": "catálogo",
    "catalogue": "catálogo",
    "dashboard": "painel",
    "dashboards": "painéis",
    "viewer": "visualizador",
    "viewers": "visualizadores",
    "web map": "mapa web",
    "web maps": "mapas web",
    "map": "mapa",
    "maps": "mapas",
    "chart": "gráfico",
    "charts": "gráficos",
    "table": "tabela",
    "tables": "tabelas",
    "image": "imagem",
    "images": "imagens",
    "time series": "séries temporais",
    "search": "busca",
    "download": "download",
    "downloads": "downloads",
    "interactive map": "mapa interativo",
    "interactive maps": "mapas interativos",
    "visualization": "visualização",
    "visualizations": "visualizações"
  };

  const STATUS_LABELS = {
    "sim": "Sim",
    "parcial": "Parcial",
    "não": "Não",
    "nao": "Não",
    "desconhecido": "Desconhecido",
    "não se aplica": "Não se aplica",
    "nao se aplica": "Não se aplica"
  };

  const KEYWORD_LABELS = {
    "aboveground biomass": "biomassa acima do solo",
    "agriculture": "agricultura",
    "alerts": "alertas",
    "annual monitoring": "monitoramento anual",
    "Amazon": "Amazônia",
    "amazon": "Amazônia",
    "biodiversity": "biodiversidade",
    "biomes": "biomas",
    "biomass": "biomassa",
    "burned area": "área queimada",
    "carbon": "carbono",
    "climate": "clima",
    "conservation": "conservação",
    "data publishing": "publicação de dados",
    "degradation": "degradação",
    "deforestation": "desmatamento",
    "drought": "seca",
    "emissions": "emissões",
    "environment": "meio ambiente",
    "environmental monitoring": "monitoramento ambiental",
    "experimental": "experimental",
    "fire": "fogo",
    "flood": "inundação",
    "forest": "floresta",
    "forest loss": "perda florestal",
    "geospatial": "geoespacial",
    "governance": "governança",
    "health": "saúde",
    "hydrology": "hidrologia",
    "land cover": "cobertura do solo",
    "land use": "uso da terra",
    "land-use": "uso da terra",
    "livestock": "pecuária",
    "native vegetation": "vegetação nativa",
    "pasture": "pastagem",
    "population": "população",
    "precipitation": "precipitação",
    "rainfall": "chuva",
    "regrowth": "regeneração",
    "remote sensing": "sensoriamento remoto",
    "restoration": "restauração",
    "satellite": "satélite",
    "secondary vegetation": "vegetação secundária",
    "soil": "solo",
    "temperature": "temperatura",
    "urban": "urbano",
    "vegetation": "vegetação",
    "vegetation change": "mudança da vegetação",
    "water": "água"
  };

  const SEARCH_GROUPS = [
    ["biodiversidade", "biodiversity"],
    ["agricultura", "agriculture"],
    ["pecuária", "livestock"],
    ["clima", "climate"],
    ["solo", "soil", "soils"],
    ["água", "water"],
    ["hidrologia", "hydrology"],
    ["recursos hídricos", "water resources"],
    ["floresta", "forest", "forests"],
    ["ecologia florestal", "forest ecology"],
    ["savanas", "savanna", "savanna ecology"],
    ["áreas úmidas", "wetland", "wetland ecology"],
    ["conservação", "conservation"],
    ["sensoriamento remoto", "remote sensing"],
    ["monitoramento ambiental", "environmental monitoring"],
    ["restauração", "restoration", "restoration ecology"],
    ["paisagem", "landscape", "landscape ecology"],
    ["desmatamento", "deforestation", "forest loss"],
    ["uso da terra", "land use", "land-use"],
    ["cobertura do solo", "land cover"],
    ["fogo", "fire", "wildfire"],
    ["queimadas", "burned area", "fire"],
    ["emissões", "emissions"],
    ["carbono", "carbon"],
    ["biomassa", "biomass"],
    ["precipitação", "precipitation", "rainfall"],
    ["temperatura", "temperature"],
    ["seca", "drought"],
    ["inundação", "flood"],
    ["socioeconomia", "socioeconomics"],
    ["população", "population"],
    ["saúde", "health"],
    ["governança", "governance"],
    ["áreas protegidas", "protected areas"],
    ["distribuição de espécies", "species distribution"],
    ["serviços ecossistêmicos", "ecosystem services"],
    ["topografia", "topography"],
    ["geologia", "geology"],
    ["geomorfologia", "geomorphology"],
    ["oceanografia", "oceanography"],
    ["ecologia marinha", "marine ecology"],
    ["ecologia urbana", "urban ecology"],
    ["dinâmica da vegetação", "vegetation dynamics"],
    ["ciência de dados ambientais", "environmental data science"],
    ["computação geoespacial", "geospatial computing"],
    ["aprendizado de máquina geoespacial", "geospatial machine learning"],
    ["ciência da informação geoespacial", "geospatial information science"],
    ["ciências da Terra e ambientais", "earth and environmental sciences"],
    ["publicação de dados", "data publishing"]
  ];

  const norm = value => String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();

  const split = value => String(value || "")
    .split("|")
    .map(item => item.trim())
    .filter(Boolean);

  function exactLabel(map, value) {
    const clean = String(value || "").trim();
    if (!clean) return clean;
    return map[clean] || map[clean.toLowerCase()] || clean;
  }

  function labelArea(value) {
    return exactLabel(AREA_LABELS, value);
  }

  function labelKind(value) {
    return exactLabel(KIND_LABELS, value);
  }

  function labelKeyword(value) {
    return exactLabel(KEYWORD_LABELS, value);
  }

  function labelTerm(value) {
    return exactLabel(TERM_LABELS, value);
  }

  function labelStatus(value) {
    return exactLabel(STATUS_LABELS, value);
  }

  function labelPipeList(value, mapper = labelTerm) {
    return split(value).map(mapper).join(" | ");
  }

  function withCount(text, mapper) {
    const match = String(text || "").match(/^(.*?)(\s+\(\d+\))$/);
    if (!match) return mapper(text);
    return `${mapper(match[1])}${match[2]}`;
  }

  function searchAliases(product) {
    const base = norm([
      product.product_name,
      product.product_family,
      product.product_description,
      product.research_areas,
      product.keywords,
      product.geographic_coverage
    ].join(" "));

    const aliases = SEARCH_GROUPS
      .filter(group => group.some(term => base.includes(norm(term))))
      .flat();

    split(product.research_areas).forEach(area => {
      const translated = labelArea(area);
      if (translated !== area) aliases.push(translated);
    });

    return [...new Set(aliases)].join(" | ");
  }

  /*
   * A busca de produtos usa campos canônicos, muitos deles deliberadamente
   * mantidos no idioma da fonte. Acrescentamos aliases apenas à cópia em
   * memória usada pela busca, sem alterar os arquivos publicados.
   */
  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const input = args[0];
    const url = typeof input === "string" ? input : (input && input.url) || "";
    const response = await originalFetch(...args);
    if (!/data\/data_products\.json(?:[?#].*)?$/.test(url) || !response.ok) return response;

    try {
      const data = await response.clone().json();
      if (!Array.isArray(data)) return response;

      data.forEach(product => {
        const aliases = searchAliases(product);
        if (!aliases) return;
        product.source = product.source || {};
        product.source.official_identity = [product.source.official_identity, aliases]
          .filter(Boolean)
          .join(" | ");
      });

      const headers = new Headers(response.headers);
      headers.delete("content-length");
      headers.delete("content-encoding");
      return new Response(JSON.stringify(data), {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    } catch (error) {
      console.warn("Vitrine Ciência: não foi possível acrescentar aliases de busca em português.", error);
      return response;
    }
  };

  function localizeSelect(selector, mapper) {
    const select = document.querySelector(selector);
    if (!select) return;
    [...select.options].forEach(option => {
      if (!option.value) return;
      const label = mapper(option.value);
      const nextText = withCount(option.textContent, () => label);
      if (option.textContent !== nextText) option.textContent = nextText;
      if (option.dataset.label !== label) option.dataset.label = label;
    });
  }

  function localizeAreaChips(root = document) {
    root.querySelectorAll('.chips[aria-label="Áreas de pesquisa"] .chip').forEach(chip => {
      const translated = labelArea(chip.textContent);
      if (chip.textContent !== translated) chip.textContent = translated;
    });
  }

  function localizeAreaCards(root = document) {
    root.querySelectorAll(".area-card strong").forEach(element => {
      const translated = labelArea(element.textContent);
      if (element.textContent !== translated) element.textContent = translated;
    });
  }

  function localizeKinds(root = document) {
    root.querySelectorAll(".product-card .identity").forEach(element => {
      const text = element.textContent || "";
      Object.entries(KIND_LABELS).some(([source, target]) => {
        const suffix = ` · ${source}`;
        if (!text.endsWith(suffix)) return false;
        const translated = `${text.slice(0, -suffix.length)} · ${target}`;
        if (element.textContent !== translated) element.textContent = translated;
        return true;
      });
    });
  }

  function localizeDetails(root = document) {
    root.querySelectorAll(".detail").forEach(item => {
      const label = item.querySelector("strong");
      const value = item.querySelector("span");
      if (!label || !value) return;
      const name = label.textContent.trim();
      let translated = value.textContent;

      if (name === "Palavras-chave") translated = labelPipeList(value.textContent, labelKeyword);
      if (name === "Produtos" || name === "Visualizações") translated = labelPipeList(value.textContent, labelTerm);

      if (translated && value.textContent !== translated) value.textContent = translated;
    });
  }

  function replaceButtonText(button, text) {
    const textNode = [...button.childNodes].find(node => node.nodeType === Node.TEXT_NODE);
    if (textNode && textNode.textContent !== `${text} `) textNode.textContent = `${text} `;
    const marker = button.querySelector("b");
    if (marker && marker.textContent !== "×") marker.textContent = "×";
    const aria = `Remover ${text}`;
    if (button.getAttribute("aria-label") !== aria) button.setAttribute("aria-label", aria);
  }

  function localizeActiveFilters() {
    const regions = [
      document.querySelector("#product-active-filters"),
      document.querySelector("#active-filters")
    ].filter(Boolean);

    regions.forEach(region => {
      region.querySelectorAll("[data-remove]").forEach(button => {
        const key = button.dataset.remove;
        const current = button.textContent.replace(/\s*×\s*$/, "").trim();
        if (key === "area") {
          const raw = current.replace(/^Área:\s*/, "");
          replaceButtonText(button, `Área: ${labelArea(raw)}`);
        }
        if (key === "kind") {
          const raw = current.replace(/^Tipo:\s*/, "");
          replaceButtonText(button, `Tipo: ${labelKind(raw)}`);
        }
      });
    });
  }

  function localizeInterface(root = document) {
    localizeSelect("#product-area", labelArea);
    localizeSelect("#product-kind", labelKind);
    localizeSelect("#area", labelArea);
    localizeAreaChips(root);
    localizeAreaCards(root);
    localizeKinds(root);
    localizeDetails(root);
    localizeActiveFilters();
  }

  function start() {
    localizeInterface();
    const observer = new MutationObserver(mutations => {
      if (mutations.some(mutation => mutation.addedNodes.length)) localizeInterface();
    });
    observer.observe(document.body, {childList: true, subtree: true});
  }

  window.VitrinePTBR = {
    labelArea,
    labelKind,
    labelKeyword,
    labelTerm,
    labelStatus,
    labelPipeList
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once: true});
  else start();
})();
