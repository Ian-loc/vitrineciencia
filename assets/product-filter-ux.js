(() => {
  "use strict";

  const COVERAGE_GROUPS = [
    ["brasil", "Brasil / cobertura nacional"],
    ["amazonia", "Amazônia"],
    ["cerrado", "Cerrado"],
    ["mata atlantica", "Mata Atlântica"],
    ["caatinga", "Caatinga"],
    ["pantanal", "Pantanal"],
    ["pampa", "Pampa"],
    ["global", "Global"],
    ["variavel", "Variável conforme conjunto ou camada"]
  ];

  const cleanLabel = text => String(text || "").replace(/\s+\(\d+\)$/, "");

  function rebuildCoverage() {
    if (!els.coverage || !all.length) return;
    const current = els.coverage.value;
    const entries = COVERAGE_GROUPS.map(([value, label]) => [
      value,
      label,
      all.filter(product => norm(product.geographic_coverage).includes(norm(value))).length
    ]).filter(([, , count]) => count > 0);
    els.coverage.innerHTML = "";
    els.coverage.add(new Option("Qualquer território", ""));
    entries.forEach(([value, label, count]) => els.coverage.add(new Option(`${label} (${count})`, value)));
    if (current && ![...els.coverage.options].some(option => option.value === current)) {
      els.coverage.add(new Option(`${current} (0)`, current));
    }
    els.coverage.value = current;
  }

  function contextualCount(facet, value) {
    const f = currentFilters();
    if (facet === "theme") f.theme = value;
    if (facet === "coverage") f.coverage = norm(value);
    if (facet === "kind") f.kind = value;
    if (facet === "access") f.access = value;
    const excluded = {theme:"", coverage:"", kind:"", access:""};
    excluded[facet] = f[facet];
    const base = currentFilters();
    base[facet] = "";
    return all.filter(product => {
      const probe = {...base, [facet]: value};
      if (facet === "coverage") probe.coverage = norm(value);
      return productMatches(product, probe);
    }).length;
  }

  function refreshSelect(select, facet) {
    if (!select) return;
    [...select.options].forEach(option => {
      if (!option.value) return;
      if (!option.dataset.baseLabel) option.dataset.baseLabel = cleanLabel(option.textContent);
      const count = contextualCount(facet, option.value);
      option.textContent = `${option.dataset.baseLabel} (${count})`;
      const unavailable = count === 0 && option.value !== select.value;
      option.disabled = unavailable;
      option.hidden = unavailable;
    });
  }

  function refresh() {
    refreshSelect(els.theme, "theme");
    refreshSelect(els.coverage, "coverage");
    refreshSelect(els.kind, "kind");
    refreshSelect(els.access, "access");
  }

  function initialize() {
    if (!all.length || !els.theme || !els.coverage || !els.kind || !els.access) {
      window.setTimeout(initialize, 60);
      return;
    }
    rebuildCoverage();
    refresh();
    [els.theme, els.coverage, els.kind, els.access].forEach(select => {
      select.addEventListener("change", () => window.setTimeout(refresh, 0));
    });
    document.querySelector("#product-clear")?.addEventListener("click", () => window.setTimeout(refresh, 0));
    window.addEventListener("popstate", () => window.setTimeout(refresh, 0));
  }

  initialize();
})();