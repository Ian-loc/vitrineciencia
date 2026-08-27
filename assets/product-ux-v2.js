/* Product-first discovery layer for Vitrine Ciência, 2026-08-27.
   Extends the stable product model without changing Fonte → Produto → Distribuição. */

const UX_STOPWORDS = new Set(["a","as","o","os","de","da","das","do","dos","e","em","no","na","nos","nas","para","por","com","dados","dado","dataset","datasets","sobre","the","of","and","for","in","data"]);
const UX_CONCEPTS = [
  {key:"carbon", label:"carbono", aliases:["carbono","carbon","soc","carbon stock","estoque de carbono","organic carbon","carbono orgânico"]},
  {key:"soil", label:"solo", aliases:["solo","soil","edáfico","edafico"]},
  {key:"biomass", label:"biomassa", aliases:["biomassa","biomass","agb","aboveground biomass"]},
  {key:"biodiversity", label:"biodiversidade", aliases:["biodiversidade","biodiversity","species","espécies","especies"]},
  {key:"precipitation", label:"precipitação", aliases:["precipitação","precipitacao","precipitation","rainfall","chuva"]},
  {key:"landuse", label:"uso/cobertura da terra", aliases:["uso da terra","cobertura da terra","land use","land cover","lulc"]},
  {key:"fire", label:"fogo", aliases:["fogo","fire","burned area","área queimada","area queimada","hotspot","foco de calor"]},
  {key:"cerrado", label:"Cerrado", aliases:["cerrado"]},
  {key:"amazon", label:"Amazônia", aliases:["amazônia","amazonia","amazon","amazonas"]},
  {key:"atlantic", label:"Mata Atlântica", aliases:["mata atlântica","mata atlantica","atlantic forest"]},
  {key:"caatinga", label:"Caatinga", aliases:["caatinga"]},
  {key:"pantanal", label:"Pantanal", aliases:["pantanal"]},
  {key:"pampa", label:"Pampa", aliases:["pampa"]},
  {key:"brazil", label:"Brasil", aliases:["brasil","brazil"]},
  {key:"annual", label:"anual", aliases:["anual","annual","yearly"]},
  {key:"monthly", label:"mensal", aliases:["mensal","monthly"]},
  {key:"daily", label:"diário", aliases:["diário","diario","daily"]}
];
const UX_TOKEN_TO_CONCEPT = new Map();
UX_CONCEPTS.forEach(concept => concept.aliases.forEach(alias => {
  const normalized = norm(alias);
  if (!normalized.includes(" ")) UX_TOKEN_TO_CONCEPT.set(normalized, concept);
}));

const UX_SOURCE_PRIORITY = new Map();

els.coverage = document.querySelector("#product-coverage");
els.yearStart = document.querySelector("#product-year-start");
els.yearEnd = document.querySelector("#product-year-end");
els.temporal = document.querySelector("#product-temporal");
els.spatialSupport = document.querySelector("#product-spatial-support");
els.spatialResolution = document.querySelector("#product-spatial-resolution");
els.access = document.querySelector("#product-access");
els.free = document.querySelector("#product-free");
els.license = document.querySelector("#product-license");
els.queryInterpretation = document.querySelector("#query-interpretation");

function uxText(value) {
  return norm(value || "");
}

function uxYears(value) {
  return [...String(value || "").matchAll(/\b(?:18|19|20)\d{2}\b/g)].map(match => Number(match[0]));
}

function uxTemporalRange(product) {
  const years = uxYears(product.temporal_coverage);
  if (!years.length) return null;
  return {start: Math.min(...years), end: Math.max(...years)};
}

function uxCoverageContainsPeriod(product, requestedStart, requestedEnd) {
  if (!requestedStart && !requestedEnd) return true;
  const range = uxTemporalRange(product);
  if (!range) return false;
  const start = requestedStart ? Number(requestedStart) : null;
  const end = requestedEnd ? Number(requestedEnd) : null;
  if (start && end) return range.start <= start && range.end >= end;
  if (start) return range.start <= start && range.end >= start;
  return range.start <= end && range.end >= end;
}

function uxAccessMethods(product) {
  return unique(product.distributions.flatMap(distribution => [distribution.access_protocol, distribution.access_tool]).flatMap(split));
}

function uxLicenses(product) {
  return unique(product.distributions.flatMap(distribution => split(distribution.license)));
}

