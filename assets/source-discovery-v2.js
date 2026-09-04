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

  const splitValues = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  let verifiedAccess = new Map();

  function accessRole(resource) {
    return verifiedAccess.get(resource.resource_id) || "E";
  }

  function populateDerivedSelect(select, values, emptyLabel, labels = {}) {
    const counts = new Map();
    values.filter(Boolean).forEach(value => counts.set(value, (counts.get(value) || 0) + 1));
    const current = select.value;
    select.innerHTML = `<option value="">${emptyLabel}</option>`;
    [...counts.entries()].sort((a, b) => {
      const ai = ACCESS_ORDER.indexOf(a[0]);
      const bi = ACCESS_ORDER.indexOf(b[0]);
      if (ai !== -1 || bi !== -1) return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
      return a[0].localeCompare(b[0], "pt-BR");
    }).forEach(([value, count]) => {
      const option = new Option(`${labels[value] || value} (${count})`, value);
      option.dataset.label = labels[value] || value;
      select.add(option);
    });
    if ([...select.options].some(option => option.value === current)) select.value = current;
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
      if (summary) summary.textContent = "Detalhes técnicos, qualidade e documentação";
    });
  }

  function syncDerivedUrl(information, access) {
    const params = new URLSearchParams(location.search);
    information.value ? params.set("information", information.value) : params.delete("information");
    access.value ? params.set("access", access.value) : params.delete("access");
    const query = params.toString();
    history.replaceState(null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
  }

  let informationSelect = null;
  let accessSelect = null;

  function apply(syncUrl = true) {
    if (!informationSelect || !accessSelect || !all.length) return;
    const query = norm(els.q.value.trim());
    filtered = all.filter(resource =>
      (!query || searchText(resource).includes(query)) &&
      (!els.scope.value || resource._scope.brazil_scope_class === els.scope.value) &&
      (!els.area.value || split(resource.research_areas).includes(els.area.value)) &&
      (!els.brazil.value || resource.covers_brazil === els.brazil.value) &&
      (!els.download.value || resource.free_download === els.download.value) &&
      (!els.programmatic.value || resource.programmatic_access === els.programmatic.value) &&
      (!els.coverage.value || resource.geographic_coverage === els.coverage.value) &&
      (!els.format.value || formats(resource).includes(els.format.value)) &&
      (!els.evidence.value || resource.academic_evidence_type === els.evidence.value) &&
      (!informationSelect.value || splitValues(resource.data_product_types).includes(informationSelect.value)) &&
      (!accessSelect.value || accessRole(resource) === accessSelect.value)
    );
    sortResults(query);
    visibleCount = PAGE_SIZE;
    render();
    renderActiveFilters();
    addDerivedActiveFilters(informationSelect, accessSelect);
    decorateCards();
    if (syncUrl) {
      writeUrl();
      syncDerivedUrl(informationSelect, accessSelect);
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
    if (!informationSelect || !accessSelect || !all.length) {
      window.setTimeout(initialize, 60);
      return;
    }

    await loadVerifiedAccess();
    populateDerivedSelect(informationSelect, all.flatMap(resource => splitValues(resource.data_product_types)), "Todos os tipos de informação");
    populateDerivedSelect(accessSelect, all.map(accessRole), "Todas as formas de acesso", ACCESS_LABELS);
    const params = new URLSearchParams(location.search);
    if ([...informationSelect.options].some(option => option.value === params.get("information"))) informationSelect.value = params.get("information") || "";
    if ([...accessSelect.options].some(option => option.value === params.get("access"))) accessSelect.value = params.get("access") || "";

    informationSelect.addEventListener("change", () => apply());
    accessSelect.addEventListener("change", () => apply());
    [els.q, els.scope, els.area, els.brazil, els.download, els.programmatic, els.coverage, els.format, els.evidence, els.sort].forEach(element => {
      element.addEventListener(element === els.q ? "input" : "change", () => window.setTimeout(() => apply(), 0));
    });
    document.querySelector("#clear")?.addEventListener("click", () => window.setTimeout(() => apply(), 0));
    window.addEventListener("popstate", () => window.setTimeout(() => {
      const current = new URLSearchParams(location.search);
      informationSelect.value = [...informationSelect.options].some(option => option.value === current.get("information")) ? (current.get("information") || "") : "";
      accessSelect.value = [...accessSelect.options].some(option => option.value === current.get("access")) ? (current.get("access") || "") : "";
      apply(false);
    }, 0));

    apply(false);
    new MutationObserver(decorateCards).observe(els.list, {childList: true});
  }

  initialize();
})();