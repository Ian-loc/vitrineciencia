(() => {
  const ROLE_LABELS = {
    DISTRIBUTION: "Distribuição de dados",
    DATASERVICE: "DataService",
    VIEWER_SERVICE: "Serviço de visualização",
    METADATA_SERVICE: "Serviço de metadados",
    CATALOG: "Catálogo",
    DOCUMENTATION_METADATA: "Metadados / documentação",
    VIEWER_PORTAL: "Viewer / portal",
    SOFTWARE_DOCUMENTATION: "Software / documentação"
  };
  let roles = null;

  function apply() {
    if (!roles) return;
    const distributionCount = document.querySelector("#p-distributions");
    const expectedCount = String(Object.keys(roles.routes || {}).length);
    if (distributionCount && distributionCount.textContent !== expectedCount) {
      distributionCount.textContent = expectedCount;
    }

    document.querySelectorAll("article.distribution").forEach(card => {
      const heading = card.querySelector("h5");
      if (!heading) return;
      const headingText = heading.textContent.trim();
      const meta = roles.routes[headingText];
      if (!meta) return;

      if (card.dataset.routeRole !== meta.role) card.dataset.routeRole = meta.role;
      if (card.dataset.accessClass !== meta.access_class) card.dataset.accessClass = meta.access_class;

      let badge = card.querySelector(".distribution-semantic-role");
      if (!badge) {
        badge = document.createElement("p");
        badge.className = "distribution-semantic-role identity";
        heading.insertAdjacentElement("afterend", badge);
      }
      const badgeText = `${ROLE_LABELS[meta.role] || meta.role} · classe ${meta.access_class}`;
      if (badge.textContent !== badgeText) badge.textContent = badgeText;

      const link = card.querySelector("header a");
      if (link) {
        if (link.textContent !== meta.action) link.textContent = meta.action;
        const ariaLabel = `${meta.action}: ${headingText}`;
        if (link.getAttribute("aria-label") !== ariaLabel) link.setAttribute("aria-label", ariaLabel);
      }
    });
  }

  fetch("data/product_distribution_roles.json")
    .then(response => {
      if (!response.ok) throw new Error("route roles unavailable");
      return response.json();
    })
    .then(data => {
      roles = data;
      apply();
      const list = document.querySelector("#product-list");
      if (list) new MutationObserver(apply).observe(list, {childList:true});
    })
    .catch(() => {});
})();
