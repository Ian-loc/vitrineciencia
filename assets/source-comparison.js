(() => {
  "use strict";

  const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
  const enumLabel = value => ({"sim":"Sim","parcial":"Parcial","não":"Não","desconhecido":"Desconhecido","não se aplica":"Não se aplica"}[value] || value || "Não informado");
  const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const csvCell = value => `"${String(value ?? "").replace(/"/g, '""')}"`;

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

  function waitForElement(selector, timeout = 8000) {
    const existing = document.querySelector(selector);
    if (existing) return Promise.resolve(existing);
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        observer.disconnect();
        reject(new Error(`Elemento não encontrado: ${selector}`));
      }, timeout);
      const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (!element) return;
        clearTimeout(timer);
        observer.disconnect();
        resolve(element);
      });
      observer.observe(document.documentElement, {childList: true, subtree: true});
    });
  }

  function comparisonValues(resource) {
    return {
      identity: resource.official_identity,
      areas: split(resource.research_areas).join(" | "),
      coverage: resource.geographic_coverage,
      brazil: enumLabel(resource.covers_brazil),
      spatial: resource.spatial_resolution,
      temporalCoverage: resource.temporal_coverage,
      temporal: resource.temporal_resolution,
      products: resource.data_product_types,
      formats: resource.data_formats,
      visualizations: resource.visualization_types,
      free: enumLabel(resource.free_download),
      programmatic: enumLabel(resource.programmatic_access),
      protocols: resource.access_protocols,
      authentication: enumLabel(resource.authentication_required),
      conditions: resource.access_conditions,
      license: resource.license,
      evidence: resource.academic_evidence_type,
      uses: resource.academic_uses,
      limitations: resource.limitations,
      owner: resource.owner_or_manager,
      verified: resource.last_verified
    };
  }

  const rows = [
    ["Identidade e escopo", null, "section"],
    ["Identidade oficial", "identity", "structured"],
    ["Áreas de pesquisa", "areas", "controlled"],
    ["Cobertura geográfica", "coverage", "structured"],
    ["Dados para o Brasil", "brazil", "controlled"],
    ["Resolução espacial", "spatial", "structured"],
    ["Cobertura temporal", "temporalCoverage", "structured"],
    ["Resolução temporal", "temporal", "structured"],
    ["Dados e acesso", null, "section"],
    ["Tipos de produto", "products", "structured"],
    ["Formatos", "formats", "controlled"],
    ["Visualizações", "visualizations", "structured"],
    ["Download gratuito", "free", "controlled"],
    ["API ou acesso automatizado", "programmatic", "controlled"],
    ["Protocolos e ferramentas", "protocols", "controlled"],
    ["Autenticação", "authentication", "controlled"],
    ["Condições de acesso", "conditions", "structured"],
    ["Licença", "license", "controlled"],
    ["Uso e evidência", null, "section"],
    ["Tipo de documentação", "evidence", "controlled"],
    ["Uso em pesquisa", "uses", "narrative"],
    ["Limitações", "limitations", "narrative"],
    ["Responsável", "owner", "structured"],
    ["Registro revisado em", "verified", "controlled"]
  ];

  async function init() {
    if (!document.querySelector("#list")) return;

    const response = await fetch("data/data_resources.json");
    if (!response.ok) throw new Error(`Falha ao carregar fontes: HTTP ${response.status}`);
    const resources = await response.json();
    const byId = new Map(resources.map(resource => [resource.resource_id, resource]));
    const selected = new Set();

    const bar = await waitForElement("#source-export-bar");
    const actions = bar.querySelector(".source-export-actions");
    const status = bar.querySelector("div:first-child span");
    bar.setAttribute("aria-label", "Fontes selecionadas para comparação e exportação");
    if (status) status.textContent = "Compare duas ou três fontes ou exporte os registros selecionados.";

    const compareButton = document.createElement("button");
    compareButton.type = "button";
    compareButton.id = "source-compare-open";
    compareButton.className = "source-compare-primary";
    compareButton.textContent = "Comparar fontes";
    compareButton.disabled = true;
    actions?.prepend(compareButton);

    const dialog = document.createElement("dialog");
    dialog.id = "source-compare-dialog";
    dialog.setAttribute("aria-labelledby", "source-compare-title");
    dialog.innerHTML = `<div class="source-compare-dialog-header"><div><p class="eyebrow">Comparação lado a lado</p><h2 id="source-compare-title">Fontes selecionadas</h2></div><div class="compare-dialog-actions"><button type="button" id="source-compare-download" class="download-comparison">Baixar tabela (CSV)</button><button type="button" id="source-compare-close">Fechar</button></div></div><div id="source-compare-content"></div>`;
    document.body.appendChild(dialog);

    const content = dialog.querySelector("#source-compare-content");
    const closeButton = dialog.querySelector("#source-compare-close");
    const downloadButton = dialog.querySelector("#source-compare-download");

    function syncLabels() {
      document.querySelectorAll("[data-source-export-controls] span").forEach(label => {
        label.textContent = "Selecionar para comparar ou exportar";
      });
    }

    function syncSelectedFromDom() {
      selected.clear();
      document.querySelectorAll("[data-select-source]:checked").forEach(input => {
        if (byId.has(input.dataset.selectSource)) selected.add(input.dataset.selectSource);
      });
      const count = selected.size;
      compareButton.disabled = count < 2 || count > 3;
      compareButton.title = count > 3 ? "A comparação aceita até três fontes; a exportação pode incluir mais." : "";
      if (status) {
        if (count === 0) status.textContent = "Compare duas ou três fontes ou exporte os registros selecionados.";
        else if (count === 1) status.textContent = "Selecione mais uma fonte para comparar.";
        else if (count <= 3) status.textContent = "Comparação pronta; a seleção também pode ser exportada.";
        else status.textContent = "Para comparar, mantenha duas ou três fontes selecionadas; a exportação aceita mais.";
      }
    }

    function renderComparison() {
      const chosen = [...selected].map(id => byId.get(id)).filter(Boolean);
      if (chosen.length < 2 || chosen.length > 3) return;
      const values = chosen.map(comparisonValues);
      const body = rows.map(([label, key, kind]) => {
        if (kind === "section") return `<tr class="comparison-section"><th scope="row">${esc(label)}</th>${chosen.map(() => "<td></td>").join("")}</tr>`;
        return `<tr><th scope="row">${esc(label)}</th>${values.map(value => `<td data-comparison-kind="${kind}">${esc(value[key] || "Não informado")}</td>`).join("")}</tr>`;
      }).join("");
      content.innerHTML = `<div class="compare-table-wrap"><table class="compare-table source-compare-table"><thead><tr><th scope="col">Dimensão</th>${chosen.map(resource => `<th scope="col">${esc(resource.resource_name)}</th>`).join("")}</tr></thead><tbody>${body}</tbody></table></div><p class="export-note">A comparação organiza metadados catalogados; confirme versão, metodologia e condições de uso na fonte original antes da análise.</p>`;
    }

    document.addEventListener("change", event => {
      if (!event.target.closest("[data-select-source]")) return;
      syncSelectedFromDom();
    });

    new MutationObserver(() => {
      syncLabels();
      syncSelectedFromDom();
    }).observe(document.querySelector("#list"), {childList: true, subtree: true});

    compareButton.addEventListener("click", () => {
      syncSelectedFromDom();
      renderComparison();
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    });

    closeButton.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", event => {
      if (event.target === dialog) dialog.close();
    });

    downloadButton.addEventListener("click", () => {
      const table = content.querySelector("table");
      if (!table) return;
      const csvRows = [...table.querySelectorAll("tr")].map(row => [...row.querySelectorAll("th,td")].map(cell => cell.textContent.trim()));
      downloadCsv(`vitrine-ciencia_comparacao_${selected.size}-fontes.csv`, csvRows);
    });

    syncLabels();
    syncSelectedFromDom();
  }

  const start = () => init().catch(error => console.warn("Vitrine Ciência: comparação de fontes indisponível.", error));
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once: true});
  else start();
})();
