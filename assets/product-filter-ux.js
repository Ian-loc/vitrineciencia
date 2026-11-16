(() => {
  "use strict";

  const facets = ["theme", "coverage", "kind", "access", "source", "format", "free", "temporal", "support", "spatial", "license", ...TECHNICAL_FILTERS];

  function refreshSelect(select, facet, filters) {
    for (const option of select.options) {
      if (!option.value) continue;
      if (!option.dataset.baseLabel) option.dataset.baseLabel = option.textContent.replace(/\s+\(\d+\)$/, "");
      const value = facet === "coverage" ? norm(option.value) : option.value;
      const count = all.filter(product => productMatches(product, {...filters, [facet]: value})).length;
      option.textContent = `${option.dataset.baseLabel} (${count})`;
      const unavailable = count === 0 && option.value !== select.value;
      option.disabled = unavailable;
      option.hidden = unavailable;
    }
  }

  document.addEventListener("vitrine:products-filtered", () => {
    const filters = currentFilters();
    facets.forEach(facet => refreshSelect(els[facet], facet, filters));
  });
})();
