(() => {
  "use strict";
  const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const set = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
  const escapeHtml = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));

  const accessLabel = item => {
    if (item.access_role === "A") return "Baixar dados";
    if (item.access_role === "B") return "Página do conjunto / obter dados";
    if (item.access_role === "C") return "Consultar API-serviço";
    if (item.access_role === "E") return "Página do provedor · acesso em revisão";
    return /visualiza|painel/i.test(item.distribution || "") ? "Explorar viewer" : "Ver documentação";
  };

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
        <div><p class="eyebrow">Rotas prioritárias verificadas</p><h2 id="applied-priority-heading">Exemplos aplicados: da pergunta à rota correta</h2></div>
        <p>Esta camada reutiliza diretamente a autoridade P1–P6; não cria novos registros no núcleo de 51.</p>
      </div>
      <div class="product-area-grid process-grid" data-priority-grid></div>
      <p class="search-help">A, B e C indicam acesso confirmado; D é visualização/documentação; E permanece explicitamente em revisão.</p>`;

    const grid = section.querySelector("[data-priority-grid]");
    items.forEach(item => {
      const card = document.createElement("article");
      card.className = "product-area-card process-card priority-gate-card";
      const role = escapeHtml(item.access_role || "E");
      const coreRef = item.core_resource_id ? ` · ${escapeHtml(item.core_resource_id)}` : "";
      const secondaryDocumentation = item.documentation_url && item.documentation_url !== item.access_url
        ? `<a href="${escapeHtml(item.documentation_url)}" target="_blank" rel="noopener noreferrer">Ver documentação</a>`
        : "";
      card.innerHTML = `
        <strong>${escapeHtml(item.gate)} · ${escapeHtml(item.platform)}</strong>
        <span class="area-examples"><b>Fenômeno/processo:</b> ${escapeHtml(item.theme)}</span>
        <span class="area-examples"><b>Dataset/família ou objeto informacional:</b> ${escapeHtml(item.data_object)}</span>
        <span class="area-examples"><b>Território/escala essencial:</b> ${escapeHtml(item.territory)}</span>
        <span class="area-examples"><b>Proveniência:</b> ${escapeHtml(item.provenance)}</span>
        <span class="area-examples"><b>Rota:</b> ${escapeHtml(item.distribution)}</span>
        <span class="area-examples"><b>Acesso ${role}${coreRef}:</b> ${role === "A" || role === "B" || role === "C" ? "confirmado" : role === "D" ? "visualização/documentação" : "em revisão"}</span>
        <span><a href="${escapeHtml(item.access_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(accessLabel(item))}</a>${secondaryDocumentation ? ` · ${secondaryDocumentation}` : ""}</span>`;
      grid.appendChild(card);
    });
    anchor.insertAdjacentElement("beforebegin", section);
  };

  Promise.all([
    fetch("data/data_products.json").then(response => {
      if (!response.ok) throw new Error("Falha ao carregar produtos");
      return response.json();
    }),
    fetch("data/data_resources.json").then(response => {
      if (!response.ok) throw new Error("Falha ao carregar fontes");
      return response.json();
    }),
    fetch("data/applied_priority_gate.json", {cache: "no-store"}).then(response => {
      if (!response.ok) throw new Error("Falha ao carregar gate P1-P6");
      return response.json();
    })
  ])
    .then(([products, resources, priorityGate]) => {
      const accessCount = products.reduce((total, product) => total + (product.distributions?.length || 0), 0);
      const freeCount = products.filter(product => product.distributions?.some(distribution => distribution.free_download === "sim")).length;
      set("home-products", products.length);
      set("home-all-products", products.length);
      set("home-sources", resources.length);
      set("home-access", accessCount);
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