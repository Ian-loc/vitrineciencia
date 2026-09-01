(() => {
  "use strict";
  const normUrl = value => String(value || "").trim().replace(/\/$/, "").toLowerCase();
  const https = value => /^https:\/\//i.test(String(value || ""));
  const isPdf = value => /\.pdf(?:$|[?#])/i.test(String(value || ""));
  const DATASET_KINDS = new Set(["dataset", "dataset_series", "indicator_family", "map_layer_collection"]);

  function accessClass(distribution) {
    const text = `${distribution?.distribution_name || ""} ${distribution?.access_protocol || ""} ${distribution?.access_tool || ""} ${distribution?.format || ""}`.toLowerCase();
    const url = String(distribution?.access_url || "");
    if (!https(url)) return "review";
    if (isPdf(url) || /metadad|visualiza|documenta|manual|user guide/.test(text)) return "context";
    if (/download|arquivo|geotiff|shapefile|csv|netcdf|parquet/.test(text) || /\.(?:zip|csv|tif|tiff|nc|geojson|gpkg)(?:$|[?#])/i.test(url)) return "download";
    if (/\bapi\b|wfs|wcs|earth engine|ckan|rest|script|python/.test(text)) return "api";
    return "landing";
  }

  function bestDistribution(product) {
    const choices = (product.distributions || []).filter(item => https(item.access_url));
    const priority = {download:0, api:1, landing:2, context:3, review:4};
    return choices.sort((a,b) => priority[accessClass(a)] - priority[accessClass(b)])[0] || null;
  }

  function addNote(card, text, level = "info") {
    let note = card.querySelector(".access-review-note");
    if (!note) {
      note = document.createElement("p");
      note.className = "access-review-note";
      const actions = card.querySelector(".card-actions") || card.querySelector(".product-card-bottom") || card;
      actions.insertAdjacentElement("beforebegin", note);
    }
    note.dataset.level = level;
    note.textContent = text;
  }

  function reviewProductCards(products) {
    const byId = new Map(products.map(item => [item.product_id, item]));
    document.querySelectorAll("#product-list .product-card[data-product-id]").forEach(card => {
      if (card.dataset.accessReviewed === "1") return;
      const product = byId.get(card.dataset.productId);
      if (!product) return;
      const isDataset = DATASET_KINDS.has(product.product_kind);
      const distribution = bestDistribution(product);
      const action = card.querySelector(".card-actions a.action-primary");
      const head = card.querySelector(".product-card-head");
      const badge = document.createElement("span");
      badge.className = "entity-role-badge";
      badge.textContent = isDataset ? "Dado científico" : "Serviço/catálogo — apoio à descoberta";
      if (head) head.insertAdjacentElement("afterend", badge);

      if (!isDataset) {
        addNote(card, "Este registro é infraestrutura de acesso ou descoberta; não deve ser interpretado como um dataset equivalente aos demais.");
        if (action) action.textContent = product.product_kind.includes("catalog") ? "Abrir catálogo ↗" : "Abrir serviço ↗";
      } else if (!distribution) {
        addNote(card, "Acesso em revisão: não há uma distribuição HTTPS suficiente registrada para este produto.", "review");
        if (action) action.textContent = "Ver página informada ↗";
      } else {
        const kind = accessClass(distribution);
        if (action) {
          action.href = distribution.access_url;
          action.textContent = kind === "download" ? "Acessar download ↗" : kind === "api" ? "Consultar dados/API ↗" : "Acessar dados ↗";
        }
        if (kind === "context") addNote(card, "A rota principal registrada parece ser visualização ou documentação; confirme onde os dados podem ser obtidos antes do uso.", "review");
      }
      card.dataset.accessReviewed = "1";
    });
  }

  function reviewSourceCards(resources, products) {
    const byId = new Map(resources.map(item => [item.resource_id, item]));
    const productCount = new Map();
    products.forEach(product => productCount.set(product.resource_id, (productCount.get(product.resource_id) || 0) + 1));
    document.querySelectorAll("#list .card[data-resource-id]").forEach(card => {
      if (card.dataset.accessReviewed === "1") return;
      const resource = byId.get(card.dataset.resourceId);
      if (!resource) return;
      const action = card.querySelector(".card-actions a.action-primary");
      const same = https(resource.data_access_url) && normUrl(resource.data_access_url) === normUrl(resource.homepage_url);
      const uncertain = ["desconhecido", "não localizado", "não documentado", "não localizada"].includes(String(resource.free_download || "").toLowerCase()) && ["desconhecido", "não documentado"].includes(String(resource.programmatic_access || "").toLowerCase());
      if (isPdf(resource.data_access_url)) {
        addNote(card, "Revisar acesso: o destino informado é um PDF/documento, não uma rota de dados demonstrada.", "review");
        if (action) action.textContent = "Abrir documento informado ↗";
      } else if (!https(resource.data_access_url)) {
        addNote(card, "Revisar acesso: não há uma URL HTTPS de dados demonstrada para esta fonte.", "review");
        if (action) action.textContent = "Acesso em revisão";
      } else if (same) {
        addNote(card, "Revisar acesso: site institucional e acesso aos dados apontam para o mesmo destino; confirme se a página permite obter os dados.", "review");
        if (action) action.textContent = "Ver acesso informado ↗";
      } else if (uncertain) {
        addNote(card, "Acesso parcialmente documentado: download e acesso automatizado ainda não estão esclarecidos no registro.", "review");
        if (action) action.textContent = "Ver acesso informado ↗";
      } else if (action) {
        action.textContent = "Ver acesso informado ↗";
      }

      const count = productCount.get(resource.resource_id) || 0;
      if (count) {
        const actions = card.querySelector(".card-actions");
        if (actions && !actions.querySelector(".internal-product-link")) {
          const link = document.createElement("a");
          link.className = "internal-product-link";
          link.href = `products.html?source=${encodeURIComponent(resource.resource_name)}`;
          link.textContent = `Ver ${count} ${count === 1 ? "produto" : "produtos"} no núcleo`;
          actions.appendChild(link);
        }
      }
      card.dataset.accessReviewed = "1";
    });
  }

  const productList = document.querySelector("#product-list");
  if (productList) {
    fetch("data/data_products.json").then(r => r.ok ? r.json() : Promise.reject()).then(products => {
      const apply = () => reviewProductCards(products);
      apply();
      new MutationObserver(apply).observe(productList, {childList:true});
    }).catch(() => {});
  }

  const sourceList = document.querySelector("#list");
  if (sourceList) {
    Promise.all([
      fetch("data/data_resources.json").then(r => r.ok ? r.json() : Promise.reject()),
      fetch("data/data_products.json").then(r => r.ok ? r.json() : [])
    ]).then(([resources, products]) => {
      const apply = () => reviewSourceCards(resources, products);
      apply();
      new MutationObserver(apply).observe(sourceList, {childList:true});
    }).catch(() => {});
  }
})();