function uxFree(product) {
  return aggregateEnum(product.distributions.map(distribution => distribution.free_download));
}

function uxConceptsInQuery(raw) {
  const query = uxText(raw);
  return UX_CONCEPTS.filter(concept => concept.aliases.some(alias => query.includes(norm(alias))));
}

function uxResolutionInQuery(raw) {
  const query = uxText(raw).replace(",", ".");
  const match = query.match(/\b\d+(?:\.\d+)?\s?(?:m|km)\b/);
  return match ? match[0].replace(/\s+/g, "") : "";
}

function uxRenderInterpretation(raw) {
  if (!els.queryInterpretation) return;
  const concepts = uxConceptsInQuery(raw).map(concept => concept.label);
  const years = uxYears(raw);
  const resolution = uxResolutionInQuery(raw);
  const labels = unique([
    ...concepts,
    ...(years.length ? [`período: ${years.join("–")}`] : []),
    ...(resolution ? [`escala: ${resolution}`] : [])
  ]);
  els.queryInterpretation.hidden = labels.length === 0;
  els.queryInterpretation.innerHTML = labels.map(label => `<span>${esc(label)}</span>`).join("");
}

function uxConceptMatches(product, concept) {
  if (concept.key === "brazil") return product.covers_brazil === "sim" || product.covers_brazil === "parcial" || product._search.includes("brasil") || product._search.includes("brazil");
  return concept.aliases.some(alias => product._search.includes(norm(alias)));
}

function uxProductMatchesQuery(product, raw) {
  const query = uxText(raw).trim();
  if (!query) return true;

  const years = uxYears(query);
  if (years.length) {
    const range = uxTemporalRange(product);
    if (!range || years.some(year => year < range.start || year > range.end)) return false;
  }

  const requestedResolution = uxResolutionInQuery(query);
  if (requestedResolution) {
    const productResolution = uxText(product.spatial_resolution).replace(/\s+/g, "");
    if (!productResolution.includes(requestedResolution)) return false;
  }

  const terms = query.split(/\s+/).filter(Boolean).filter(term => !UX_STOPWORDS.has(term)).filter(term => !/^\d{4}$/.test(term)).filter(term => !/^(m|km)$/.test(term));
  return terms.every(term => {
    const concept = UX_TOKEN_TO_CONCEPT.get(term);
    if (concept) return uxConceptMatches(product, concept);
    return product._search.includes(term);
  });
}

function uxCompletenessScore(product) {
  const fields = [
    product.product_description, product.geographic_coverage, product.temporal_coverage,
    product.temporal_resolution, product.spatial_support, product.spatial_resolution,
    product.version_or_collection, product.update_frequency, product.limitations,
    product.methodology_url, product.last_verified
  ];
  let score = fields.filter(value => value && !/^(não informado|desconhecido|varia)$/i.test(String(value).trim())).length;
  if (product.distributions.some(distribution => validUrl(distribution.access_url))) score += 2;
  if (product.distributions.some(distribution => distribution.license && !/desconhecido/i.test(distribution.license))) score += 1;
  return score;
}

function uxBrazilScore(product) {
  if (product.covers_brazil === "sim") return 3;
  if (product.covers_brazil === "parcial") return 2;
  if (product._search.includes("brasil") || product._search.includes("brazil")) return 1;
  return 0;
}

function uxSourceOriginScore(product) {
  const priority = UX_SOURCE_PRIORITY.get(product.resource_id);
  return priority == null ? 0 : Math.max(0, 100 - priority);
}

function uxRelevanceScore(product, raw) {
  const query = uxText(raw).trim();
  if (!query) return 0;
  const name = uxText(product.product_name);
  const acronym = uxText(product.product_acronym);
  const areas = uxText(product.research_areas);
  const keywords = uxText(product.keywords);
  const description = uxText(product.product_description);
  const coverage = uxText(product.geographic_coverage);
  let score = 0;
  if (name === query) score += 150;
  if (name.startsWith(query)) score += 80;
  if (name.includes(query)) score += 50;
  if (acronym === query) score += 60;
  uxConceptsInQuery(query).forEach(concept => { if (uxConceptMatches(product, concept)) score += 18; });
  query.split(/\s+/).filter(term => !UX_STOPWORDS.has(term)).forEach(term => {
    if (name.includes(term)) score += 14;
    if (keywords.includes(term)) score += 10;
    if (areas.includes(term)) score += 9;
    if (description.includes(term)) score += 5;
    if (coverage.includes(term)) score += 4;
  });
  return score;
}

