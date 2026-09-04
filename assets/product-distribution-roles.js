(() => {
  "use strict";
  let roles = null;

  function apply() {
    if (!roles) return;
    const distributionCount = document.querySelector("#p-distributions");
    const expectedCount = String(Object.keys(roles.routes || {}).length);
    if (distributionCount && distributionCount.textContent !== expectedCount) distributionCount.textContent = expectedCount;

    document.querySelectorAll("article.distribution").forEach(card => {
      const heading = card.querySelector("h5");
      if (!heading) return;
      const meta = roles.routes[heading.textContent.trim()];
      if (!meta) return;
      card.dataset.routeRole = meta.role;
      card.dataset.accessClass = meta.access_class;
      card.querySelector(".distribution-semantic-role")?.remove();
    });
  }

  fetch("data/product_distribution_roles.json", {cache: "no-store"})
    .then(response => {
      if (!response.ok) throw new Error("route roles unavailable");
      return response.json();
    })
    .then(data => {
      roles = data;
      apply();
      const list = document.querySelector("#product-list");
      if (list) new MutationObserver(apply).observe(list, {childList:true, subtree:true});
    })
    .catch(() => {});
})();
