(() => {
  "use strict";
  const set = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
  fetch("data/data_products.json")
    .then(response => {
      if (!response.ok) throw new Error("Falha ao carregar produtos");
      return response.json();
    })
    .then(products => {
      set("home-products", products.length);
      set("home-sources", new Set(products.map(product => product.resource_id)).size);
      set("home-access", products.reduce((total, product) => total + (product.distributions?.length || 0), 0));
      set("home-free", products.filter(product => product.distributions?.some(distribution => distribution.free_download === "sim")).length);
    })
    .catch(() => {});
})();
