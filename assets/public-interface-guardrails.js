(() => {
  "use strict";

  const https = value => /^https:\/\//i.test(String(value || ""));
  const normUrl = value => String(value || "").trim().replace(/\/$/, "").toLowerCase();
  const sameUrl = (a, b) => https(a) && https(b) && normUrl(a) === normUrl(b);
  const technicalAccess = (url, text = "") => /(?:\bapi\b|graphql|opendap|\bwms\b|\bwfs\b|\bwcs\b|wmts|stac|csw|swagger|openapi|earth engine|client librar|endpoint|\brest\b)/i.test(`${url || ""} ${text || ""}`);
  const PUBLIC_ACTIONS = new Set(["Acessar site", "Acessar dados"]);

  function link(label, url, className) {
    if (!https(url)) return null;
    const anchor = document.createElement("a");
    anchor.className = className;
    anchor.href = url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.textContent = label;
    return anchor;
  }

  function cleanTechnicalDetails(card) {
    card.querySelectorAll(".status-badge, .detail").forEach(node => {
      if (/\bapi\b|acesso automatizado|protocolos e ferramentas/i.test(node.textContent || "")) node.remove();
    });
    card.querySelectorAll(".card-details .detail-links a, article.distribution a, .distribution-semantic-role, .entity-role-badge, .semantic-role-line, .semantic-scope-note").forEach(node => node.remove());
  }

  function expectedActions(dataUrl, siteUrl, dataClassName = "action-primary") {
    const expected = [];
    if (https(dataUrl) && !technicalAccess(dataUrl)) expected.push({label:"Acessar dados", url:dataUrl, className:dataClassName});
    if (https(siteUrl) && !technicalAccess(siteUrl) && !sameUrl(siteUrl, dataUrl)) expected.push({label:"Acessar site", url:siteUrl, className:"action-secondary"});
    return expected;
  }

  function visibleLabel(anchor) {
    const clone = anchor.cloneNode(true);
    clone.querySelectorAll(".sr-only").forEach(node => node.remove());
    return (clone.textContent || "").replace(/↗/g, "").trim();
  }

  function actionsMatch(actions, expected) {
    if (!actions) return expected.length === 0;
    const anchors = [...actions.querySelectorAll("a[href]")];
    if (anchors.length !== expected.length) return false;
    return anchors.every((anchor, index) => {
      const label = visibleLabel(anchor);
      return PUBLIC_ACTIONS.has(label) && label === expected[index].label && normUrl(anchor.href) === normUrl(expected[index].url) && !technicalAccess(anchor.href, label);
    });
  }

  function syncActions(actions, expected, before = null) {
    if (!actions) return;
    actions.hidden = expected.length === 0;
    if (actionsMatch(actions, expected)) return;
    actions.querySelectorAll("a[href]").forEach(anchor => anchor.remove());
    expected.forEach(item => {
      const anchor = link(item.label, item.url, item.className);
      if (anchor) actions.insertBefore(anchor, before);
    });
  }

  async function protectProducts() {
    const list = document.querySelector("#product-list");
    if (!list) return;
    try {
      const [products, rolePayload] = await Promise.all([
        fetch("data/data_products.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject()),
        fetch("data/product_distribution_roles.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject())
      ]);
      const productById = new Map((products || []).map(item => [item.product_id, item]));
      const routeRoles = rolePayload.routes || {};

      const safeDataRoute = product => {
        const candidates = (product.distributions || []).map(distribution => ({distribution, meta: routeRoles[distribution.distribution_name] || {}}))
          .filter(({distribution, meta}) => ["A", "B"].includes(meta.access_class) && https(distribution.access_url) && !technicalAccess(distribution.access_url, `${distribution.distribution_name || ""} ${distribution.access_protocol || ""} ${distribution.access_tool || ""}`));
        return candidates.find(({meta}) => meta.access_class === "A") || candidates.find(({meta}) => meta.access_class === "B") || null;
      };

      const apply = () => {
        list.querySelectorAll(".product-card[data-product-id]").forEach(card => {
          const product = productById.get(card.dataset.productId);
          if (!product) return;
          const provenanceLabel = card.querySelector(".provenance-line strong");
          if (provenanceLabel && provenanceLabel.textContent !== "Responsável: ") provenanceLabel.textContent = "Responsável: ";
          const dataRoute = safeDataRoute(product);
          const dataUrl = dataRoute?.distribution?.access_url || "";
          const siteUrl = https(product.product_page_url) && !technicalAccess(product.product_page_url)
            ? product.product_page_url
            : (https(product.source?.homepage_url) && !technicalAccess(product.source.homepage_url) ? product.source.homepage_url : "");
          const actions = card.querySelector(".card-actions");
          syncActions(actions, expectedActions(dataUrl, siteUrl), actions?.querySelector(".compare-toggle") || null);
          cleanTechnicalDetails(card);
          card.querySelectorAll(".access-review-note").forEach(note => {
            if (/infraestrutura|distribui|rota registrada|\bapi\b|visualização|documentação/i.test(note.textContent || "")) note.remove();
          });
          card.dataset.publicActions = "1";
        });
      };

      let scheduled = false;
      const scheduleApply = () => {
        if (scheduled) return;
        scheduled = true;
        setTimeout(() => { scheduled = false; apply(); }, 0);
      };
      apply();
      new MutationObserver(scheduleApply).observe(list, {childList: true, subtree: true});
    } catch (_) {}
  }

  document.addEventListener("DOMContentLoaded", () => {
    protectProducts();
  }, {once: true});
})();
