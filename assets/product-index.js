(() => {
  "use strict";
  const list = document.querySelector("#product-index-list");
  const count = document.querySelector("#product-index-count");
  const query = document.querySelector("#product-index-q");
  const empty = document.querySelector("#product-index-empty");
  if (!list || !count || !query || !empty) return;

  const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const https = value => /^https:\/\//i.test(String(value || ""));
  const technical = value => /(?:\bapi\b|graphql|opendap|\bwms\b|\bwfs\b|\bwcs\b|wmts|stac|csw|swagger|openapi|earth engine|\brest\b)/i.test(String(value || ""));
  const kindLabels = {
    dataset:"Conjunto de dados", dataset_series:"Série de conjuntos de dados",
    data_service:"Serviço de dados", catalog:"Catálogo", federated_catalog:"Catálogo",
    indicator_family:"Família de indicadores", map_layer_collection:"Coleção de camadas cartográficas",
    software_output:"Saída de software"
  };
  let products = [];

  function primaryDataAccess(product) {
    const distributions = (product.distributions || []).filter(item => {
      const text = `${item.distribution_name || ""} ${item.access_protocol || ""} ${item.access_tool || ""} ${item.format || ""}`;
      return https(item.access_url) && !technical(`${item.access_url} ${text}`) && /download|arquivo|dados|csv|geotiff|shapefile|netcdf|parquet|xlsx|zip/i.test(text);
    });
    return distributions[0] || null;
  }

  function render() {
    const term = norm(query.value).trim();
    const shown = term ? products.filter(product => norm(`${product.product_name} ${product.source?.resource_name || ""} ${product.product_family || ""}`).includes(term)) : products;
    list.innerHTML = shown.map(product => {
      const source = product.source?.resource_name || "Fonte não informada";
      const kind = kindLabels[product.product_kind] || product.product_family || "Dado científico";
      const distribution = primaryDataAccess(product);
      const site = https(product.product_page_url) ? product.product_page_url : (https(product.source?.homepage_url) ? product.source.homepage_url : "");
      const href = distribution?.access_url || site;
      const action = distribution ? "Acessar dados / download" : "Acessar site";
      return `<article class="product-index-row" data-product-id="${esc(product.product_id)}" role="listitem"><div><h3>${esc(product.product_name)}</h3><p class="index-source">${esc(source)}</p></div><div class="index-kind">${esc(kind)}</div><div class="index-actions">${href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(action)} <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span></a>` : "Acesso em revisão"}</div></article>`;
    }).join("");
    list.setAttribute("aria-busy", "false");
    empty.hidden = shown.length !== 0;
    count.textContent = term ? `${shown.length} de ${products.length} itens` : `${products.length} itens disponíveis`;
  }

  fetch("data/data_products.json")
    .then(response => { if (!response.ok) throw new Error("Não foi possível carregar os dados."); return response.json(); })
    .then(data => { products = [...data].sort((a,b) => String(a.product_name || "").localeCompare(String(b.product_name || ""), "pt-BR")); render(); query.addEventListener("input", render); })
    .catch(error => { list.setAttribute("aria-busy", "false"); count.textContent = "Falha ao carregar dados"; list.innerHTML = `<div class="empty"><h3>Falha ao carregar a lista</h3><p>${esc(error.message)}</p></div>`; });
})();
