(() => {
  "use strict";

  const ACCESS = {
    A: {label: "Dados / download", tone: "confirmed"},
    B: {label: "Página para obter dados", tone: "confirmed"},
    C: {label: "API / serviço de dados", tone: "confirmed"},
    D: {label: "Visualização / documentação", tone: "review"},
    E: {label: "Acesso em revisão", tone: "review"}
  };

  const norm = value => String(value || "")
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase().trim();

  function addText(parent, tag, text, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = text;
    parent.appendChild(node);
    return node;
  }

  function card(item) {
    const article = document.createElement("article");
    article.className = "priority-data-card";
    article.dataset.gate = item.gate;

    const meta = document.createElement("div");
    meta.className = "priority-card-meta";
    addText(meta, "span", item.gate, "priority-gate");
    addText(meta, "span", item.theme, "priority-theme");
    article.appendChild(meta);

    addText(article, "h3", item.data_object);
    addText(article, "p", item.platform, "priority-platform");

    const facts = document.createElement("dl");
    facts.className = "priority-facts";
    [
      ["Território", item.territory],
      ["Proveniência", item.provenance],
      ["Distribuição", item.distribution]
    ].forEach(([label, value]) => {
      const row = document.createElement("div");
      addText(row, "dt", label);
      addText(row, "dd", value);
      facts.appendChild(row);
    });
    article.appendChild(facts);

    const access = ACCESS[item.access_role] || ACCESS.E;
    const note = document.createElement("p");
    note.className = `priority-access ${access.tone}`;
    addText(note, "strong", `${item.access_role} · ${access.label}: `);
    note.appendChild(document.createTextNode(item.verification_note));
    article.appendChild(note);

    const actions = document.createElement("div");
    actions.className = "card-actions priority-actions";
    const accessLink = document.createElement("a");
    accessLink.href = item.access_url;
    accessLink.target = "_blank";
    accessLink.rel = "noopener noreferrer";
    accessLink.className = item.access_role === "B" || item.access_role === "A" || item.access_role === "C"
      ? "action-primary"
      : "action-secondary";
    accessLink.textContent = item.access_role === "E" ? "Ver referência atual" : access.label;
    actions.appendChild(accessLink);

    if (item.documentation_url && item.documentation_url !== item.access_url) {
      const docs = document.createElement("a");
      docs.href = item.documentation_url;
      docs.target = "_blank";
      docs.rel = "noopener noreferrer";
      docs.className = "action-secondary";
      docs.textContent = "Documentação / evidência";
      actions.appendChild(docs);
    }
    article.appendChild(actions);
    return article;
  }

  async function init() {
    const list = document.querySelector("#priority-applied-list");
    const status = document.querySelector("#priority-applied-status");
    if (!list) return;
    try {
      const response = await fetch("data/applied_priority_gate.json", {cache: "no-store"});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      const items = Array.isArray(payload.items) ? payload.items : [];
      const q = document.querySelector("#q");

      const render = () => {
        const query = norm(q?.value);
        const visible = query
          ? items.filter(item => norm(`${item.theme} ${item.data_object} ${item.platform} ${item.territory}`).includes(query))
          : items;
        list.replaceChildren(...visible.map(card));
        list.hidden = visible.length === 0;
        if (status) {
          status.textContent = query
            ? `${visible.length} dado(s) prioritário(s) relacionado(s) ao tema selecionado.`
            : `${items.length} objetos aplicados cobrem os gates P1–P6 sem alterar o núcleo histórico de 51 registros.`;
        }
      };

      q?.addEventListener("input", render);
      render();
    } catch (error) {
      list.hidden = true;
      if (status) status.textContent = "Camada aplicada temporariamente indisponível; o núcleo de 51 registros permanece acessível abaixo.";
      console.error("Falha ao carregar gate aplicado P1–P6", error);
    }
  }

  document.addEventListener("DOMContentLoaded", init, {once: true});
})();