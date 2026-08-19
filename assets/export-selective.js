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

  const ENUM_LABELS = {
    "sim": "Sim",
    "parcial": "Parcial",
    "não": "Não",
    "desconhecido": "Desconhecido",
    "não se aplica": "Não se aplica"
  };

  const KIND_LABELS = {
    dataset: "Conjunto de dados",
    dataset_series: "Série de conjuntos de dados",
    catalog: "Catálogo",
    federated_catalog: "Catálogo federado",
    data_service: "Serviço de dados",
    indicator_family: "Família de indicadores",
    map_layer_collection: "Coleção de camadas cartográficas",
    software_output: "Saída de software"
  };

  const ORIGIN_LABELS = {
    primário: "Primário",
    derivado: "Derivado",
    agregador: "Agregador",
    serviço: "Serviço",
    misto: "Misto",
    desconhecido: "Desconhecido"
  };

  const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
  const unique = values => [...new Set(values.filter(Boolean))];
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

  function withCount(text, mapper) {
    const match = String(text || "").match(/^(.*?)(\s+\(\d+\))$/);
    return match ? `${mapper(match[1])}${match[2]}` : mapper(text);
  }

  function localizeProductAreaControls() {
    const labelArea = window.VitrinePTBR?.labelArea;
    if (!labelArea) return;
    const select = document.querySelector("#product-area");
    if (select) {
      [...select.options].forEach(option => {
        if (!option.value) return;
        const translated = labelArea(option.value);
        option.textContent = withCount(option.textContent, () => translated);
        option.dataset.label = translated;
      });
    }
    document.querySelectorAll('#product-active-filters [data-remove="area"]').forEach(button => {
      const raw = button.textContent.replace(/\s*×\s*$/, "").replace(/^Área:\s*/, "").trim();
      const translated = `Área: ${labelArea(raw)}`;
      const textNode = [...button.childNodes].find(node => node.nodeType === Node.TEXT_NODE);
      if (textNode) textNode.textContent = `${translated} `;
      button.setAttribute("aria-label", `Remover ${translated}`);
    });
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

    const sourceRows = sourceIds => {
      const chosen = sourceIds.map(id => byId.get(id)).filter(Boolean);
      return [SOURCE_FIELDS, ...chosen.map(resource => SOURCE_FIELDS.map(field => resource[field] ?? ""))];
    };

    const decorateCards = () => {
      list.querySelectorAll(".card[data-resource-id]").forEach(card => {
        const id = card.dataset.resourceId;
        if (!id || !byId.has(id)) return;
        let controls = card.querySelector("[data-source-export-controls]");
        if (!controls) {
          const actions = card.querySelector(".card-actions");
          if (actions) {
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
          const cardActions = card.querySelector(".card-actions");
          if (cardActions) cardActions.insertAdjacentElement("afterend", controls);
          else card.appendChild(controls);
        }
        const checkbox = controls.querySelector("[data-select-source]");
        if (checkbox) checkbox.checked = selected.has(id);
      });
    };

    list.addEventListener("click", event => {
      const button = event.target.closest("[data-download-source]");
      if (!button) return;
      const id = button.dataset.downloadSource;
      const resource = byId.get(id);
      if (!resource) return;
      downloadCsv(`vitrine-ciencia_fonte_${slug(resource.resource_name)}_${id}.csv`, sourceRows([id]));
    });

    list.addEventListener("change", event => {
      const input = event.target.closest("[data-select-source]");
      if (!input) return;
      if (input.checked) selected.add(input.dataset.selectSource);
      else selected.delete(input.dataset.selectSource);
      renderBar();
    });

    document.querySelector("#source-export-download").addEventListener("click", () => {
      if (!selected.size) return;
      downloadCsv(`vitrine-ciencia_fontes-selecionadas_${selected.size}.csv`, sourceRows([...selected]));
    });

    document.querySelector("#source-export-clear").addEventListener("click", () => {
      selected.clear();
      list.querySelectorAll("[data-select-source]").forEach(input => { input.checked = false; });
      renderBar();
    });

    decorateCards();
    new MutationObserver(decorateCards).observe(list, {childList: true, subtree: true});
  }

  function productFormats(product) {
    return unique((product.distributions || []).flatMap(distribution => split(distribution.format)));
  }

  function productProtocols(product) {
    return unique((product.distributions || []).map(distribution => distribution.access_protocol));
  }

  function aggregateEnum(values) {
    const clean = values.filter(Boolean);
    if (clean.includes("sim")) return "sim";
    if (clean.includes("parcial")) return "parcial";
    if (clean.length && clean.every(value => value === "não")) return "não";
    if (clean.includes("desconhecido")) return "desconhecido";
    return clean[0] || "desconhecido";
  }

  function comparisonRows(product) {
    const free = aggregateEnum((product.distributions || []).map(item => item.free_download));
    const auth = aggregateEnum((product.distributions || []).map(item => item.authentication_required));
    return {
      source: product.source?.resource_name,
      family: product.product_family,
      kind: KIND_LABELS[product.product_kind] || product.product_kind,
      brazil: ENUM_LABELS[product.covers_brazil] || product.covers_brazil,
      origin: ORIGIN_LABELS[product.primary_or_derived] || product.primary_or_derived,
      status: product.product_status,
      coverage: product.geographic_coverage,
      spatial_support: product.spatial_support,
      spatial_resolution: product.spatial_resolution,
      temporal_coverage: product.temporal_coverage,
      temporal_resolution: product.temporal_resolution,
      update_frequency: product.update_frequency,
      version: product.version_or_collection,
      formats: productFormats(product).join(" | "),
      protocols: productProtocols(product).join(" | "),
      free: ENUM_LABELS[free] || free,
      auth: ENUM_LABELS[auth] || auth,
      limitations: product.limitations,
      description: product.product_description,
      verified: product.last_verified
    };
  }

  async function initProductComparisonExport() {
    const compareButton = document.querySelector("#compare-open");
    const compareContent = document.querySelector("#compare-content");
    const dialogHeader = document.querySelector(".compare-dialog-header");
    if (!compareButton || !compareContent || !dialogHeader) return;

    const response = await fetch("data/data_products.json");
    if (!response.ok) return;
    const products = await response.json();
    const byId = new Map(products.map(product => [product.product_id, product]));
    const selected = new Set();

    const closeButton = document.querySelector("#compare-close");
    const actions = document.createElement("div");
    actions.className = "compare-dialog-actions";
    const downloadButton = document.createElement("button");
    downloadButton.type = "button";
    downloadButton.id = "compare-download-csv";
    downloadButton.className = "download-comparison";
    downloadButton.textContent = "Baixar tabela (CSV)";
    actions.appendChild(downloadButton);
    if (closeButton) actions.appendChild(closeButton);
    dialogHeader.appendChild(actions);

    document.addEventListener("change", event => {
      const input = event.target.closest("[data-compare]");
      if (!input) return;
      const id = input.dataset.compare;
      if (input.checked) selected.add(id);
      else selected.delete(id);
    });

    const rows = [
      ["Fonte", "source", "controlled"],
      ["Família do produto", "family", "controlled"],
      ["Tipo de produto", "kind", "controlled"],
      ["Dados para o Brasil", "brazil", "controlled"],
      ["Origem", "origin", "controlled"],
      ["Estado do produto", "status", "controlled"],
      ["Cobertura geográfica", "coverage", "structured"],
      ["Suporte espacial", "spatial_support", "structured"],
      ["Resolução espacial", "spatial_resolution", "structured"],
      ["Cobertura temporal", "temporal_coverage", "structured"],
      ["Resolução temporal", "temporal_resolution", "structured"],
      ["Frequência de atualização", "update_frequency", "structured"],
      ["Versão ou coleção", "version", "structured"],
      ["Formatos", "formats", "controlled"],
      ["Protocolos", "protocols", "controlled"],
      ["Download gratuito", "free", "controlled"],
      ["Autenticação", "auth", "controlled"],
      ["Limitações", "limitations", "narrative"],
      ["Descrição", "description", "narrative"],
      ["Registro revisado em", "verified", "controlled"]
    ];

    function renderComparison() {
      const chosen = [...selected].map(id => byId.get(id)).filter(Boolean);
      if (chosen.length < 2) return;
      const values = chosen.map(comparisonRows);
      compareContent.innerHTML = `<div class="compare-table-wrap"><table class="compare-table"><thead><tr><th scope="col">Dimensão</th>${chosen.map(product => `<th scope="col">${esc(product.product_name)}</th>`).join("")}</tr></thead><tbody>${rows.map(([label, key, kind]) => `<tr><th scope="row">${esc(label)}</th>${values.map(value => `<td data-comparison-kind="${kind}">${esc(value[key] || "Não informado")}</td>`).join("")}</tr>`).join("")}</tbody></table></div><p class="export-note">Os campos comparáveis foram separados por dimensão. Descrição e limitações permanecem narrativas e aparecem ao final da tabela.</p>`;
      localizeProductAreaControls();
    }

    compareButton.addEventListener("click", () => setTimeout(renderComparison, 0));

    downloadButton.addEventListener("click", () => {
      const table = compareContent.querySelector("table.compare-table");
      if (!table) return;
      const csvRows = [...table.querySelectorAll("tr")].map(row => [...row.querySelectorAll("th,td")].map(cell => cell.textContent.trim()));
      downloadCsv(`vitrine-ciencia_comparacao_${Math.max(2, selected.size)}-produtos.csv`, csvRows);
    });

    localizeProductAreaControls();
    const productsRoot = document.querySelector("#product-catalog");
    if (productsRoot) new MutationObserver(localizeProductAreaControls).observe(productsRoot, {childList: true, subtree: true});
  }

  async function start() {
    try {
      await Promise.all([initSourceExports(), initProductComparisonExport()]);
    } catch (error) {
      console.warn("Vitrine Ciência: exportação seletiva indisponível nesta página.", error);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once: true});
  else start();
})();
