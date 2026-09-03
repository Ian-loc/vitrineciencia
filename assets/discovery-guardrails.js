(() => {
  "use strict";

  const normUrl = value => String(value || "").trim().replace(/\/$/, "").toLowerCase();
  const https = value => /^https:\/\//i.test(String(value || ""));
  const isPdf = value => /\.pdf(?:$|[?#])/i.test(String(value || ""));
  const sameUrl = (a, b) => https(a) && https(b) && normUrl(a) === normUrl(b);
  const DATASET_KINDS = new Set(["dataset", "dataset_series", "indicator_family", "map_layer_collection"]);

  function accessClass(distribution) {
    const text = `${distribution?.distribution_name || ""} ${distribution?.access_protocol || ""} ${distribution?.access_tool || ""} ${distribution?.format || ""}`.toLowerCase();
    const url = String(distribution?.access_url || "");
    if (!https(url)) return "review";
    if (isPdf(url) || /metadad|visualiza|documenta|manual|user guide|notebook|modelo/.test(text)) return "context";
    if (/download|arquivo|geotiff|shapefile|csv|netcdf|parquet/.test(text) || /\.(?:zip|csv|tif|tiff|nc|geojson|gpkg)(?:$|[?#])/i.test(url)) return "download";
    if (/\bapi\b|wfs|wcs|wms|wmts|stac|graphql|earth engine|ckan|rest|opendap|script|python/.test(text)) return "api";
    return "landing";
  }

  function bestDistribution(product) {
    const choices = (product.distributions || []).filter(item => https(item.access_url));
    const priority = {download: 0, api: 1, landing: 2, context: 3, review: 4};
    return choices.sort((a, b) => priority[accessClass(a)] - priority[accessClass(b)])[0] || null;
  }

  function findApiDistribution(product, exceptUrl = "") {
    return (product.distributions || []).find(item =>
      https(item.access_url) && accessClass(item) === "api" && !sameUrl(item.access_url, exceptUrl)
    ) || null;
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

  function appendUniqueAction(container, label, url, className = "action-secondary") {
    if (!container || !https(url)) return null;
    const duplicate = [...container.querySelectorAll("a[href]")].find(link => sameUrl(link.href, url));
    if (duplicate) return duplicate;
    const link = document.createElement("a");
    link.className = className;
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.innerHTML = `${label} <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span>`;
    container.appendChild(link);
    return link;
  }

  function addProvenance(card, text) {
    if (!text || card.querySelector(".provenance-line")) return;
    const description = card.querySelector(".description, .product-description");
    if (!description) return;
    const line = document.createElement("p");
    line.className = "provenance-line";
    line.innerHTML = `<strong>Proveniência:</strong> ${String(text).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]))}`;
    description.insertAdjacentElement("afterend", line);
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
      const actions = card.querySelector(".card-actions");
      const head = card.querySelector(".product-card-head");
      const badge = document.createElement("span");
      badge.className = "entity-role-badge";
      badge.textContent = isDataset ? "Dado científico" : "Serviço/catálogo — infraestrutura";
      if (head) head.insertAdjacentElement("afterend", badge);

      addProvenance(card, product.source?.owner_or_manager || product.source?.resource_name || "");

      let primaryUrl = "";
      if (!isDataset) {
        addNote(card, "Este item é infraestrutura de acesso ou descoberta; não deve ser interpretado como um dataset equivalente aos demais.");
        if (action) {
          action.textContent = product.product_kind.includes("catalog") ? "Abrir catálogo ↗" : "Abrir serviço ↗";
          primaryUrl = action.href;
        }
      } else if (!distribution) {
        addNote(card, "Acesso em revisão: não há uma distribuição HTTPS suficiente registrada para este item.", "review");
        if (action) action.textContent = "Ver página informada ↗";
        primaryUrl = action?.href || "";
      } else {
        const kind = accessClass(distribution);
        primaryUrl = distribution.access_url;
        if (action) {
          action.href = distribution.access_url;
          action.textContent = kind === "download" ? "Dados / download ↗" : kind === "api" ? "Dados / API ↗" : kind === "context" ? "Abrir visualização/documentação ↗" : "Dados / página de acesso ↗";
        }
        if (kind === "context") addNote(card, "A melhor rota registrada é visualização ou documentação; não a trate como download de dados.", "review");
      }

      const apiDistribution = findApiDistribution(product, primaryUrl);
      if (apiDistribution) appendUniqueAction(actions, "API / serviço", apiDistribution.access_url, "action-secondary access-role-api");

      if (https(product.product_page_url) && !sameUrl(product.product_page_url, primaryUrl)) {
        appendUniqueAction(actions, isDataset ? "Página do conjunto" : "Página do item", product.product_page_url, "action-secondary access-role-dataset-page");
      }

      const providerUrl = product.source?.homepage_url;
      if (https(providerUrl) && !sameUrl(providerUrl, primaryUrl) && !sameUrl(providerUrl, product.product_page_url)) {
        appendUniqueAction(actions, "Página do provedor", providerUrl, "action-secondary access-role-provider");
      }

      card.dataset.accessReviewed = "1";
    });
  }

  function sourceDataRole(resource) {
    const url = String(resource.data_access_url || "");
    const text = `${resource.access_protocols || ""} ${resource.data_formats || ""} ${resource.access_conditions || ""} ${url}`.toLowerCase();
    if (!https(url)) return "review";
    if (isPdf(url)) return "context";
    if (/swagger|openapi|graphql|\/api(?:\/|$)|\bwfs\b|\bwcs\b|\bwms\b|stac|ckan|opendap|rest api/.test(text)) return "api";
    if (/download|downloads|baixar|arquivo|csv|geotiff|shapefile|netcdf|parquet/.test(text)) return "data";
    if (/viewer|visualizador|dashboard|painel|mapa interativo/.test(text)) return "viewer";
    return "portal";
  }

  function hasProgrammaticAccess(resource) {
    const value = String(resource.programmatic_access || "").toLowerCase();
    return value === "sim" || value === "parcial";
  }

  function reviewSourceCards(resources, products) {
    const byId = new Map(resources.map(item => [item.resource_id, item]));
    const productCount = new Map();
    products.forEach(product => productCount.set(product.resource_id, (productCount.get(product.resource_id) || 0) + 1));

    document.querySelectorAll("#list .card[data-resource-id]").forEach(card => {
      if (card.dataset.accessReviewed === "1") return;
      const resource = byId.get(card.dataset.resourceId);
      if (!resource) return;

      const actions = card.querySelector(".card-actions");
      const action = actions?.querySelector("a.action-primary");
      const providerAction = actions ? [...actions.querySelectorAll("a[href]")].find(link => sameUrl(link.href, resource.homepage_url)) : null;
      const same = sameUrl(resource.data_access_url, resource.homepage_url);
      const uncertain = ["desconhecido", "não localizado", "não documentado", "não localizada"].includes(String(resource.free_download || "").toLowerCase()) && ["desconhecido", "não documentado"].includes(String(resource.programmatic_access || "").toLowerCase());
      const role = sourceDataRole(resource);

      addProvenance(card, resource.owner_or_manager || resource.official_identity || "");
      if (providerAction) providerAction.textContent = "Página do provedor ↗";

      if (role === "context") {
        addNote(card, "Revisar acesso: o destino informado é um PDF/documento, não uma rota de dados demonstrada.", "review");
        if (action) action.textContent = "Documentação informada ↗";
      } else if (role === "review") {
        addNote(card, "Revisar acesso: não há uma URL HTTPS de dados demonstrada para este registro.", "review");
        if (action) action.textContent = "Acesso em revisão";
      } else if (same) {
        addNote(card, "O acesso informado coincide com a página do provedor; confirme no destino onde os dados podem ser obtidos.", "review");
        if (action) action.textContent = "Página / acesso informado ↗";
      } else if (uncertain) {
        addNote(card, "Acesso parcialmente documentado: download e acesso automatizado ainda não estão esclarecidos no registro.", "review");
        if (action) action.textContent = role === "viewer" ? "Abrir visualizador ↗" : "Dados / portal informado ↗";
      } else if (action) {
        action.textContent = role === "api" ? "API / serviço ↗" : role === "viewer" ? "Abrir visualizador ↗" : role === "data" ? "Dados / download ↗" : "Dados / portal ↗";
      }

      if (hasProgrammaticAccess(resource) && https(resource.access_documentation_url) && !sameUrl(resource.access_documentation_url, resource.data_access_url) && !sameUrl(resource.access_documentation_url, resource.homepage_url)) {
        appendUniqueAction(actions, "API / documentação", resource.access_documentation_url, "action-secondary access-role-api");
      }

      const count = productCount.get(resource.resource_id) || 0;
      if (count && actions && !actions.querySelector(".internal-product-link")) {
        const link = document.createElement("a");
        link.className = "internal-product-link";
        link.href = `products.html?source=${encodeURIComponent(resource.resource_name)}`;
        link.textContent = `${count} ${count === 1 ? "item detalhado" : "itens detalhados"}`;
        actions.appendChild(link);
      }

      card.dataset.accessReviewed = "1";
    });
  }

  const productList = document.querySelector("#product-list");
  if (productList) {
    fetch("data/data_products.json").then(r => r.ok ? r.json() : Promise.reject()).then(products => {
      const apply = () => reviewProductCards(products);
      apply();
      new MutationObserver(apply).observe(productList, {childList: true});
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
      new MutationObserver(apply).observe(sourceList, {childList: true});
    }).catch(() => {});
  }
})();
