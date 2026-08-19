(() => {
  "use strict";

  /*
   * Camada de localização da interface pública da Vitrine Ciência.
   * Os valores canônicos e os nomes oficiais das fontes/produtos permanecem
   * inalterados; apenas taxonomias editoriais e termos de interface são
   * apresentados em português (Brasil).
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
    "Ecology": "Ecologia",
    "Ecosystem services": "Serviços ecossistêmicos",
    "Environmental monitoring": "Monitoramento ambiental",
    "Fire ecology": "Ecologia do fogo",
    "Forest ecology": "Ecologia florestal",
    "Forestry": "Ciências florestais",
    "Geology": "Geologia",
    "Geomorphology": "Geomorfologia",
    "Hydrology": "Hidrologia",
    "Land use and land cover": "Uso da terra e cobertura do solo",
    "Landscape ecology": "Ecologia da paisagem",
    "Marine ecology": "Ecologia marinha",
    "Oceanography": "Oceanografia",
    "Protected areas": "Áreas protegidas",
    "Remote sensing": "Sensoriamento remoto",
    "Restoration ecology": "Ecologia da restauração",
    "Savanna ecology": "Ecologia de savanas",
    "Soil science": "Ciência do solo",
    "Socioeconomics": "Socioeconomia",
    "Species distribution": "Distribuição de espécies",
    "Topography": "Topografia",
    "Urban ecology": "Ecologia urbana",
    "Water resources": "Recursos hídricos",
    "Wetland ecology": "Ecologia de áreas úmidas"
  };

  const KIND_LABELS = {
    "Dataset": "Conjunto de dados",
    "Série de datasets": "Série de conjuntos de dados",
    "dataset": "Conjunto de dados",
    "dataset_series": "Série de conjuntos de dados",
    "data_service": "Serviço de dados",
    "catalog": "Catálogo",
    "federated_catalog": "Catálogo federado"
  };

  const KEYWORD_LABELS = {
    "aboveground biomass": "biomassa acima do solo",
    "agriculture": "agricultura",
    "alerts": "alertas",
    "annual monitoring": "monitoramento anual",
    "Amazon": "Amazônia",
    "biodiversity": "biodiversidade",
    "biomes": "biomas",
    "biomass": "biomassa",
    "burned area": "área queimada",
    "carbon": "carbono",
    "climate": "clima",
    "conservation": "conservação",
    "degradation": "degradação",
    "deforestation": "desmatamento",
    "drought": "seca",
    "emissions": "emissões",
    "environmental monitoring": "monitoramento ambiental",
    "experimental": "experimental",
    "fire": "fogo",
    "flood": "inundação",
    "forest": "floresta",
    "forest loss": "perda florestal",
    "governance": "governança",
    "health": "saúde",
    "hydrology": "hidrologia",
    "land cover": "cobertura do solo",
    "land use": "uso da terra",
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
    ["uso da terra", "land use"],
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
    ["ecologia urbana", "urban ecology"]
  ];

  const norm = value => String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();

  const split = value => String(value || "")
    .split("|")
    .map(item => item.trim())
    .filter(Boolean);

  function labelArea(value) {
    const clean = String(value || "").trim();
    if (!clean) return clean;
    return AREA_LABELS[clean] || clean;
  }

  function labelKind(value) {
    const clean = String(value || "").trim();
    return KIND_LABELS[clean] || clean;
  }

  function labelKeyword(value) {
    const clean = String(value || "").trim();
    if (!clean) return clean;
    return KEYWORD_LABELS[clean] || KEYWORD_LABELS[clean.toLowerCase()] || clean;
  }

  function labelPipeList(value, mapper) {
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
   * A busca do catálogo usa campos canônicos, muitos deles deliberadamente
   * mantidos no idioma da fonte. Acrescentamos aliases apenas na cópia em
   * memória usada pela busca, sem alterar os arquivos de dados publicados.
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

  function localizeAreaSelect() {
    const select = document.querySelector("#product-area");
    if (!select) return;
    [...select.options].forEach(option => {
      if (!option.value) return;
      const label = labelArea(option.value);
      const nextText = withCount(option.textContent, () => label);
      if (option.textContent !== nextText) option.textContent = nextText;
      if (option.dataset.label !== label) option.dataset.label = label;
    });
  }

  function localizeKindSelect() {
    const select = document.querySelector("#product-kind");
    if (!select) return;
    [...select.options].forEach(option => {
      if (!option.value) return;
      const label = labelKind(option.dataset.label || option.textContent.replace(/\s+\(\d+\)$/, ""));
      const nextText = withCount(option.textContent, () => label);
      if (option.textContent !== nextText) option.textContent = nextText;
      if (option.dataset.label !== label) option.dataset.label = label;
    });
  }

  function localizeAreaChips(root = document) {
    root.querySelectorAll('.product-card .chips[aria-label="Áreas de pesquisa"] .chip').forEach(chip => {
      const translated = labelArea(chip.textContent);
      if (chip.textContent !== translated) chip.textContent = translated;
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
    root.querySelectorAll(".product-card .detail").forEach(item => {
      const label = item.querySelector("strong");
      const value = item.querySelector("span");
      if (!label || !value) return;
      if (label.textContent.trim() === "Palavras-chave") {
        const translated = labelPipeList(value.textContent, labelKeyword);
        if (translated && value.textContent !== translated) value.textContent = translated;
      }
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
    const region = document.querySelector("#product-active-filters");
    if (!region) return;
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
  }

  function localizeProductInterface(root = document) {
    localizeAreaSelect();
    localizeKindSelect();
    localizeAreaChips(root);
    localizeKinds(root);
    localizeDetails(root);
    localizeActiveFilters();
  }

  function start() {
    if (!document.querySelector("#product-catalog")) return;
    localizeProductInterface();
    const observer = new MutationObserver(mutations => {
      if (mutations.some(mutation => mutation.addedNodes.length)) localizeProductInterface();
    });
    observer.observe(document.body, {childList: true, subtree: true});
  }

  window.VitrinePTBR = {
    labelArea,
    labelKind,
    labelKeyword
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once: true});
  else start();
})();
