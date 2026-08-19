const $ = selector => document.querySelector(selector);
const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const countValues = values => values.filter(Boolean).reduce((counts, value) => {
  counts[value] = (counts[value] || 0) + 1;
  return counts;
}, {});
const sorted = counts => Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "pt-BR"));
const chartTargets = ["#chart-areas", "#chart-download", "#chart-programmatic", "#chart-brazil", "#chart-evidence", "#chart-formats", "#chart-visualizations"];
const pt = window.VitrinePTBR || {};
const identity = value => value;
const labelArea = pt.labelArea || identity;
const labelStatus = pt.labelStatus || identity;
const labelTerm = pt.labelTerm || identity;

function bars(target, entries, labeler = identity) {
  const element = $(target);
  const max = Math.max(1, ...entries.map(([, count]) => count));
  element.innerHTML = `<div class="bars" role="list">${entries.map(([rawLabel, count]) => {
    const label = labeler(rawLabel);
    return `<div class="bar-row" role="listitem"><div class="bar-label"><span>${esc(label)}</span><strong>${count}</strong></div><div class="bar-track" role="img" aria-label="${esc(label)}: ${count} fontes"><span aria-hidden="true" style="width:${(count / max) * 100}%"></span></div></div>`;
  }).join("")}</div>`;
  element.setAttribute("aria-busy", "false");
}

async function init() {
  try {
    const response = await fetch("data/data_resources.json");
    if (!response.ok) throw Error("Falha ao carregar os dados.");
    const all = await response.json();
    const peerReviewed = all.filter(resource => resource.academic_evidence_type === "artigo revisado por pares").length;

    const summary = $("#summary");
    summary.innerHTML = [
      ["Fontes catalogadas", all.length],
      ["Áreas de pesquisa", new Set(all.flatMap(resource => split(resource.research_areas))).size],
      ["Com download gratuito", all.filter(resource => resource.free_download === "sim").length],
      ["Com API ou acesso automatizado", all.filter(resource => resource.programmatic_access === "sim").length],
      ["Com dados para o Brasil", all.filter(resource => ["sim", "parcial"].includes(resource.covers_brazil)).length],
      ["Com artigo revisado por pares", peerReviewed]
    ].map(([label, value]) => `<div><strong>${value}</strong><span>${esc(label)}</span></div>`).join("");
    summary.setAttribute("aria-busy", "false");

    bars("#chart-areas", sorted(countValues(all.flatMap(resource => split(resource.research_areas)))), labelArea);
    bars("#chart-download", sorted(countValues(all.map(resource => resource.free_download))), labelStatus);
    bars("#chart-programmatic", sorted(countValues(all.map(resource => resource.programmatic_access))), labelStatus);
    bars("#chart-brazil", sorted(countValues(all.map(resource => resource.covers_brazil))), labelStatus);
    bars("#chart-evidence", sorted(countValues(all.map(resource => resource.academic_evidence_type))));

    const ignored = new Set(["formatos variados", "varia", "visualização web"]);
    const formats = all.flatMap(resource => split(resource.data_formats).map(value => value.split(";")[0].trim())).filter(value => value && !ignored.has(value.toLowerCase()));
    bars("#chart-formats", sorted(countValues(formats)).slice(0, 14));
    bars("#chart-visualizations", sorted(countValues(all.flatMap(resource => split(resource.visualization_types)))), labelTerm);
  } catch (error) {
    $("#summary").setAttribute("aria-busy", "false");
    chartTargets.forEach(target => $(target).setAttribute("aria-busy", "false"));
    $("#analise").insertAdjacentHTML("afterbegin", `<div class="empty" role="alert"><h2>Falha ao carregar a análise</h2><p>${esc(error.message)}</p></div>`);
  }
}

init();