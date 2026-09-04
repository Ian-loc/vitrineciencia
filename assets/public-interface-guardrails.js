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

  function formatDate(value) {
    const match = String(value || "").match(/^(\d{4})-(\d{2})-(\d{2})$/);
    return match ? `${match[3]}/${match[2]}/${match[1]}` : String(value || "");
  }

  function cleanTechnicalDetails(card) {
    card.querySelectorAll(".status-badge, .detail").forEach(node => {
      if (/\bapi\b|acesso automatizado|protocolos e ferramentas/i.test(node.textContent || "")) node.remove();
    });
    card.querySelectorAll(".card-details .detail-links a, article.distribution a, .distribution-semantic-role, .entity-role-badge, .semantic-role-line, .semantic-scope-note").forEach(node => node.remove());
  }

  function expectedActions(dataUrl, siteUrl) {
    const expected = [];
    if (https(dataUrl) && !technicalAccess(dataUrl)) expected.push({label:"Acessar dados / download", url:dataUrl, className:"action-primary"});
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
    if (!actions || actionsMatch(actions, expected)) return;
    actions.querySelectorAll("a[href]").forEach(anchor => anchor.remove());
    expected.forEach(item => {
      const anchor = link(item.label, item.url, item.className);
      if (anchor) actions.insertBefore(anchor, before);
    });
  }

  function ensureSourceEvidence(card, auditItem, publicLabel) {
    const provenance = card.querySelector(".provenance-line");
    const provenanceLabel = provenance?.querySelector("strong");
    if (provenanceLabel && provenanceLabel.textContent !== "Responsável: ") provenanceLabel.textContent = "Responsável: ";

    card.querySelectorAll(".discovery-facts > div").forEach(row => {
      const dt = row.querySelector("dt");
      const dd = row.querySelector("dd");
      if (!dt || !dd) return;
      if (/Distribuição\s*\/\s*acesso|Como acessar/i.test(dt.textContent || "")) {
        dt.textContent = "Como acessar";
        dd.textContent = publicLabel;
      }
    });

    const verified = formatDate(auditItem?.source_last_verified);
    if (verified) {
      let line = card.querySelector(".verification-line");
      if (!line) {
        line = document.createElement("p");
        line.className = "verification-line";
        (provenance || card.querySelector(".description"))?.insertAdjacentElement("afterend", line);
      }
      if (line.textContent !== `Acesso verificado em ${verified}`) line.textContent = `Acesso verificado em ${verified}`;
    }
  }

  async function protectSources() {
    const list = document.querySelector("#list");
    if (!list) return;
    try {
      const [audit, resources] = await Promise.all([
        fetch("data/static_core_51_access_audit.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject()),
        fetch("data/data_resources.json", {cache: "no-store"}).then(r => r.ok ? r.json() : Promise.reject())
      ]);
      const auditById = new Map((audit.records || []).map(item => [item.resource_id, item]));
      const resourceById = new Map((resources || []).map(item => [item.resource_id, item]));
      const publicAccessLabel = {
        A: "Dados para download",
        B: "Página para obter dados",
        C: "Acesso pelo site",
        D: "Visualização / site",
        E: "Acesso a confirmar"
      };

      const apply = () => {
        const accessSelect = document.querySelector("#access-role");
        if (accessSelect) [...accessSelect.options].forEach(option => {
          const label = publicAccessLabel[option.value];
          if (!label) return;
          const count = (option.textContent.match(/\(\d+\)\s*$/) || [""])[0];
          const text = `${label}${count ? ` ${count}` : ""}`;
          if (option.textContent !== text) option.textContent = text;
          if (option.dataset.label !== label) option.dataset.label = label;
        });

        list.querySelectorAll(".card[data-resource-id]").forEach(card => {
          const resource = resourceById.get(card.dataset.resourceId);
          if (!resource) return;
          const auditItem = auditById.get(resource.resource_id) || {};
          const role = auditItem.access_role || "E";
          const publicLabel = publicAccessLabel[role] || "Acesso a confirmar";
          const fact = card.querySelector("[data-access-authority]");
          if (fact && fact.textContent !== publicLabel) fact.textContent = publicLabel;
          ensureSourceEvidence(card, auditItem, publicLabel);

          const dataUrl = ["A", "B"].includes(role) && https(resource.data_access_url) && !technicalAccess(resource.data_access_url, `${resource.access_protocols || ""} ${resource.access_documentation_url || ""}`)
            ? resource.data_access_url : "";
          const siteUrl = https(resource.homepage_url) && !technicalAccess(resource.homepage_url) ? resource.homepage_url : "";
          syncActions(card.querySelector(".card-actions"), expectedActions(dataUrl, siteUrl));
          cleanTechnicalDetails(card);
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
      document.querySelector("#filters")?.addEventListener("change", scheduleApply);
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
    protectSources();
    protectProducts();
  }, {once: true});
})();
