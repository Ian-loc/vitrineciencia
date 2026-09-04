(() => {
  "use strict";

  const CATALOG_PAGE = "sources.html";
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

  const heading = document.querySelector("#catalog-heading");
  const themeStatus = document.querySelector("#source-theme-status");
  const hiddenQuery = document.querySelector("#q");
  const catalog = document.querySelector("#catalogo");

  function renderThemeState(value) {
    const label = THEMES.get(value);
    if (heading) heading.textContent = label ? `Fontes relacionadas a ${label}` : "Fontes e dados disponíveis";
    if (themeStatus) {
      themeStatus.textContent = label
        ? `${label}: veja abaixo as opções disponíveis e refine por território, tipo de informação ou acesso.`
        : "Escolha um tema para começar e refine os resultados conforme a sua pergunta.";
    }
  }

  function applyTheme(value, scroll = true) {
    const controlledValue = THEMES.has(value) ? value : "";
    select.value = controlledValue;
    renderThemeState(controlledValue);

    if (hiddenQuery) {
      hiddenQuery.value = controlledValue;
      hiddenQuery.dispatchEvent(new Event("input", {bubbles: true}));
    } else {
      const next = new URLSearchParams(window.location.search);
      if (controlledValue) next.set("q", controlledValue);
      else next.delete("q");
      const query = next.toString();
      const fallbackPath = location.pathname.endsWith(`/${CATALOG_PAGE}`) ? location.pathname : CATALOG_PAGE;
      history.replaceState(null, "", `${fallbackPath}${query ? `?${query}` : ""}${location.hash}`);
    }

    if (scroll && catalog) {
      catalog.scrollIntoView({block: "start", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"});
    }
  }

  select.addEventListener("change", () => applyTheme(select.value));
  renderThemeState(current);

  const clear = document.querySelector("#clear");
  if (clear) clear.addEventListener("click", () => {
    select.value = "";
    renderThemeState("");
  });

  const activeFilters = document.querySelector("#active-filters");
  if (activeFilters) {
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

  window.addEventListener("popstate", () => {
    const value = (new URLSearchParams(window.location.search).get("q") || "").trim().toLowerCase();
    select.value = THEMES.has(value) ? value : "";
    renderThemeState(select.value);
  });
})();
