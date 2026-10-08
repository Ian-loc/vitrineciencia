(() => {
  "use strict";

  let registry = new Map();
  let accessRegistry = new Map();

  function decorate() {
    document.querySelectorAll("#list .card[data-resource-id]").forEach(card => {
      const item = registry.get(card.dataset.resourceId);
      if (!item) return;
      card.dataset.entityType = item.entity_type || "";
      card.dataset.accessRole = accessRegistry.get(card.dataset.resourceId) || "E";
      card.querySelector(".semantic-role-line")?.remove();
      card.querySelector(".semantic-scope-note")?.remove();
    });
  }

  async function init() {
    try {
      const [semanticResponse, accessResponse, postCoreResponse] = await Promise.all([
        fetch("data/static_core_51_progress.json", {cache:"no-store"}),
        fetch("data/static_core_51_access_audit.json", {cache:"no-store"}),
        fetch("data/post_core_access_audit.json", {cache:"no-store"})
      ]);
      if (!semanticResponse.ok) throw new Error(`semantic HTTP ${semanticResponse.status}`);
      if (!accessResponse.ok || !postCoreResponse.ok) throw new Error("Matrizes de acesso indisponíveis");
      const semanticPayload = await semanticResponse.json();
      const accessPayload = await accessResponse.json();
      const postCorePayload = await postCoreResponse.json();
      registry = new Map((semanticPayload.records || []).map(item => [item.resource_id, item]));
      accessRegistry = new Map([...accessPayload.records, ...postCorePayload.records].map(item => [item.resource_id, item.access_role]));
      const list = document.querySelector("#list");
      if (!list) return;
      decorate();
      new MutationObserver(decorate).observe(list, {childList:true, subtree:true});
    } catch (error) {
      console.error("Falha ao carregar a classificação verificada dos registros", error);
    }
  }

  document.addEventListener("DOMContentLoaded", init, {once:true});
})();
