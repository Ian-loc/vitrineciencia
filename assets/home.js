(() => {
  "use strict";
  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const set = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };

  fetch("data/data_products.json")
    .then(response => {
      if (!response.ok) throw new Error("Falha ao carregar produtos");
      return response.json();
    })
    .then(products => {
      const sourceCount = new Set(products.map(product => product.resource_id)).size;
      const accessCount = products.reduce((total, product) => total + (product.distributions?.length || 0), 0);
      const freeCount = products.filter(product => product.distributions?.some(distribution => distribution.free_download === "sim")).length;
      set("home-products", products.length);
      set("home-all-products", products.length);
      set("home-sources", sourceCount);
      set("home-access", accessCount);
      set("home-free", freeCount);

      document.querySelectorAll("[data-area]").forEach(card => {
        const area = norm(card.dataset.area);
        const count = products.filter(product => split(product.research_areas).some(value => norm(value) === area)).length;
        const target = card.querySelector("[data-area-count]");
        if (target) target.textContent = `${count} ${count === 1 ? "produto" : "produtos"}`;
      });
    })
    .catch(() => {});
})();