searchableText = function(product) {
  return norm([
    product.product_name, product.product_acronym, product.product_family,
    product.product_kind, product.product_description, product.research_areas,
    product.keywords, product.geographic_coverage, product.spatial_support,
    product.spatial_resolution, product.temporal_coverage, product.temporal_resolution,
    product.update_frequency, product.product_status, product.version_or_collection,
    product.primary_or_derived, product.limitations,
    product.source.resource_name, product.source.acronym, product.source.official_identity,
    ...product.distributions.flatMap(distribution => [
      distribution.distribution_name, distribution.format, distribution.access_protocol,
      distribution.access_tool, distribution.access_conditions, distribution.license,
      distribution.subset_support
    ])
  ].join(" "));
};

productMatchesQuery = function(product, query) {
  return uxProductMatchesQuery(product, query);
};

populateFilters = function() {
  populateSelect(els.source, all.map(product => product.source.resource_name), "Todas as fontes");
  populateSelect(els.area, all.flatMap(product => split(product.research_areas)), "Todos os temas e áreas");
  populateSelect(els.brazil, all.map(product => product.covers_brazil), "Qualquer abrangência", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.kind, all.map(product => product.product_kind), "Todos os tipos", null, KIND_LABELS);
  populateSelect(els.format, all.flatMap(productFormats), "Todos os formatos");
  populateSelect(els.protocol, all.flatMap(productProtocols), "Todos os protocolos");
  populateSelect(els.auth, all.flatMap(product => product.distributions.map(item => item.authentication_required)), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.status, all.map(product => product.product_status), "Todos os estados");
  populateSelect(els.origin, all.map(product => product.primary_or_derived), "Qualquer origem", null, ORIGIN_LABELS);
  populateSelect(els.temporal, all.map(product => product.temporal_resolution), "Qualquer resolução temporal");
  populateSelect(els.spatialSupport, all.map(product => product.spatial_support), "Qualquer suporte espacial");
  populateSelect(els.spatialResolution, all.map(product => product.spatial_resolution), "Qualquer resolução espacial");
  populateSelect(els.access, all.flatMap(uxAccessMethods), "Qualquer forma de acesso");
  populateSelect(els.free, all.map(uxFree), "Gratuito ou restrito", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.license, all.flatMap(uxLicenses), "Qualquer licença");
};

function uxSelectedLabel(element) {
  if (!element || !element.value) return "";
  return optionLabel(element);
}

renderActiveFilters = function() {
  const items = [];
  if (els.q.value.trim()) items.push({key:"q", label:`Busca: ${els.q.value.trim()}`});
  if (els.coverage.value.trim()) items.push({key:"coverage", label:`Geografia: ${els.coverage.value.trim()}`});
  if (els.yearStart.value || els.yearEnd.value) items.push({key:"period", label:`Período: ${els.yearStart.value || "…"}–${els.yearEnd.value || "…"}`});
  [
    ["area","Tema",els.area], ["temporal","Resolução temporal",els.temporal],
    ["spatialSupport","Suporte espacial",els.spatialSupport], ["spatialResolution","Resolução espacial",els.spatialResolution],
    ["access","Acesso",els.access], ["format","Formato",els.format], ["free","Gratuidade",els.free],
    ["source","Fonte",els.source], ["brazil","Brasil",els.brazil], ["kind","Tipo",els.kind],
    ["license","Licença",els.license], ["auth","Autenticação",els.auth], ["status","Estado",els.status], ["origin","Origem",els.origin]
  ].forEach(([key,label,element]) => { if (element && element.value) items.push({key,label:`${label}: ${uxSelectedLabel(element)}`}); });

  const advancedActive = [els.source,els.brazil,els.kind,els.license,els.auth,els.status,els.origin].filter(element => element && element.value).length;
  els.advancedCount.textContent = advancedActive ? `(${advancedActive} ${advancedActive === 1 ? "ativo" : "ativos"})` : "";
  if (advancedActive) els.advancedFilters.open = true;

  els.activeFilters.hidden = items.length === 0;
  els.activeFilters.innerHTML = items.length ? `<span>Filtros ativos:</span>${items.map(item => `<button type="button" data-remove="${item.key}" aria-label="Remover ${esc(item.label)}">${esc(item.label)} <b aria-hidden="true">×</b></button>`).join("")}` : "";
  els.activeFilters.querySelectorAll("[data-remove]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.remove;
    if (key === "q") els.q.value = "";
    else if (key === "coverage") els.coverage.value = "";
    else if (key === "period") { els.yearStart.value = ""; els.yearEnd.value = ""; }
    else if (els[key]) els[key].value = "";
    filter();
  }));
};

