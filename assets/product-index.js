(() => {
  "use strict";
  const list = document.querySelector("#product-index-list");
  const count = document.querySelector("#product-index-count");
  const query = document.querySelector("#product-index-q");
  const empty = document.querySelector("#product-index-empty");
  if (!list || !count || !query || !empty) return;

  const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const kindLabels = {
    dataset:"Conjunto de dados", dataset_series:"Série de conjuntos de dados",
    data_service:"Serviço de dados", catalog:"Catálogo", federated_catalog:"Catálogo federado",
    indicator_family:"Família de indicadores", map_layer_collection:"Coleção de camadas cartográficas",
    software_output:"Saída de software"
  };

  let products = [];

  function render() {
    const term = norm(query.value).trim();
    const shown = term ? products.filter(product => norm(`${product.product_name} ${product.source?.resource_name || ""} ${product.product_family || ""}`).includes(term)) : products;
    list.innerHTML = shown.map(product => {
      const source = product.source?.resource_name || "Fonte não informada";
      const kind = product.product_family || kindLabels[product.product_kind] || "Produto de dados";
      const href = /^https:\/\//.test(String(product.product_page_url || "")) ? product.product_page_url : "";
      return `<article class="product-index-row" role="listitem"><div><h3>${esc(product.product_name)}</h3><p class="index-source">${esc(source)}</p></div><div class="index-kind">${esc(kind)}</div><div class="index-actions">${href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">Acessar <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span></a>` : "Sem link direto"}</div></article>`;
    }).join("");
    list.setAttribute("aria-busy", "false");
    empty.hidden = shown.length !== 0;
    count.textContent = term ? `${shown.length} de ${products.length} produtos` : `${products.length} produtos catalogados`;
  }

  fetch("data/data_products.json")
    .then(response => {
      if (!response.ok) throw new Error("Não foi possível carregar os produtos.");
      return response.json();
    })
    .then(data => {
      products = [...data].sort((a,b) => String(a.product_name || "").localeCompare(String(b.product_name || ""), "pt-BR"));
      render();
      query.addEventListener("input", render);
    })
    .catch(error => {
      list.setAttribute("aria-busy", "false");
      count.textContent = "Falha ao carregar produtos";
      list.innerHTML = `<div class="empty"><h3>Falha ao carregar a lista</h3><p>${esc(error.message)}</p></div>`;
    });
})();
