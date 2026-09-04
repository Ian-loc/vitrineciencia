(() => {
  "use strict";

  const norm = value => String(value || "")
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase().trim();
  const https = value => /^https:\/\//i.test(String(value || ""));

  function addText(parent, tag, text, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = text;
    parent.appendChild(node);
    return node;
  }

  function publicAccess(item) {
    if (["A", "B"].includes(item.access_role) && https(item.access_url)) return {label: "Acessar dados / download", url: item.access_url, primary: true};
    if (item.access_role === "C") {
      const site = https(item.documentation_url) ? item.documentation_url : "";
      return site ? {label: "Acessar site", url: site, primary: false} : null;
    }
    const site = https(item.access_url) ? item.access_url : (https(item.documentation_url) ? item.documentation_url : "");
    return site ? {label: "Acessar site", url: site, primary: false} : null;
  }

  function card(item) {
    const article = document.createElement("article");
    article.className = "priority-data-card";

    const meta = document.createElement("div");
    meta.className = "priority-card-meta";
    addText(meta, "span", item.theme, "priority-theme");
    article.appendChild(meta);

    addText(article, "h3", item.data_object);
    addText(article, "p", item.platform, "priority-platform");

    const facts = document.createElement("dl");
    facts.className = "priority-facts";
    [["Território", item.territory], ["Proveniência", item.provenance]].forEach(([label, value]) => {
      const row = document.createElement("div");
      addText(row, "dt", label);
      addText(row, "dd", value);
      facts.appendChild(row);
    });
    article.appendChild(facts);

    const access = publicAccess(item);
    if (access) {
      const actions = document.createElement("div");
      actions.className = "card-actions priority-actions";
      const accessLink = document.createElement("a");
      accessLink.href = access.url;
      accessLink.target = "_blank";
      accessLink.rel = "noopener noreferrer";
      accessLink.className = access.primary ? "action-primary" : "action-secondary";
      accessLink.textContent = access.label;
      actions.appendChild(accessLink);
      article.appendChild(actions);
    }
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
        if (status) status.textContent = query ? `${visible.length} exemplo(s) relacionado(s) ao tema selecionado.` : `${items.length} exemplos disponíveis.`;
      };

      q?.addEventListener("input", render);
      render();
    } catch (error) {
      list.hidden = true;
      if (status) status.textContent = "Exemplos temporariamente indisponíveis.";
      console.error("Falha ao carregar exemplos prioritários", error);
    }
  }

  document.addEventListener("DOMContentLoaded", init, {once: true});
})();