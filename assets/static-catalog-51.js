(() => {
  "use strict";

  const select = document.querySelector("#source-theme-shortcut");
  if (!select) return;

  const THEMES = new Map([
    ["clima", "Clima e mudanças climáticas"],
    ["hidrologia", "Água e hidrologia"],
    ["fogo", "Fogo e queimadas"],
    ["uso da terra", "Uso e cobertura da terra"],
    ["desmatamento", "Desmatamento e degradação"],
    ["vegetação", "Vegetação e florestas"],
    ["restauração", "Restauração e regeneração"],
    ["biodiversidade", "Biodiversidade e espécies"],
    ["carbono", "Carbono e emissões"],
    ["solo", "Solos"],
    ["agricultura", "Agricultura e pecuária"],
    ["territorial", "Território e sociedade"],
    ["geoinformação", "Bases territoriais e geoespaciais"]
  ]);

  const params = new URLSearchParams(window.location.search);
  const current = (params.get("q") || "").trim().toLowerCase();
  if (THEMES.has(current)) select.value = current;

  function destination(value) {
    const next = new URLSearchParams(window.location.search);
    if (value) next.set("q", value);
    else next.delete("q");
    const query = next.toString();
    return `sources.html${query ? `?${query}` : ""}#catalogo`;
  }

  select.addEventListener("change", () => {
    window.location.assign(destination(select.value));
  });

  const heading = document.querySelector("#catalog-heading");
  const themeLabel = THEMES.get(current);
  if (heading && themeLabel) heading.textContent = `Fontes relacionadas a ${themeLabel}`;

  const themeStatus = document.querySelector("#source-theme-status");
  if (themeStatus) {
    themeStatus.textContent = themeLabel
      ? `Tema ativo: ${themeLabel}. O filtro usa termos controlados nos metadados do núcleo de 51 registros.`
      : "Escolha um tema científico para restringir o núcleo de 51 registros sem usar busca textual livre.";
  }

  const activeFilters = document.querySelector("#active-filters");
  if (activeFilters && themeLabel) {
    const relabel = () => {
      activeFilters.querySelectorAll("button, span").forEach(element => {
        if (element.childElementCount === 0 && element.textContent.trim().startsWith("Busca:")) {
          element.textContent = element.textContent.replace(/^Busca:/, "Tema:");
        }
      });
    };
    relabel();
    new MutationObserver(relabel).observe(activeFilters, {childList: true, subtree: true});
  }
})();
