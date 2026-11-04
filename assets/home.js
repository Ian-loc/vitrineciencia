(() => {
  "use strict";
  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const set = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
  const escapeHtml = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
  const https = value => /^https:\/\//i.test(String(value || ""));

  const publicAccess = item => window.VitrinePublicAccess(item);

  const renderPriorityGate = payload => {
    const items = Array.isArray(payload?.items) ? payload.items : [];
    if (!items.length || document.getElementById("applied-priority-gate")) return;
    const anchor = document.querySelector(".core-note");
    if (!anchor) return;

    const section = document.createElement("section");
    section.className = "home-section thematic-products";
    section.id = "applied-priority-gate";
    section.setAttribute("aria-labelledby", "applied-priority-heading");
    section.innerHTML = `
      <div class="section-heading">
        <div><p class="eyebrow">Acesso rápido</p><h2 id="applied-priority-heading">Exemplos para chegar aos dados</h2></div>
        <p>Alguns caminhos úteis para perguntas recorrentes.</p>
      </div>
      <div class="product-area-grid process-grid" data-priority-grid></div>`;

    const grid = section.querySelector("[data-priority-grid]");
    items.forEach(item => {
      const card = document.createElement("article");
      card.className = "product-area-card process-card priority-gate-card";
      const access = publicAccess(item);
      card.innerHTML = `
        <strong>${escapeHtml(item.platform)}</strong>
        <span class="area-examples"><b>Fenômeno/processo:</b> ${escapeHtml(item.theme)}</span>
        <span class="area-examples"><b>Dado:</b> ${escapeHtml(item.data_object)}</span>
        <span class="area-examples"><b>Território:</b> ${escapeHtml(item.territory)}</span>
        <span class="area-examples"><b>Responsável:</b> ${escapeHtml(item.provenance)}</span>
        ${access ? `<span><a href="${escapeHtml(access.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(access.label)}</a></span>` : ""}`;
      grid.appendChild(card);
    });
    anchor.insertAdjacentElement("beforebegin", section);
  };

  Promise.all([
    fetch("data/data_products.json").then(response => response.ok ? response.json() : Promise.reject()),
    fetch("data/data_resources.json").then(response => response.ok ? response.json() : Promise.reject()),
    fetch("data/applied_priority_gate.json", {cache: "no-store"}).then(response => response.ok ? response.json() : Promise.reject()),
    fetch("data/access_routes.json", {cache: "no-store"}).then(response => response.ok ? response.json() : Promise.reject())
  ])
    .then(([products, resources, priorityGate, accessAudit]) => {
      const confirmedDataAccess = new Set((accessAudit.routes || []).filter(item => item.target_type === "resource" && item.primary && ["A", "B"].includes(item.access_assessment) && resources.some(resource => resource.resource_id === item.record_id)).map(item => item.record_id)).size;
      const freeCount = products.filter(product => product.distributions?.some(distribution => distribution.free_download === "sim")).length;
      set("home-products", products.length);
      set("home-all-products", products.length);
      set("home-sources", resources.length);
      set("home-all-sources", resources.length);
      set("home-access", confirmedDataAccess);
      set("home-free", freeCount);
      renderPriorityGate(priorityGate);

      document.querySelectorAll("[data-area]").forEach(card => {
        const area = norm(card.dataset.area);
        const count = products.filter(product => split(product.research_areas).some(value => norm(value) === area)).length;
        const target = card.querySelector("[data-area-count]");
        if (target) target.textContent = `${count} ${count === 1 ? "produto" : "produtos"}`;
      });
    })
    .catch(error => console.error("Falha ao inicializar a página inicial", error));
})();