(() => {
  "use strict";

  const ACCESS_ORDER = ["A", "B", "C", "D", "E"];
  const ACCESS_LABELS = {
    A: "Arquivos para baixar",
    B: "Página de dados",
    C: "API ou serviço de dados",
    D: "Visualização ou consulta",
    E: "Acesso a confirmar"
  };

  const THEMES = [
    {key:"clima", label:"Clima e mudanças climáticas", terms:["clima","climate","mudancas climaticas","mudança climática","temperatura","precipitacao","chuva","atmosfera","risco climatico"]},
    {key:"hidrologia", label:"Água e hidrologia", terms:["agua","hidrologia","hydrology","recursos hidricos","rio","rios","vazao","bacia hidrografica","water"]},
    {key:"fogo", label:"Fogo e queimadas", terms:["fogo","queimada","queimadas","fire","burned area","area queimada","hotspot","hotspots"]},
    {key:"uso da terra", label:"Uso e cobertura da terra", terms:["uso da terra","cobertura da terra","land use","land cover","lulc"]},
    {key:"desmatamento", label:"Desmatamento e degradação", terms:["desmatamento","deforestation","degradacao","degradation","forest loss"]},
    {key:"vegetação", label:"Vegetação e florestas", terms:["vegetacao","floresta","florestas","vegetation","forest","forests","cobertura vegetal"]},
    {key:"restauração", label:"Restauração e regeneração", terms:["restauracao","regeneracao","restoration","regeneration","regrowth"]},
    {key:"biodiversidade", label:"Biodiversidade e espécies", terms:["biodiversidade","biodiversity","especie","especies","species","ocorrencia","ocorrencias","occurrence","occurrences","taxonomia","taxonomy"]},
    {key:"carbono", label:"Carbono e emissões", terms:["carbono","carbon","emissao","emissoes","emission","emissions","co2","gases de efeito estufa"]},
    {key:"solo", label:"Solos", terms:["solo","solos","soil","soils","pedologia","soil profile","soil profiles"]},
    {key:"agricultura", label:"Agricultura e pecuária", terms:["agricultura","agriculture","pecuaria","livestock","pastagem","pastagens","pasture","pastures","crop","crops"]},
    {key:"territorial", label:"Território e sociedade", terms:["territorio","territorios","territorial","demografia","demographic","demographics","populacao","population","socioeconomico","socioeconomicos","socioeconomica","socioeconomicas","socioeconomic","governanca","governance","municipio","municipios","municipal"]},
    {key:"geoinformação", label:"Bases territoriais e geoespaciais", terms:["geoinformacao","geoespacial","geoespaciais","geospatial","sensoriamento remoto","remote sensing","cartografia","cartography","infraestrutura de dados espaciais","spatial data infrastructure"]}
  ];

  const splitValues = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const flexNorm = value => String(value || "")
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");
  const THEME_BY_KEY = new Map(THEMES.map(theme => [theme.key, theme]));
  const THEME_BY_NORM = new Map(THEMES.map(theme => [flexNorm(theme.key), theme]));
  const themeForQuery = value => THEME_BY_KEY.get(value) || THEME_BY_NORM.get(flexNorm(value)) || null;
  const flexibleContains = (haystack, needle) => {
    const words = new Set(flexNorm(haystack).split(" ").filter(Boolean));
    const tokens = flexNorm(needle).split(" ").filter(Boolean);
    return !tokens.length || tokens.every(token => words.has(token));
  };
  const scientificText = resource => [
    resource.resource_name, resource.acronym, resource.official_identity, resource.description,
    resource.research_areas, resource.keywords, resource.data_product_types,
    resource.academic_uses, resource.geographic_coverage, resource.data_sources
  ].join(" ");
  const themeMatches = (resource, key) => {
    const theme = themeForQuery(key);
    if (!theme) return flexibleContains(searchText(resource), key);
    const text = scientificText(resource);
    return theme.terms.some(term => flexibleContains(text, term));
  };

  // Agrupamentos de descoberta; descrições e ressalvas originais ficam nos cards.
  const COVERAGE_LABELS = {
    global: "Global", brasil: "Brasil — nacional", mg: "Minas Gerais", amazonia: "Amazônia",
    americas: "Américas / América do Sul", eua: "Estados Unidos", outro: "Outros territórios"
  };
  const INFORMATION_GROUPS = [
    ["mapas", "Mapas e camadas geoespaciais", /mapa|camada|raster|vetoria|poligono|mosaico|geometr/],
    ["imagens", "Imagens e produtos de sensoriamento", /imagem|imagens|dossel|missoes/],
    ["series", "Séries e medições", /serie|medic|observa|fluxo|telemetria|meteorolog|climatolog/],
    ["indicadores", "Indicadores e estatísticas", /indicador|estatistic|ranking|tendencia|visualizacao interativa de financiamento/],
    ["inventarios", "Inventários, cadastros e registros", /inventario|cadastro|registro|ocorrencia|checklist|lista|especie|taxonomia|amostra|parcela|horizonte|perfil|traits|abundancia/],
    ["alertas", "Alertas e detecções", /alerta|detecc|foco|risco de fogo/],
    ["modelos", "Modelos, projeções e simulações", /modelo|projec|simulac|reanalise|trajetoria|variaveis bioclimaticas/],
    ["catalogos", "Catálogos, metadados e arquivos", /metadado|dataset|arquivo|pacote|repositorio|link|software/],
    ["relatorios", "Relatórios e documentação", /relatorio|estudo|bibliograf|citac|metodolog|descric/],
    ["paineis", "Painéis e consultas", /painel|grafico|visualiza|consulta/]
  ];
  const INFORMATION_LABELS = Object.fromEntries(INFORMATION_GROUPS.map(([key, label]) => [key, label]));
  INFORMATION_LABELS.outros = "Outras informações";
  const coverageCategory = resource => {
    const text = flexNorm(resource.geographic_coverage);
    if (text.includes("global")) return "global";
    if (text.includes("minas gerais")) return "mg";
    if (text.includes("estados unidos")) return "eua";
    if (text.includes("america")) return "americas";
    if (text.startsWith("regional") && text.includes("amazonia")) return "amazonia";
    if (text.includes("brasil") || text.includes("brazil")) return "brasil";
    return "outro";
  };
  const informationCategories = resource => [...new Set(splitValues(resource.data_product_types).map(value => {
    const text = flexNorm(value);
    return INFORMATION_GROUPS.find(([, , pattern]) => pattern.test(text))?.[0] || "outros";
  }))];
  const coverageMatches = (resource, value) => !value || (COVERAGE_LABELS[value]
    ? coverageCategory(resource) === value : resource.geographic_coverage === value);
  const informationMatches = (resource, value) => !value || (INFORMATION_LABELS[value]
    ? informationCategories(resource).includes(value) : splitValues(resource.data_product_types).includes(value));
  window.VitrineSourceFacets = {coverageCategory, informationCategories, coverageMatches, informationMatches};

  const sourceAccess = window.VitrineSourceAccess;
  let verifiedRoutes = null;
  let informationSelect = null;
  let accessSelect = null;
  let themeSelect = null;

  const routesFor = resource => verifiedRoutes?.get(resource.resource_id) || [];
  const accessModes = resource => sourceAccess.modes(routesFor(resource));
  const accessMatches = resource => !accessSelect.value || accessModes(resource).includes(accessSelect.value);

  function addAccessLink(container, label, url, external = true) {
    const link = document.createElement("a");
    link.className = "action-secondary";
    link.href = url;
    link.textContent = label;
    if (external) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
    container.appendChild(link);
  }

  function decorateAccess(card, resource) {
    const routes = routesFor(resource);
    const modes = accessModes(resource);
    const actions = card.querySelector(".card-actions");
    const labels = {
      A: "Arquivos para baixar",
      B: "Abrir página de dados",
      C: "Ver API ou serviço",
      D: "Abrir visualização ou consulta"
    };
    const urls = new Set();
    for (const mode of modes) {
      if (mode === "E") continue;
      const route = sourceAccess.destination(routes, mode);
      const url = mode === "C" ? `${recordUrl(resource)}#acesso-tecnico` : route.url;
      if (urls.has(url)) continue;
      const customLabel = ["A", "D"].includes(mode) &&
        !["Acessar dados", "Abrir visualizador ou página de consulta"].includes(route.label) ? route.label : null;
      addAccessLink(actions, customLabel || labels[mode], url, mode !== "C");
      urls.add(url);
    }

    if (!actions.children.length) {
      const site = routes.find(route => route.status === "active" && route.roles.includes("official_site") && /^https:\/\//i.test(route.url || ""));
      if (site) addAccessLink(actions, "Abrir site oficial", site.url);
    }
    actions.hidden = !actions.children.length;

    if (modes.length) return modes.map(mode => ACCESS_LABELS[mode]).join(" · ");
    return verifiedRoutes ? "Acesso ainda não descrito" : "Informação de acesso indisponível";
  }

  function populateDerivedSelect(select, entries, emptyLabel, labels = {}) {
    const current = select.value;
    select.innerHTML = `<option value="">${emptyLabel}</option>`;
    entries
      .filter(([, count]) => count > 0)
      .sort((a, b) => {
        const ai = ACCESS_ORDER.indexOf(a[0]);
        const bi = ACCESS_ORDER.indexOf(b[0]);
        if (ai !== -1 || bi !== -1) return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
        return String(labels[a[0]] || a[0]).localeCompare(String(labels[b[0]] || b[0]), "pt-BR");
      })
      .forEach(([value, count]) => {
        const option = new Option(`${labels[value] || value} (${count})`, value);
        option.dataset.label = labels[value] || value;
        select.add(option);
      });
    if (current && ![...select.options].some(option => option.value === current)) {
      const option = new Option(`${labels[current] || current} (0)`, current);
      option.dataset.label = labels[current] || current;
      select.add(option);
    }
    select.value = current;
  }

  function restoreAccessFilter(value) {
    if (!verifiedRoutes || !Object.hasOwn(ACCESS_LABELS, value)) {
      accessSelect.value = "";
      return;
    }
    if (![...accessSelect.options].some(option => option.value === value)) {
      const label = ACCESS_LABELS[value];
      const option = new Option(`${label} (0)`, value);
      option.dataset.label = label;
      accessSelect.add(option);
    }
    accessSelect.value = value;
  }

  function addDerivedActiveFilters(information, access) {
    if (!els.activeFilters) return;
    els.activeFilters.querySelectorAll("[data-derived-filter]").forEach(node => node.remove());
    const items = [];
    if (information.value) items.push(["information", `Informação: ${information.selectedOptions[0]?.dataset.label || information.value}`, information]);
    if (access.value) items.push(["access", `Acesso: ${access.selectedOptions[0]?.dataset.label || ACCESS_LABELS[access.value] || access.value}`, access]);
    items.forEach(([key, label, select]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.derivedFilter = key;
      button.setAttribute("aria-label", `Remover ${label}`);
      button.innerHTML = `${label.replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]))} <b aria-hidden="true">×</b>`;
      button.addEventListener("click", () => {
        select.value = "";
        apply();
        select.focus();
      });
      els.activeFilters.appendChild(button);
    });
    if (items.length) els.activeFilters.hidden = false;
  }

  function decorateCards() {
    const byId = new Map(all.map(resource => [resource.resource_id, resource]));
    document.querySelectorAll("#list .card[data-resource-id]").forEach(card => {
      if (card.querySelector(".discovery-facts")) return;
      const resource = byId.get(card.dataset.resourceId);
      if (!resource) return;
      const description = card.querySelector(".description");
      const actions = card.querySelector(".card-actions");
      const recordAction = card.querySelector(".record-detail-actions");
      const chips = card.querySelector(".chips");
      const provenance = resource.owner_or_manager || resource.official_identity || "Não informada";
      if (!card.querySelector(".provenance-line") && description) {
        const line = document.createElement("p");
        line.className = "provenance-line";
        const strong = document.createElement("strong");
        strong.textContent = "Responsável: ";
        line.append(strong, document.createTextNode(provenance));
        description.insertAdjacentElement("afterend", line);
      }
      if (chips) chips.classList.add("source-topic-chips");
      const facts = document.createElement("dl");
      facts.className = "discovery-facts";
      [
        ["O que oferece", resource.data_product_types || "Não informado"],
        ["Território", resource.geographic_coverage || "Não informado"],
        ["Como acessar", decorateAccess(card, resource)]
      ].forEach(([label, value]) => {
        const item = document.createElement("div");
        const dt = document.createElement("dt");
        const dd = document.createElement("dd");
        dt.textContent = label;
        dd.textContent = value;
        item.append(dt, dd);
        facts.appendChild(item);
      });
      if (recordAction) recordAction.insertAdjacentElement("beforebegin", facts);
      else if (actions) actions.insertAdjacentElement("beforebegin", facts);
    });
  }

  function syncDerivedUrl() {
    const params = new URLSearchParams(location.search);
    informationSelect.value ? params.set("information", informationSelect.value) : params.delete("information");
    accessSelect.value ? params.set("access", accessSelect.value) : params.delete("access");
    const query = params.toString();
    history.replaceState(null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
  }

  function baseMatches(resource, exclude = "") {
    const rawQuery = els.q.value.trim();
    const theme = themeForQuery(rawQuery);
    const queryMatch = !rawQuery || (theme ? themeMatches(resource, theme.key) : flexibleContains(searchText(resource), rawQuery));
    return queryMatch &&
      (exclude === "coverage" || coverageMatches(resource, els.coverage.value)) &&
      (exclude === "information" || informationMatches(resource, informationSelect.value)) &&
      (exclude === "access" || accessMatches(resource));
  }

  function refreshPrimaryFacets() {
    const coverageCounts = new Map();
    all.filter(resource => baseMatches(resource, "coverage")).forEach(resource => {
      const value = coverageCategory(resource);
      if (value) coverageCounts.set(value, (coverageCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(els.coverage, [...coverageCounts.entries()], "Todos os territórios", COVERAGE_LABELS);

    const informationCounts = new Map();
    all.filter(resource => baseMatches(resource, "information")).flatMap(resource => informationCategories(resource)).forEach(value => {
      informationCounts.set(value, (informationCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(informationSelect, [...informationCounts.entries()], "Todos os tipos de informação", INFORMATION_LABELS);

    const accessCounts = new Map();
    all.filter(resource => baseMatches(resource, "access")).forEach(resource => {
      for (const mode of accessModes(resource)) {
        accessCounts.set(mode, (accessCounts.get(mode) || 0) + 1);
      }
    });
    populateDerivedSelect(accessSelect, [...accessCounts.entries()], "Todas as formas de acesso", ACCESS_LABELS);

    if (themeSelect) {
      const current = themeSelect.value;
      const themeCounts = THEMES.map(theme => [theme, all.filter(resource => {
        if (!themeMatches(resource, theme.key)) return false;
        return (coverageMatches(resource, els.coverage.value)) &&
          (informationMatches(resource, informationSelect.value)) &&
          accessMatches(resource);
      }).length]);
      themeSelect.innerHTML = '<option value="">Todos os temas</option>';
      themeCounts.filter(([, count]) => count > 0).forEach(([theme, count]) => themeSelect.add(new Option(`${theme.label} (${count})`, theme.key)));
      if (current && ![...themeSelect.options].some(option => option.value === current)) {
        const theme = themeForQuery(current);
        themeSelect.add(new Option(`${theme?.label || current} (0)`, theme?.key || current));
      }
      const canonicalCurrent = themeForQuery(current)?.key || current;
      themeSelect.value = canonicalCurrent;
    }
  }

  function apply(syncUrl = true) {
    if (!informationSelect || !accessSelect || !all.length) return;
    const rawQuery = els.q.value.trim();
    const theme = themeForQuery(rawQuery);
    filtered = all.filter(resource =>
      (!rawQuery || (theme ? themeMatches(resource, theme.key) : flexibleContains(searchText(resource), rawQuery))) &&
      (coverageMatches(resource, els.coverage.value)) &&
      (informationMatches(resource, informationSelect.value)) &&
      accessMatches(resource)
    );
    sortResults(flexNorm(rawQuery));
    visibleCount = PAGE_SIZE;
    render();
    renderActiveFilters();
    addDerivedActiveFilters(informationSelect, accessSelect);
    decorateCards();
    refreshPrimaryFacets();
    if (syncUrl) {
      writeUrl();
      syncDerivedUrl();
    }
  }

  async function loadVerifiedAccess() {
    try {
      const response = await fetch("data/access_routes.json");
      if (!response.ok) throw new Error("Rotas de acesso indisponíveis");
      verifiedRoutes = sourceAccess.index((await response.json()).routes);
    } catch (error) {
      accessSelect.disabled = true;
      console.error("Falha ao carregar as rotas de acesso", error);
    }
  }

  async function initialize() {
    informationSelect = document.querySelector("#information");
    accessSelect = document.querySelector("#access-role");
    themeSelect = document.querySelector("#source-theme-shortcut");
    if (!informationSelect || !accessSelect || !all.length) {
      window.setTimeout(initialize, 60);
      return;
    }

    await loadVerifiedAccess();

    refreshPrimaryFacets();
    const params = new URLSearchParams(location.search);
    const legacyInformation = params.get("information");
    if (legacyInformation && !INFORMATION_LABELS[legacyInformation] && all.some(resource => splitValues(resource.data_product_types).includes(legacyInformation))) {
      informationSelect.add(new Option(legacyInformation, legacyInformation));
    }
    if ([...els.coverage.options].some(option => option.value === params.get("coverage"))) els.coverage.value = params.get("coverage") || "";
    if ([...informationSelect.options].some(option => option.value === params.get("information"))) informationSelect.value = params.get("information") || "";
    restoreAccessFilter(params.get("access"));

    [informationSelect, accessSelect, els.coverage, els.sort].forEach(element => element.addEventListener("change", () => window.setTimeout(() => apply(), 0)));
    els.activeFilters.addEventListener("click", event => {
      if (event.target.closest("[data-remove]")) window.setTimeout(() => apply(), 0);
    });
    els.q.addEventListener("input", () => window.setTimeout(() => apply(), 0));
    document.querySelector("#clear")?.addEventListener("click", () => window.setTimeout(() => apply(), 0));
    window.addEventListener("popstate", () => window.setTimeout(() => {
      const current = new URLSearchParams(location.search);
      informationSelect.value = [...informationSelect.options].some(option => option.value === current.get("information")) ? (current.get("information") || "") : "";
      restoreAccessFilter(current.get("access"));
      apply(false);
    }, 0));

    apply(false);
    new MutationObserver(decorateCards).observe(els.list, {childList:true});
  }

  initialize();
})();
