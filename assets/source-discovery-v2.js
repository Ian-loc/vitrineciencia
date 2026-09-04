(() => {
  "use strict";

  const ACCESS_ORDER = ["A", "B", "C", "D", "E"];
  const ACCESS_LABELS = {
    A: "Download / arquivo de dados",
    B: "Página específica para obter dados",
    C: "API / serviço de dados",
    D: "Visualização ou documentação",
    E: "Acesso em revisão"
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

  let verifiedAccess = new Map();
  let informationSelect = null;
  let accessSelect = null;
  let themeSelect = null;

  function accessRole(resource) {
    return verifiedAccess.get(resource.resource_id) || "E";
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
      const chips = card.querySelector(".chips");
      const status = card.querySelector(".status-grid");
      const provenance = resource.owner_or_manager || resource.official_identity || "Não informada";
      if (!card.querySelector(".provenance-line") && description) {
        const line = document.createElement("p");
        line.className = "provenance-line";
        const strong = document.createElement("strong");
        strong.textContent = "Proveniência: ";
        line.append(strong, document.createTextNode(provenance));
        description.insertAdjacentElement("afterend", line);
      }
      if (chips) chips.classList.add("source-topic-chips");
      const facts = document.createElement("dl");
      facts.className = "discovery-facts";
      [
        ["O que oferece", resource.data_product_types || "Não informado"],
        ["Território", resource.geographic_coverage || "Não informado"],
        ["Distribuição / acesso", `${accessRole(resource)} · ${ACCESS_LABELS[accessRole(resource)]}`]
      ].forEach(([label, value]) => {
        const item = document.createElement("div");
        const dt = document.createElement("dt");
        const dd = document.createElement("dd");
        dt.textContent = label;
        dd.textContent = value;
        if (label === "Distribuição / acesso") dd.dataset.accessAuthority = "static_core_51_access_audit";
        item.append(dt, dd);
        facts.appendChild(item);
      });
      if (actions) actions.insertAdjacentElement("beforebegin", facts);
      if (status) status.hidden = true;
      const summary = card.querySelector(".card-details summary");
      if (summary) summary.textContent = "Detalhes científicos, técnicos e documentação";
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
      (exclude === "coverage" || !els.coverage.value || resource.geographic_coverage === els.coverage.value) &&
      (exclude === "information" || !informationSelect.value || splitValues(resource.data_product_types).includes(informationSelect.value)) &&
      (exclude === "access" || !accessSelect.value || accessRole(resource) === accessSelect.value);
  }

  function refreshPrimaryFacets() {
    const coverageCounts = new Map();
    all.filter(resource => baseMatches(resource, "coverage")).forEach(resource => {
      const value = resource.geographic_coverage;
      if (value) coverageCounts.set(value, (coverageCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(els.coverage, [...coverageCounts.entries()], "Todos os territórios");

    const informationCounts = new Map();
    all.filter(resource => baseMatches(resource, "information")).flatMap(resource => splitValues(resource.data_product_types)).forEach(value => {
      informationCounts.set(value, (informationCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(informationSelect, [...informationCounts.entries()], "Todos os tipos de informação");

    const accessCounts = new Map();
    all.filter(resource => baseMatches(resource, "access")).forEach(resource => {
      const value = accessRole(resource);
      accessCounts.set(value, (accessCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(accessSelect, [...accessCounts.entries()], "Todas as formas de acesso", ACCESS_LABELS);

    if (themeSelect) {
      const current = themeSelect.value;
      const themeCounts = THEMES.map(theme => [theme, all.filter(resource => {
        if (!themeMatches(resource, theme.key)) return false;
        return (!els.coverage.value || resource.geographic_coverage === els.coverage.value) &&
          (!informationSelect.value || splitValues(resource.data_product_types).includes(informationSelect.value)) &&
          (!accessSelect.value || accessRole(resource) === accessSelect.value);
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
      (!els.coverage.value || resource.geographic_coverage === els.coverage.value) &&
      (!informationSelect.value || splitValues(resource.data_product_types).includes(informationSelect.value)) &&
      (!accessSelect.value || accessRole(resource) === accessSelect.value)
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
      const response = await fetch("data/static_core_51_access_audit.json", {cache:"no-store"});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      verifiedAccess = new Map((payload.records || []).map(item => [item.resource_id, item.access_role]));
    } catch (error) {
      verifiedAccess = new Map();
      console.error("Falha ao carregar a matriz auditada de acesso; classificação conservadora E aplicada", error);
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

    const informationCounts = new Map();
    all.flatMap(resource => splitValues(resource.data_product_types)).forEach(value => informationCounts.set(value, (informationCounts.get(value) || 0) + 1));
    populateDerivedSelect(informationSelect, [...informationCounts.entries()], "Todos os tipos de informação");
    const accessCounts = new Map();
    all.forEach(resource => {
      const value = accessRole(resource);
      accessCounts.set(value, (accessCounts.get(value) || 0) + 1);
    });
    populateDerivedSelect(accessSelect, [...accessCounts.entries()], "Todas as formas de acesso", ACCESS_LABELS);

    const params = new URLSearchParams(location.search);
    if ([...informationSelect.options].some(option => option.value === params.get("information"))) informationSelect.value = params.get("information") || "";
    if ([...accessSelect.options].some(option => option.value === params.get("access"))) accessSelect.value = params.get("access") || "";

    [informationSelect, accessSelect, els.coverage].forEach(element => element.addEventListener("change", () => window.setTimeout(() => apply(), 0)));
    els.q.addEventListener("input", () => window.setTimeout(() => apply(), 0));
    document.querySelector("#clear")?.addEventListener("click", () => window.setTimeout(() => apply(), 0));
    window.addEventListener("popstate", () => window.setTimeout(() => {
      const current = new URLSearchParams(location.search);
      informationSelect.value = [...informationSelect.options].some(option => option.value === current.get("information")) ? (current.get("information") || "") : "";
      accessSelect.value = [...accessSelect.options].some(option => option.value === current.get("access")) ? (current.get("access") || "") : "";
      apply(false);
    }, 0));

    apply(false);
    new MutationObserver(decorateCards).observe(els.list, {childList:true});
  }

  initialize();
})();