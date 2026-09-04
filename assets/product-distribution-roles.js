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
    if (distributionCount) distributionCount.textContent = Object.keys(roles.routes || {}).length;
    document.querySelectorAll("article.distribution").forEach(card => {
      const heading = card.querySelector("h5");
      if (!heading) return;
      const meta = roles.routes[heading.textContent.trim()];
      if (!meta) return;
      card.dataset.routeRole = meta.role;
      card.dataset.accessClass = meta.access_class;
      let badge = card.querySelector(".distribution-semantic-role");
      if (!badge) {
        badge = document.createElement("p");
        badge.className = "distribution-semantic-role identity";
        heading.insertAdjacentElement("afterend", badge);
      }
      badge.textContent = `${ROLE_LABELS[meta.role] || meta.role} · classe ${meta.access_class}`;
      const link = card.querySelector("header a");
      if (link) {
        link.textContent = meta.action;
        link.setAttribute("aria-label", `${meta.action}: ${heading.textContent.trim()}`);
      }
    });
  }

  fetch("data/product_distribution_roles.json")
    .then(response => { if (!response.ok) throw new Error("route roles unavailable"); return response.json(); })
    .then(data => { roles = data; apply(); new MutationObserver(apply).observe(document.querySelector("#product-list"), {childList:true, subtree:true}); })
    .catch(() => {});
})();
