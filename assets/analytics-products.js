const $ = selector => document.querySelector(selector);
const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const countValues = values => values.filter(Boolean).reduce((counts, value) => {
  counts[value] = (counts[value] || 0) + 1;
  return counts;
}, {});
const sorted = counts => Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "pt-BR"));
const pt = window.VitrinePTBR || {};
const identity = value => value;
const labelArea = pt.labelArea || identity;
const labelStatus = pt.labelStatus || identity;
const localKindLabels = {
  dataset:"Conjunto de dados",
  dataset_series:"Série de conjuntos de dados",
  data_service:"Serviço de dados",
  catalog:"Catálogo",
  federated_catalog:"Catálogo federado",
  indicator_family:"Família de indicadores",
  map_layer_collection:"Coleção de camadas cartográficas",
  software_output:"Saída de software"
};
const labelKind = value => localKindLabels[value] || (pt.labelKind ? pt.labelKind(value) : value);
const chartTargets = ["#product-chart-areas", "#product-chart-kinds", "#product-chart-brazil", "#product-chart-temporal", "#product-chart-support", "#product-chart-formats", "#product-chart-access"];

function bars(target, entries, labeler = identity) {
  const element = $(target);
  const max = Math.max(1, ...entries.map(([, count]) => count));
  element.innerHTML = `<div class="bars" role="list">${entries.map(([rawLabel, count]) => {
    const label = labeler(rawLabel);
    return `<div class="bar-row" role="listitem"><div class="bar-label"><span>${esc(label)}</span><strong>${count}</strong></div><div class="bar-track" role="img" aria-label="${esc(label)}: ${count} produtos"><span aria-hidden="true" style="width:${(count / max) * 100}%"></span></div></div>`;
  }).join("")}</div>`;
  element.setAttribute("aria-busy", "false");
}

function distributions(product) {
  return Array.isArray(product.distributions) ? product.distributions : [];
}

async function init() {
  try {
    const response = await fetch("data/data_products.json");
    if (!response.ok) throw Error("Falha ao carregar os produtos.");
    const all = await response.json();
    const sources = new Set(all.map(product => product.source?.resource_name).filter(Boolean));
    const areas = new Set(all.flatMap(product => split(product.research_areas)));
    const formats = all.flatMap(product => distributions(product).flatMap(item => split(item.format)));
    const access = all.flatMap(product => distributions(product).map(item => item.access_protocol || item.access_tool).filter(Boolean));
    const withTemporal = all.filter(product => String(product.temporal_coverage || "").trim()).length;
    const withSpatial = all.filter(product => String(product.spatial_resolution || "").trim()).length;

    const summary = $("#product-summary");
    summary.innerHTML = [
      ["Produtos catalogados", all.length],
      ["Fontes representadas", sources.size],
      ["Áreas de pesquisa", areas.size],
      ["Com dados para o Brasil", all.filter(product => ["sim", "parcial"].includes(product.covers_brazil)).length],
      ["Com período informado", withTemporal],
      ["Com resolução espacial", withSpatial]
    ].map(([label, value]) => `<div><strong>${value}</strong><span>${esc(label)}</span></div>`).join("");
    summary.setAttribute("aria-busy", "false");

    bars("#product-chart-areas", sorted(countValues(all.flatMap(product => split(product.research_areas)))).slice(0, 18), labelArea);
    bars("#product-chart-kinds", sorted(countValues(all.map(product => product.product_kind))), labelKind);
    bars("#product-chart-brazil", sorted(countValues(all.map(product => product.covers_brazil))), labelStatus);
    bars("#product-chart-temporal", sorted(countValues(all.map(product => product.temporal_resolution))).slice(0, 12));
    bars("#product-chart-support", sorted(countValues(all.map(product => product.spatial_support))).slice(0, 12));
    bars("#product-chart-formats", sorted(countValues(formats)).slice(0, 14));
    bars("#product-chart-access", sorted(countValues(access)).slice(0, 14));
  } catch (error) {
    $("#product-summary").setAttribute("aria-busy", "false");
    chartTargets.forEach(target => $(target).setAttribute("aria-busy", "false"));
    $("#analise-produtos").insertAdjacentHTML("afterbegin", `<div class="empty" role="alert"><h2>Falha ao carregar o panorama</h2><p>${esc(error.message)}</p></div>`);
  }
}

init();
