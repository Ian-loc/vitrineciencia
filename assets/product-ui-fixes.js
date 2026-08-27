(() => {
  "use strict";
  const coverage = document.querySelector("#product-coverage");
  const query = document.querySelector("#product-q");
  if (!coverage || !query) return;

  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();

  // "Brasil" is a structured availability concept, not merely a literal substring
  // of geographic_coverage. Route it through the query interpreter, which correctly
  // accepts products with systematic or partial Brazilian coverage.
  const routeBrazil = () => {
    const value = norm(coverage.value);
    if (value !== "brasil" && value !== "brazil") return;
    if (!/\b(brasil|brazil)\b/i.test(query.value)) query.value = `${query.value.trim()} Brasil`.trim();
    coverage.value = "";
    query.dispatchEvent(new Event("input", {bubbles:true}));
  };
  coverage.addEventListener("change", routeBrazil);
  coverage.addEventListener("search", routeBrazil);

  coverage.placeholder = "Cerrado, Amazônia, Minas Gerais, município…";
})();
