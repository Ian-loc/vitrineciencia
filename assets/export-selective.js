(() => {
  "use strict";

  const SOURCE_FIELDS = [
    "resource_id","resource_name","acronym","official_identity","description","homepage_url","data_access_url",
    "research_areas","keywords","data_product_types","data_formats","visualization_types","geographic_coverage",
    "covers_brazil","spatial_resolution","temporal_coverage","temporal_resolution","data_sources","free_download",
    "access_conditions","programmatic_access","access_protocols","authentication_required","access_documentation_url",
    "license","institutional_status","owner_or_manager","academic_uses","limitations","academic_evidence_type",
    "academic_evidence_url","academic_evidence_note","verification_url","last_verified"
  ];

  const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
  const csvCell = value => `"${String(value ?? "").replace(/"/g, '""')}"`;
  const slug = value => String(value || "vitrine-ciencia").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 80);

  function downloadCsv(filename, rows) {
    const content = "\uFEFF" + rows.map(row => row.map(csvCell).join(",")).join("\r\n");
    const blob = new Blob([content], {type: "text/csv;charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function initSourceExports() {
    const list = document.querySelector("#list");
    if (!list) return;
    const response = await fetch("data/data_resources.json");
    if (!response.ok) return;
    const resources = await response.json();
    const byId = new Map(resources.map(resource => [resource.resource_id, resource]));
    const selected = new Set();

    const bar = document.createElement("div");
    bar.id = "source-export-bar";
    bar.className = "source-export-bar";
    bar.hidden = true;
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Fontes selecionadas para exportação");
    bar.innerHTML = `<div><strong id="source-export-count">0 fontes selecionadas</strong><span>Exporte somente os registros escolhidos da Vitrine.</span></div><div class="source-export-actions"><button type="button" id="source-export-download">Baixar seleção (CSV)</button><button type="button" id="source-export-clear">Limpar</button></div>`;
    document.body.appendChild(bar);

    const renderBar = () => {
      const count = selected.size;
      bar.hidden = count === 0;
      document.querySelector("#source-export-count").textContent = `${count} ${count === 1 ? "fonte selecionada" : "fontes selecionadas"}`;
    };
    const rowsFor = ids => [SOURCE_FIELDS, ...ids.map(id => byId.get(id)).filter(Boolean).map(resource => SOURCE_FIELDS.map(field => resource[field] ?? ""))];
    const decorateCards = () => {
      list.querySelectorAll(".card[data-resource-id]").forEach(card => {
        const id = card.dataset.resourceId;
        if (!id || !byId.has(id)) return;
        let controls = card.querySelector("[data-source-export-controls]");
        if (!controls) {
          const actions = card.querySelector(".card-actions");
          if (actions && !actions.querySelector("[data-download-source]")) {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "action-secondary";
            button.dataset.downloadSource = id;
            button.textContent = "Baixar registro (CSV)";
            actions.appendChild(button);
          }
          controls = document.createElement("label");
          controls.className = "select-export-toggle";
          controls.dataset.sourceExportControls = "";
          controls.innerHTML = `<input type="checkbox" data-select-source="${esc(id)}"><span>Selecionar para exportar</span>`;
          if (actions) actions.insertAdjacentElement("afterend", controls); else card.appendChild(controls);
        }
        const checkbox = controls.querySelector("[data-select-source]");
        if (checkbox) checkbox.checked = selected.has(id);
      });
    };

    list.addEventListener("click", event => {
      const button = event.target.closest("[data-download-source]");
      if (!button) return;
      const resource = byId.get(button.dataset.downloadSource);
      if (resource) downloadCsv(`vitrine-ciencia_fonte_${slug(resource.resource_name)}_${resource.resource_id}.csv`, rowsFor([resource.resource_id]));
    });
    list.addEventListener("change", event => {
      const input = event.target.closest("[data-select-source]");
      if (!input) return;
      if (input.checked) selected.add(input.dataset.selectSource); else selected.delete(input.dataset.selectSource);
      renderBar();
    });
    document.querySelector("#source-export-download").addEventListener("click", () => {
      if (selected.size) downloadCsv(`vitrine-ciencia_fontes-selecionadas_${selected.size}.csv`, rowsFor([...selected]));
    });
    document.querySelector("#source-export-clear").addEventListener("click", () => {
      selected.clear(); list.querySelectorAll("[data-select-source]").forEach(input => { input.checked = false; }); renderBar();
    });
    decorateCards();
    new MutationObserver(decorateCards).observe(list, {childList:true,subtree:true});
  }

  function initProductComparisonExport() {
    const dialogHeader = document.querySelector(".compare-dialog-header");
    const compareContent = document.querySelector("#compare-content");
    const closeButton = document.querySelector("#compare-close");
    if (!dialogHeader || !compareContent || !closeButton) return;

    const actions = document.createElement("div");
    actions.className = "compare-dialog-actions";
    const downloadButton = document.createElement("button");
    downloadButton.type = "button";
    downloadButton.id = "compare-download-csv";
    downloadButton.className = "download-comparison";
    downloadButton.textContent = "Baixar tabela (CSV)";
    actions.append(downloadButton, closeButton);
    dialogHeader.appendChild(actions);

    downloadButton.addEventListener("click", () => {
      const table = compareContent.querySelector("table.compare-table");
      if (!table) return;
      const csvRows = [...table.querySelectorAll("tr")].map(row => [...row.querySelectorAll("th,td")].map(cell => {
        const clone = cell.cloneNode(true);
        clone.querySelectorAll("button").forEach(button => button.remove());
        return clone.textContent.trim();
      }));
      const productCount = Math.max(0, (table.querySelectorAll("thead th").length || 1) - 1);
      downloadCsv(`vitrine-ciencia_comparacao_${productCount}-produtos.csv`, csvRows);
    });
  }

  async function start() {
    try { await initSourceExports(); } catch (error) { console.warn("Vitrine Ciência: exportação de fontes indisponível.", error); }
    try { initProductComparisonExport(); } catch (error) { console.warn("Vitrine Ciência: exportação da comparação indisponível.", error); }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once:true}); else start();
})();