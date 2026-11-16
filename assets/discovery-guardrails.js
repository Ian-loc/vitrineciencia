(() => {
  "use strict";

  const https = value => /^https:\/\//i.test(String(value || ""));
  const isPdf = value => /\.pdf(?:$|[?#])/i.test(String(value || ""));
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
      const actions = card.querySelector(".card-actions");
      let primaryUrl = "";
      if (!isDataset) {
        if (action) {
          action.textContent = product.product_kind.includes("catalog") ? "Abrir catálogo ↗" : "Abrir serviço ↗";
          primaryUrl = action.href;
        }
      } else if (!distribution) {
        addNote(card, "Link para obter os dados não confirmado.", "review");
        if (action) action.textContent = "Ver página informada ↗";
        primaryUrl = action?.href || "";
      } else {
        const kind = accessClass(distribution);
        primaryUrl = distribution.access_url;
        if (action) {
          action.href = distribution.access_url;
          action.textContent = kind === "download" ? "Dados / download ↗" : kind === "api" ? "Dados / API ↗" : kind === "context" ? "Abrir visualização/documentação ↗" : "Dados / página de acesso ↗";
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
      new MutationObserver(apply).observe(productList, {childList: true});
    }).catch(() => {});
  }

})();