writeUrl = function() {
  const params = new URLSearchParams();
  const values = {
    q:els.q.value.trim(), area:els.area.value, coverage:els.coverage.value.trim(),
    from:els.yearStart.value, to:els.yearEnd.value, temporal:els.temporal.value,
    support:els.spatialSupport.value, spatial:els.spatialResolution.value,
    access:els.access.value, format:els.format.value, free:els.free.value,
    source:els.source.value, brazil:els.brazil.value, kind:els.kind.value,
    license:els.license.value, auth:els.auth.value, status:els.status.value, origin:els.origin.value,
    sort:els.sort.value === "relevance" ? "" : els.sort.value
  };
  Object.entries(values).forEach(([key,value]) => { if (value) params.set(key,value); });
  const query = params.toString();
  history.replaceState(null,"",`${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
};

readUrl = function() {
  const params = new URLSearchParams(location.search);
  els.q.value = params.get("q") || "";
  els.coverage.value = params.get("coverage") || "";
  els.yearStart.value = params.get("from") || "";
  els.yearEnd.value = params.get("to") || "";
  setSelectFromParam(els.area, params.get("area"));
  setSelectFromParam(els.temporal, params.get("temporal"));
  setSelectFromParam(els.spatialSupport, params.get("support"));
  setSelectFromParam(els.spatialResolution, params.get("spatial"));
  setSelectFromParam(els.access, params.get("access"));
  setSelectFromParam(els.format, params.get("format"));
  setSelectFromParam(els.free, params.get("free"));
  setSelectFromParam(els.source, params.get("source"));
  setSelectFromParam(els.brazil, params.get("brazil"));
  setSelectFromParam(els.kind, params.get("kind"));
  setSelectFromParam(els.license, params.get("license"));
  setSelectFromParam(els.auth, params.get("auth"));
  setSelectFromParam(els.status, params.get("status"));
  setSelectFromParam(els.origin, params.get("origin"));
  setSelectFromParam(els.sort, params.get("sort"));
};

sortResults = function(query) {
  const byName = (a,b) => a.product_name.localeCompare(b.product_name,"pt-BR");
  if (els.sort.value === "verified") {
    filtered.sort((a,b) => String(b.last_verified).localeCompare(String(a.last_verified)) || byName(a,b));
    return;
  }
  if (els.sort.value === "name") {
    filtered.sort(byName);
    return;
  }
  if (els.sort.value === "source") {
    filtered.sort((a,b) => a.source.resource_name.localeCompare(b.source.resource_name,"pt-BR") || byName(a,b));
    return;
  }
  filtered.sort((a,b) =>
    uxRelevanceScore(b,query) - uxRelevanceScore(a,query) ||
    uxBrazilScore(b) - uxBrazilScore(a) ||
    uxCompletenessScore(b) - uxCompletenessScore(a) ||
    uxSourceOriginScore(b) - uxSourceOriginScore(a) ||
    byName(a,b)
  );
};

filter = function(syncUrl = true) {
  const rawQuery = els.q.value.trim();
  const coverage = uxText(els.coverage.value.trim());
  filtered = all.filter(product =>
    uxProductMatchesQuery(product, rawQuery) &&
    (!els.area.value || split(product.research_areas).includes(els.area.value)) &&
    (!coverage || uxText(product.geographic_coverage).includes(coverage) || uxText(product.keywords).includes(coverage)) &&
    uxCoverageContainsPeriod(product, els.yearStart.value, els.yearEnd.value) &&
    (!els.temporal.value || product.temporal_resolution === els.temporal.value) &&
    (!els.spatialSupport.value || product.spatial_support === els.spatialSupport.value) &&
    (!els.spatialResolution.value || product.spatial_resolution === els.spatialResolution.value) &&
    (!els.access.value || uxAccessMethods(product).includes(els.access.value)) &&
    (!els.format.value || productFormats(product).includes(els.format.value)) &&
    (!els.free.value || uxFree(product) === els.free.value) &&
    (!els.source.value || product.source.resource_name === els.source.value) &&
    (!els.brazil.value || product.covers_brazil === els.brazil.value) &&
    (!els.kind.value || product.product_kind === els.kind.value) &&
    (!els.license.value || uxLicenses(product).includes(els.license.value)) &&
    (!els.auth.value || product.distributions.some(item => item.authentication_required === els.auth.value)) &&
    (!els.status.value || product.product_status === els.status.value) &&
    (!els.origin.value || product.primary_or_derived === els.origin.value)
  );
  sortResults(rawQuery);
  visibleCount = PAGE_SIZE;
  render();
  renderActiveFilters();
  uxRenderInterpretation(rawQuery);
  if (syncUrl) writeUrl();
};

function uxShort(value, max = 150) {
  const text = String(value || "Não informado").trim();
  return text.length > max ? `${text.slice(0,max - 1).trim()}…` : text;
}

function uxAccessSummary(product) {
  const formats = productFormats(product).slice(0,2);
  const methods = uxAccessMethods(product).slice(0,1);
  const free = uxFree(product) === "sim" ? "gratuito" : uxFree(product) === "parcial" ? "parcialmente gratuito" : "acesso condicionado";
  return unique([...formats,...methods,free]).join(" · ") || "Consultar formas de acesso";
}

productCard = function(product) {
  const cardId = `product-${domId(product.product_id)}`;
  const descriptionId = `${cardId}-description`;
  const areas = split(product.research_areas);
  const formats = productFormats(product);
  const checked = selected.has(product.product_id) ? " checked" : "";
  const acronym = product.product_acronym ? `<span class="acronym">${esc(product.product_acronym)}</span>` : "";
  const limitation = uxShort(product.limitations,135);
  const access = uxAccessSummary(product);

  return `<article class="card product-card" data-product-id="${esc(product.product_id)}" role="listitem" aria-labelledby="${cardId}" aria-describedby="${descriptionId}">
    <header class="card-header"><div class="card-title">
      <p class="product-source"><a href="sources.html?q=${encodeURIComponent(product.source.resource_name)}#catalogo">${esc(product.source.resource_name)}</a></p>
      <div class="title-line"><h3 id="${cardId}">${esc(product.product_name)}</h3>${acronym}</div>
      <p class="identity">${esc(product.product_family)} · ${esc(KIND_LABELS[product.product_kind] || product.product_kind)}</p>
    </div></header>
    <p class="description" id="${descriptionId}">${esc(product.product_description)}</p>
    <div class="product-triage" aria-label="Resumo para seleção científica">
      <div class="triage-item"><span>Onde?</span><strong>${esc(uxShort(product.geographic_coverage,90))}</strong></div>
      <div class="triage-item"><span>Quando?</span><strong>${esc(uxShort(product.temporal_coverage,90))}</strong></div>
      <div class="triage-item"><span>Em que escala?</span><strong>${esc(uxShort(unique([product.spatial_resolution,product.temporal_resolution]).filter(Boolean).join(" · ") || product.spatial_support,90))}</strong></div>
      <div class="triage-item"><span>Como acessar?</span><strong>${esc(uxShort(access,90))}</strong></div>
    </div>
    <div class="chips" aria-label="Temas e áreas">${areas.slice(0,5).map(area => `<span class="chip">${esc(area)}</span>`).join("")}</div>
    <div class="chips product-format-chips" aria-label="Formatos e modalidades">${formats.slice(0,5).map(format => `<span class="chip">${esc(format)}</span>`).join("")}</div>
    <div class="limitation-flag"><strong>Atenção:</strong><span>${esc(limitation)}</span></div>
    <div class="card-actions">
      ${actionLink("Acessar produto", product.product_page_url, "action-primary")}
      ${actionLink("Metodologia", product.methodology_url)}
    </div>
    <label class="compare-toggle"><input type="checkbox" data-compare="${esc(product.product_id)}"${checked}><span>Selecionar para comparar</span></label>
    <details class="card-details"><summary aria-label="Ver detalhes e formas de acesso de ${esc(product.product_name)}">Ver detalhes, proveniência e acessos (${product.distributions.length})</summary>
      <div class="detail-groups">
        <section class="detail-group"><h4>Detalhes científicos do produto</h4><div class="detail-grid">
          ${detail("Cobertura geográfica",product.geographic_coverage)}${detail("Cobertura temporal",product.temporal_coverage)}
          ${detail("Suporte espacial",product.spatial_support)}${detail("Resolução espacial",product.spatial_resolution)}
          ${detail("Resolução temporal",product.temporal_resolution)}${detail("Atualização",product.update_frequency)}
          ${detail("Versão ou coleção",product.version_or_collection)}${detail("Estado",product.product_status)}
          ${detail("Origem",ORIGIN_LABELS[product.primary_or_derived] || product.primary_or_derived)}${detail("Palavras-chave",product.keywords)}
          ${detail("Limitações",product.limitations)}${detail("Registro revisado em",product.last_verified)}
          ${detail("Fonte / provedor",product.source.resource_name)}${detail("Identidade da fonte",product.source.official_identity)}
        </div></section>
        <section class="detail-group"><h4>Formas de acesso</h4><div class="product-distributions">${product.distributions.map(accessCard).join("")}</div></section>
      </div>
    </details>
  </article>`;
};

function uxComparisonRows() {
  return [
    ["Fonte","source"],["Descrição","description"],["Cobertura geográfica","coverage"],
    ["Suporte e resolução espacial","spatial"],["Cobertura e resolução temporal","temporal"],
    ["Atualização","update"],["Versão ou coleção","version"],["Origem","origin"],
    ["Formatos","formats"],["Protocolos / ferramentas","protocols"],["Download gratuito","free"],
    ["Autenticação","auth"],["Limitações","limitations"],["Registro revisado em","verified"]
  ];
}

function uxRenderComparison() {
  const products = [...selected].map(id => all.find(product => product.product_id === id)).filter(Boolean);
  if (!products.length) return;
  const rows = uxComparisonRows();
  els.compareContent.innerHTML = `<div class="compare-table-wrap"><table class="compare-table"><thead><tr><th scope="col">Dimensão</th>${products.map(product => `<th scope="col"><div class="compare-product-heading"><span>${esc(product.product_name)}</span><button type="button" class="compare-remove" data-remove-compare="${esc(product.product_id)}">Remover</button></div></th>`).join("")}</tr></thead><tbody>${rows.map(([label,key]) => {
    const values = products.map(product => comparisonValue(product,key));
    const different = new Set(values.map(uxText)).size > 1;
    return `<tr${different ? ` class="is-different"` : ""}><th scope="row">${esc(label)}</th>${values.map(value => `<td>${esc(value)}</td>`).join("")}</tr>`;
  }).join("")}</tbody></table></div><p class="compare-reset-note">Você pode remover produtos aqui. Ao fechar esta janela, a seleção é reiniciada automaticamente.</p>`;
  els.compareContent.querySelectorAll("[data-remove-compare]").forEach(button => button.addEventListener("click", () => {
    const id = button.dataset.removeCompare;
    selected.delete(id);
    document.querySelectorAll(`[data-compare="${CSS.escape(id)}"]`).forEach(input => { input.checked = false; });
    renderCompareBar();
    if (selected.size === 0) els.compareDialog.close();
    else uxRenderComparison();
  }));
}

openComparison = function() {
  if (selected.size < 2) {
    els.compareStatus.textContent = "Selecione pelo menos dois produtos.";
    return;
  }
  uxRenderComparison();
  if (typeof els.compareDialog.showModal === "function") els.compareDialog.showModal();
  else els.compareDialog.setAttribute("open","");
};

function uxResetSelection() {
  selected.clear();
  document.querySelectorAll("[data-compare]").forEach(input => { input.checked = false; });
  renderCompareBar();
}

clearComparison = function() {
  uxResetSelection();
  if (els.compareDialog.open) els.compareDialog.close();
};

els.compareDialog.addEventListener("close", uxResetSelection);

[els.coverage,els.yearStart,els.yearEnd,els.temporal,els.spatialSupport,els.spatialResolution,els.access,els.free,els.license]
  .filter(Boolean)
  .forEach(element => element.addEventListener(element.tagName === "INPUT" ? "input" : "change", () => filter()));

fetch("data/brazil_scope_priorities.json")
  .then(response => response.ok ? response.json() : null)
  .then(registry => {
    if (!registry?.tiers) return;
    registry.tiers.forEach((tier,order) => tier.resource_ids.forEach(resourceId => UX_SOURCE_PRIORITY.set(resourceId,order)));
    if (all.length) filter(false);
  })
  .catch(() => {});
