(() => {
  "use strict";

  const https = value => /^https:\/\//i.test(String(value || ""));
  const normUrl = value => String(value || "").trim().replace(/\/$/, "").toLowerCase();
  const sameUrl = (a, b) => https(a) && https(b) && normUrl(a) === normUrl(b);
  const technicalAccess = (url, text = "") => /(?:\bapi\b|graphql|opendap|\bwms\b|\bwfs\b|\bwcs\b|wmts|stac|csw|swagger|openapi|earth engine|client librar|endpoint|\brest\b)/i.test(`${url || ""} ${text || ""}`);
  const PUBLIC_ACTIONS = new Set(["Acessar site", "Acessar dados / download"]);

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
    card.querySelectorAll(".card-details .detail-links a, article.distribution a, .distribution-semantic-role").forEach(node => node.remove());
  }

  function removeNonPublicActions(actions) {
    if (!actions) return;
    actions.querySelectorAll("a[href]").forEach(anchor => {
      const label = (anchor.textContent || "").replace(/↗/g, "").trim();
      if (!PUBLIC_ACTIONS.has(label) || technicalAccess(anchor.href, label)) anchor.remove();
    });
  }

  async function protectSources() {
    const list = document.querySelector("#list");
    if (!list) return;
    try {
      const [audit, resources] = await Promise.all([
        fetch("data/static_core_51_access_audit.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject()),
        fetch("data/data_resources.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject())
      ]);
      const accessById = new Map((audit.records || []).map(item => [item.resource_id, item.access_role]));
      const resourceById = new Map((resources || []).map(item => [item.resource_id, item]));
      const publicAccessLabel = {
        A: "Download de dados",
        B: "Página para obter dados",
        C: "Acesso pelo site",
        D: "Visualização / site",
        E: "Site / acesso a confirmar"
      };

      const apply = () => {
        const accessSelect = document.querySelector("#access-role");
        if (accessSelect) [...accessSelect.options].forEach(option => {
          const label = publicAccessLabel[option.value];
          if (!label) return;
          const count = (option.textContent.match(/\(\d+\)\s*$/) || [""])[0];
          const text = `${label}${count ? ` ${count}` : ""}`;
          if (option.textContent !== text) option.textContent = text;
          option.dataset.label = label;
        });

        list.querySelectorAll(".card[data-resource-id]").forEach(card => {
          const resource = resourceById.get(card.dataset.resourceId);
          if (!resource) return;
          const role = accessById.get(resource.resource_id) || "E";
          const fact = card.querySelector("[data-access-authority]");
          if (fact) fact.textContent = publicAccessLabel[role] || "Acessar site";

          const actions = card.querySelector(".card-actions");
          if (actions) {
            const dataUrl = ["A", "B"].includes(role) && https(resource.data_access_url) && !technicalAccess(resource.data_access_url, `${resource.access_protocols || ""} ${resource.access_documentation_url || ""}`)
              ? resource.data_access_url : "";
            const siteUrl = https(resource.homepage_url) ? resource.homepage_url : "";
            actions.querySelectorAll("a[href]").forEach(anchor => anchor.remove());
            const dataLink = link("Acessar dados / download", dataUrl, "action-primary");
            const siteLink = link("Acessar site", siteUrl, "action-secondary");
            if (dataLink) actions.appendChild(dataLink);
            if (siteLink && !sameUrl(siteUrl, dataUrl)) actions.appendChild(siteLink);
            removeNonPublicActions(actions);
          }
          cleanTechnicalDetails(card);
          card.dataset.publicActions = "1";
        });
      };

      let scheduled = false;
      const scheduleApply = () => {
        if (scheduled) return;
        scheduled = true;
        queueMicrotask(() => { scheduled = false; apply(); });
      };
      apply();
      new MutationObserver(scheduleApply).observe(list, {childList: true, subtree: true});
      document.querySelector("#filters")?.addEventListener("change", () => setTimeout(apply, 0));
    } catch (_) {}
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
          const actions = card.querySelector(".card-actions");
          if (actions) {
            const compare = actions.querySelector(".compare-toggle");
            const dataRoute = safeDataRoute(product);
            const dataUrl = dataRoute?.distribution?.access_url || "";
            const siteUrl = https(product.product_page_url) && !technicalAccess(product.product_page_url)
              ? product.product_page_url
              : (https(product.source?.homepage_url) ? product.source.homepage_url : "");
            actions.querySelectorAll("a[href]").forEach(anchor => anchor.remove());
            const dataLink = link("Acessar dados / download", dataUrl, "action-primary");
            const siteLink = link("Acessar site", siteUrl, "action-secondary");
            if (dataLink) actions.insertBefore(dataLink, compare || null);
            if (siteLink && !sameUrl(siteUrl, dataUrl)) actions.insertBefore(siteLink, compare || null);
            removeNonPublicActions(actions);
          }
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
        queueMicrotask(() => { scheduled = false; apply(); });
      };
      apply();
      new MutationObserver(scheduleApply).observe(list, {childList: true, subtree: true});
    } catch (_) {}
  }

  document.addEventListener("DOMContentLoaded", () => {
    protectSources();
    protectProducts();
  }, {once: true});
})();
