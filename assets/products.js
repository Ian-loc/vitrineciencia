const $ = selector => document.querySelector(selector);

const els = {
  q: $("#product-q"),
  theme: $("#product-theme"),
  coverage: $("#product-coverage"),
  yearStart: $("#product-year-start"),
  yearEnd: $("#product-year-end"),
  temporal: $("#product-temporal"),
  support: $("#product-support"),
  spatial: $("#product-spatial"),
  access: $("#product-access"),
  format: $("#product-format"),
  free: $("#product-free"),
  license: $("#product-license"),
  area: $("#product-area"),
  source: $("#product-source"),
  kind: $("#product-kind"),
  auth: $("#product-auth"),
  status: $("#product-status"),
  origin: $("#product-origin"),
  brazil: $("#product-brazil"),
  sort: $("#product-sort"),
  list: $("#product-list"),
  empty: $("#product-empty"),
  count: $("#product-count"),
  activeFilters: $("#product-active-filters"),
  advancedFilters: $("#product-advanced-filters"),
  advancedCount: $("#product-advanced-count"),
  searchForm: $("#product-search"),
  catalogHeading: $("#product-catalog-heading"),
  resultsMore: $("#product-results-more"),
  showMore: $("#product-show-more"),
  shownCount: $("#product-shown-count"),
  insights: $("#product-result-insights"),
  interpreted: $("#interpreted-query"),
  compareBar: $("#compare-bar"),
  compareCount: $("#compare-count"),
  compareStatus: $("#compare-status"),
  compareDialog: $("#compare-dialog"),
  compareContent: $("#compare-content")
};

const PAGE_SIZE = 18;
const MAX_COMPARE = 3;
const CURRENT_YEAR = 2026;
let all = [];
let filtered = [];
let visibleCount = PAGE_SIZE;
const selected = new Set();

const ENUM_ORDER = ["sim", "parcial", "não", "desconhecido", "não se aplica"];
const ENUM_LABELS = {
  "sim": "Sim", "parcial": "Parcial", "não": "Não",
  "desconhecido": "Desconhecido", "não se aplica": "Não se aplica"
};
const KIND_LABELS = {
  dataset: "Conjunto de dados", dataset_series: "Série de conjuntos de dados",
  data_service: "Serviço de dados", catalog: "Catálogo",
  federated_catalog: "Catálogo federado", indicator_family: "Família de indicadores",
  map_layer_collection: "Coleção de camadas cartográficas", software_output: "Saída de software"
};
const ORIGIN_LABELS = {
  primário: "Primário", derivado: "Derivado", agregador: "Agregador",
  serviço: "Serviço", misto: "Misto", desconhecido: "Desconhecido"
};

const THEME_GROUPS = [
  {key:"carbono", label:"Carbono", terms:["carbono","carbon","carbon stock","carbon cycle","emission","emissions","co2"]},
  {key:"biomassa", label:"Biomassa", terms:["biomassa","biomass","agb","aboveground biomass"]},
  {key:"solo", label:"Solos", terms:["solo","soil","soils","pedologia","pedology"]},
  {key:"agua", label:"Água e hidrologia", terms:["água","agua","water","hydrology","hidrologia","river","rio","streamflow","vazão","vazao"]},
  {key:"clima", label:"Clima e atmosfera", terms:["clima","climate","precipitation","precipitação","precipitacao","rainfall","chuva","temperature","temperatura","atmosphere","atmosfera"]},
  {key:"uso_terra", label:"Uso e cobertura da terra", terms:["uso da terra","land use","land-use","cobertura do solo","land cover","lulc"]},
  {key:"desmatamento", label:"Desmatamento e degradação", terms:["desmatamento","deforestation","forest loss","degradação","degradacao","degradation"]},
  {key:"fogo", label:"Fogo e queimadas", terms:["fogo","fire","wildfire","burned area","área queimada","area queimada","hotspot"]},
  {key:"biodiversidade", label:"Biodiversidade e espécies", terms:["biodiversidade","biodiversity","species","espécies","especies","occurrence","ocorrência","ocorrencia"]},
  {key:"vegetacao", label:"Vegetação e florestas", terms:["vegetação","vegetacao","vegetation","forest","floresta","forestry","native vegetation","vegetação nativa"]},
  {key:"restauracao", label:"Restauração e regeneração", terms:["restauração","restauracao","restoration","regeneração","regeneracao","regrowth","secondary vegetation"]},
  {key:"agro", label:"Agricultura e pecuária", terms:["agriculture","agricultura","livestock","pecuária","pecuaria","pasture","pastagem","crop","cultura agrícola"]},
  {key:"territorio", label:"Território e sociedade", terms:["population","população","populacao","demography","demografia","socioeconomic","socioeconom","território","territorio","governance","governança","governanca"]},
  {key:"geociencias", label:"Geociências e relevo", terms:["geology","geologia","geomorphology","geomorfologia","topography","topografia","elevation","elevação","elevacao","terrain","relevo"]},
  {key:"sensoriamento", label:"Sensoriamento e geoinformação", terms:["remote sensing","sensoriamento remoto","satellite","satélite","satelite","geospatial","geoespacial","earth observation"]},
  {key:"saude", label:"Saúde", terms:["health","saúde","saude","epidemiology","epidemiologia"]}
];

const BIOME_GROUPS = [
  {key:"amazonia", label:"Amazônia", terms:["amazonia","amazon","amazônia"]},
  {key:"cerrado", label:"Cerrado", terms:["cerrado"]},
  {key:"mata_atlantica", label:"Mata Atlântica", terms:["mata atlantica","mata atlântica","atlantic forest"]},
  {key:"caatinga", label:"Caatinga", terms:["caatinga"]},
  {key:"pantanal", label:"Pantanal", terms:["pantanal"]},
  {key:"pampa", label:"Pampa", terms:["pampa"]}
];

const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
const unique = values => [...new Set(values.filter(Boolean))];
const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const validUrl = value => /^https:\/\//.test(String(value || ""));
const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const domId = value => String(value || "product").replace(/[^a-zA-Z0-9_-]/g, "-");
const labelArea = value => window.VitrinePTBR?.labelArea ? window.VitrinePTBR.labelArea(value) : value;

function productFormatsRaw(product) {
  return unique((product.distributions || []).flatMap(distribution => split(distribution.format)));
}
function productProtocols(product) {
  return unique((product.distributions || []).flatMap(distribution => [distribution.access_protocol, distribution.access_tool]));
}
function aggregateEnum(values) {
  const clean = values.filter(Boolean);
  if (clean.includes("sim")) return "sim";
  if (clean.includes("parcial")) return "parcial";
  if (clean.length && clean.every(value => value === "não")) return "não";
  if (clean.includes("desconhecido")) return "desconhecido";
  return clean[0] || "desconhecido";
}

function productSearchBase(product) {
  return norm([
    product.product_name, product.product_acronym, product.product_family, product.product_kind,
    product.product_description, product.research_areas, product.keywords, product.geographic_coverage,
    product.spatial_support, product.spatial_resolution, product.temporal_coverage, product.temporal_resolution,
    product.update_frequency, product.product_status, product.version_or_collection, product.primary_or_derived,
    product.limitations, product.source?.resource_name, product.source?.acronym, product.source?.official_identity,
    ...(product.distributions || []).flatMap(distribution => [
      distribution.distribution_name, distribution.format, distribution.access_protocol,
      distribution.access_tool, distribution.access_conditions, distribution.license,
      distribution.subset_support
    ])
  ].join(" "));
}

function themeMatches(product, key) {
  const group = THEME_GROUPS.find(item => item.key === key);
  return group ? group.terms.some(term => product._search.includes(norm(term))) : true;
}
function biomeMatches(product, key) {
  const group = BIOME_GROUPS.find(item => item.key === key);
  return group ? group.terms.some(term => product._search.includes(norm(term))) : true;
}

function temporalBucket(product) {
  const text = norm(product.temporal_resolution);
  if (!text || /desconhe|nao inform|variav/.test(text)) return "desconhecida";
  if (/minut|hour|hora|3-hour|subdiar|sub-di/.test(text)) return "subdiaria";
  if (/daily|diari|dia\b/.test(text)) return "diaria";
  if (/week|seman/.test(text)) return "semanal";
  if (/month|mensal|mes\b/.test(text)) return "mensal";
  if (/quarter|trimestr/.test(text)) return "trimestral";
  if (/season|sazon/.test(text)) return "sazonal";
  if (/annual|anual|yearly|ano\b/.test(text)) return "anual";
  if (/continu|tempo real|real time|near-real|near real/.test(text)) return "continua";
  if (/decad|plurian|multi.?year|irregular|event/.test(text)) return "outra";
  return "outra";
}

function supportBucket(product) {
  const text = norm(product.spatial_support);
  if (!text || /desconhe|nao inform/.test(text)) return "desconhecido";
  if (/point|ponto|station|estacao|estação|site\b|parcela/.test(text)) return "ponto";
  if (/pixel|raster|grid|grade|cell|celula|célula/.test(text)) return "grade";
  if (/municip|admin|uf\b|estado\b|state\b|censo|census/.test(text)) return "administrativo";
  if (/basin|bacia|watershed|sub-bacia|subbacia/.test(text)) return "bacia";
  if (/polygon|polig|políg|vector|vetor|feature/.test(text)) return "poligono";
  if (/region|regiao|região|territor|zone|zona|area\b|área/.test(text)) return "regiao";
  if (/national|nacional|country|pais\b|país|global/.test(text)) return "nacional_global";
  if (/table|tabular|non.?spatial|sem componente espacial/.test(text)) return "tabular";
  return "outro";
}

function extractMeters(textValue) {
  const text = norm(textValue).replace(/,/g, ".");
  const match = text.match(/(?:^|[^\d])(\d+(?:\.\d+)?)\s*(km|m)\b/);
  if (!match) return null;
  const value = Number(match[1]);
  return match[2] === "km" ? value * 1000 : value;
}
function spatialBucket(product) {
  const text = norm(product.spatial_resolution);
  if (!text || /desconhe|nao inform/.test(text)) return "desconhecida";
  if (/municip|admin|uf\b|estado\b|state\b|censo|regiao|região/.test(text)) return "administrativa";
  if (/variav|depende|multiple|multipla|múltipla/.test(text)) return "variavel";
  const meters = extractMeters(text);
  if (meters === null) return "outra";
  if (meters <= 10) return "ate10m";
  if (meters <= 30) return "10a30m";
  if (meters <= 100) return "30a100m";
  if (meters <= 1000) return "100m1km";
  if (meters <= 10000) return "1a10km";
  return "mais10km";
}

function productAccessCategories(product) {
  const text = norm((product.distributions || []).flatMap(d => [d.access_protocol,d.access_tool,d.format,d.access_conditions,d.distribution_name]).join(" "));
  const out = [];
  if (/google earth engine|\bgee\b/.test(text)) out.push("gee");
  if (/\bapi\b|rest|graphql|opendap/.test(text)) out.push("api");
  if (/\bwms\b|\bwfs\b|wmts|ogc/.test(text)) out.push("ogc");
  if (/sql|database|banco de dados|bigquery|duckdb/.test(text)) out.push("banco");
  if (/download|baixar|arquivo|file|csv|geotiff|tiff|shapefile|netcdf|parquet|xlsx|zip/.test(text)) out.push("arquivo");
  if (/web|portal|viewer|visualizador|consulta|dashboard|painel|mapa/.test(text)) out.push("web");
  return unique(out.length ? out : ["outro"]);
}

function productFormatCategories(product) {
  const text = norm(productFormatsRaw(product).join(" "));
  const out = [];
  if (/geotiff|geo.?tiff|\btiff?\b/.test(text)) out.push("geotiff");
  if (/\bcsv\b/.test(text)) out.push("csv");
  if (/shapefile|\bshp\b/.test(text)) out.push("shapefile");
  if (/geojson/.test(text)) out.push("geojson");
  if (/netcdf|\bnc\b/.test(text)) out.push("netcdf");
  if (/parquet/.test(text)) out.push("parquet");
  if (/\bjson\b/.test(text) && !/geojson/.test(text)) out.push("json");
  if (/kml|kmz/.test(text)) out.push("kml");
  if (/xlsx|xls|excel/.test(text)) out.push("excel");
  if (/raster/.test(text)) out.push("raster");
  if (/vector|vetor/.test(text)) out.push("vetor");
  return unique(out.length ? out : ["outro"]);
}

function productLicenseCategory(product) {
  const text = norm((product.distributions || []).map(d => d.license).join(" "));
  if (!text || /desconhe|nao inform|não inform/.test(text)) return "nao_informada";
  if (/cc ?by|cc0|creative commons|odbl|open data commons|public domain|dominio publico|domínio público/.test(text)) return "aberta";
  return "outros_termos";
}

function temporalRange(product) {
  const text = String(product.temporal_coverage || "");
  const years = [...text.matchAll(/\b(19\d{2}|20\d{2})\b/g)].map(match => Number(match[1]));
  if (!years.length) return null;
  let start = Math.min(...years);
  let end = Math.max(...years);
  if (/presente|atual|current|ongoing|present/i.test(text)) end = Math.max(end, CURRENT_YEAR);
  return {start, end};
}
function coversRequestedPeriod(product, startValue, endValue) {
  if (!startValue && !endValue) return true;
  const range = product._temporalRange;
  if (!range) return false;
  const start = startValue ? Number(startValue) : null;
  const end = endValue ? Number(endValue) : null;
  if (start && range.end < start) return false;
  if (end && range.start > end) return false;
  if (start && end) return range.start <= start && range.end >= end;
  return true;
}

function parseQuery(queryValue) {
  const raw = norm(queryValue);
  const concepts = THEME_GROUPS.filter(group => group.terms.some(term => raw.includes(norm(term))));
  const biomes = BIOME_GROUPS.filter(group => group.terms.some(term => raw.includes(norm(term))));
  const brazil = /\bbrasil\b|\bbrazil\b/.test(raw);
  const years = unique([...raw.matchAll(/\b(19\d{2}|20\d{2})\b/g)].map(match => match[1]));
  const resolution = raw.match(/\b(\d+(?:[.,]\d+)?)\s*(m|km)\b/);

  let residual = raw;
  [...concepts, ...biomes].flatMap(item => item.terms).forEach(term => {
    residual = residual.replaceAll(norm(term), " ");
  });
  residual = residual.replace(/\bbrasil\b|\bbrazil\b/g, " ");
  residual = residual.replace(/\b(?:19\d{2}|20\d{2})\b/g, " ");
  residual = residual.replace(/\b\d+(?:[.,]\d+)?\s*(?:m|km)\b/g, " ");
  const terms = residual.split(/\s+/).filter(term => term.length > 1);
  const labels = [
    ...concepts.map(item => `tema: ${item.label}`),
    ...biomes.map(item => `bioma: ${item.label}`),
    ...(brazil ? ["geografia: Brasil"] : []),
    ...(years.length ? [`período: ${years.join("–")}`] : []),
    ...(resolution ? [`resolução: ${resolution[1].replace(",", ".")} ${resolution[2]}`] : [])
  ];
  return {raw, concepts, biomes, brazil, years, resolution, terms, labels};
}

function interpretedQueryMatches(product, parsed) {
  if (!parsed.raw) return true;
  if (parsed.concepts.length && !parsed.concepts.every(group => group.terms.some(term => product._search.includes(norm(term))))) return false;
  if (parsed.biomes.length && !parsed.biomes.every(group => group.terms.some(term => product._search.includes(norm(term))))) return false;
  if (parsed.brazil && !["sim","parcial"].includes(product.covers_brazil) && !/brasil|brazil/.test(product._search)) return false;
  if (parsed.terms.length && !parsed.terms.every(term => product._search.includes(term))) return false;
  if (parsed.years.length) {
    const range = product._temporalRange;
    if (!range) return false;
    if (!parsed.years.every(year => Number(year) >= range.start && Number(year) <= range.end)) return false;
  }
  if (parsed.resolution) {
    const wantedMeters = Number(parsed.resolution[1].replace(",", ".")) * (parsed.resolution[2] === "km" ? 1000 : 1);
    const actualMeters = extractMeters(product.spatial_resolution);
    if (actualMeters !== null) {
      const tolerance = Math.max(1, wantedMeters * 0.15);
      if (Math.abs(actualMeters - wantedMeters) > tolerance) return false;
    }
  }
  return true;
}

function brazilPriority(product) {
  if (product.covers_brazil === "sim") return 3;
  if (product.covers_brazil === "parcial") return 2;
  if (/brasil|brazil/.test(product._search)) return 1;
  return 0;
}
function documentationScore(product) {
  const fields = [
    product.product_page_url, product.methodology_url, product.geographic_coverage,
    product.temporal_coverage, product.spatial_support, product.spatial_resolution,
    product.temporal_resolution, product.limitations, product.version_or_collection,
    (product.distributions || []).some(d => d.license && !/desconhe|nao inform/.test(norm(d.license)))
  ];
  return fields.filter(Boolean).length;
}
function sourceOriginScore(product) {
  const text = norm(`${product.source?.official_identity || ""} ${product.source?.resource_name || ""}`);
  return /\bbrasil\b|\bbrazil\b|\bibge\b|\binpe\b|\bembrapa\b|\bana\b|\bmme\b|\bmma\b|\bipea\b|\bfiocruz\b/.test(text) ? 1 : 0;
}
function relevanceScore(product, parsed) {
  if (!parsed.raw) return 0;
  const name = norm(product.product_name);
  const acronym = norm(product.product_acronym);
  let score = 0;
  if (name === parsed.raw) score += 140;
  if (name.startsWith(parsed.raw)) score += 80;
  if (name.includes(parsed.raw)) score += 45;
  if (acronym && acronym === parsed.raw) score += 55;
  parsed.terms.forEach(term => {
    if (name.includes(term)) score += 18;
    else if (product._search.includes(term)) score += 7;
  });
  parsed.concepts.forEach(group => { if (group.terms.some(term => product._search.includes(norm(term)))) score += 25; });
  parsed.biomes.forEach(group => { if (group.terms.some(term => product._search.includes(norm(term)))) score += 18; });
  if (parsed.brazil && brazilPriority(product)) score += 10;
  if (parsed.years.length && product._temporalRange && parsed.years.every(y => Number(y) >= product._temporalRange.start && Number(y) <= product._temporalRange.end)) score += 12;
  if (parsed.resolution) {
    const wanted = Number(parsed.resolution[1].replace(",", ".")) * (parsed.resolution[2] === "km" ? 1000 : 1);
    const actual = extractMeters(product.spatial_resolution);
    if (actual !== null && Math.abs(actual - wanted) <= Math.max(1, wanted * 0.15)) score += 14;
  }
  return score;
}

function actionLink(label, url, className = "action-secondary") {
  return validUrl(url) ? `<a class="${className}" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span></a>` : "";
}
function detail(label, value) {
  return `<div class="detail"><strong>${esc(label)}</strong><span>${esc(value || "Não informado")}</span></div>`;
}
function licenses(product) {
  return unique((product.distributions || []).map(d => d.license)).join(" | ") || "Não informado";
}
function displayAccess(product) {
  const tools = unique((product.distributions || []).flatMap(d => [d.access_tool, d.access_protocol]).filter(Boolean));
  const formats = productFormatsRaw(product);
  const free = aggregateEnum((product.distributions || []).map(d => d.free_download));
  const parts = unique([...formats.slice(0,2), ...tools.slice(0,2)]).slice(0,3);
  if (free === "sim") parts.push("gratuito");
  else if (free === "parcial") parts.push("gratuito em parte");
  return parts.join(" · ") || "ver formas de acesso";
}
function displayScale(product) {
  const spatial = product.spatial_resolution && !/desconhe/i.test(product.spatial_resolution) ? product.spatial_resolution : product.spatial_support;
  const temporal = product.temporal_resolution && !/desconhe/i.test(product.temporal_resolution) ? product.temporal_resolution : "";
  return [spatial, temporal].filter(Boolean).join(" · ") || "não informado";
}
function areaChips(product) {
  const areas = split(product.research_areas).map(labelArea);
  const shown = areas.slice(0,2).map(area => `<span class="chip">${esc(area)}</span>`).join("");
  return shown + (areas.length > 2 ? `<span class="chip chip-more">+${areas.length - 2}</span>` : "");
}
function productCard(product) {
  const cardId = `product-${domId(product.product_id)}`;
  const descriptionId = `${cardId}-description`;
  const checked = selected.has(product.product_id) ? " checked" : "";
  const limitation = product.limitations && !/desconhe|nao inform|não inform/i.test(product.limitations)
    ? `<span class="limitation-flag">Limitação registrada</span>` : "";
  return `<article class="card product-card" data-product-id="${esc(product.product_id)}" role="listitem" aria-labelledby="${cardId}" aria-describedby="${descriptionId}">
    <header class="product-card-head">
      <p class="product-source">${esc(product.source?.resource_name || "Fonte não informada")}</p>
      <h3 id="${cardId}">${esc(product.product_name)}</h3>
      <p class="identity">${esc(product.product_family || KIND_LABELS[product.product_kind] || "Produto de dados")}</p>
    </header>
    <p class="description product-description" id="${descriptionId}">${esc(product.product_description)}</p>
    <div class="chips product-area-chips" aria-label="Áreas de pesquisa">${areaChips(product)}</div>
    <dl class="triage-strip" aria-label="Triagem científica rápida">
      <div><dt>Onde?</dt><dd>${esc(product.geographic_coverage || "Não informado")}</dd></div>
      <div><dt>Quando?</dt><dd>${esc(product.temporal_coverage || "Não informado")}</dd></div>
      <div><dt>Escala?</dt><dd>${esc(displayScale(product))}</dd></div>
      <div><dt>Acesso?</dt><dd>${esc(displayAccess(product))}</dd></div>
    </dl>
    <div class="product-card-bottom">${limitation}<span class="product-verified">Revisado: ${esc(product.last_verified || "não informado")}</span></div>
    <div class="card-actions compact-actions">
      ${actionLink("Acessar", product.product_page_url, "action-primary")}
      <label class="compare-toggle compact-compare"><input type="checkbox" data-compare="${esc(product.product_id)}"${checked}><span>Comparar</span></label>
    </div>
    <details class="card-details">
      <summary>Detalhes científicos e acesso</summary>
      <div class="detail-groups">
        <section class="detail-group"><h4>Produto</h4><div class="detail-grid">
          ${detail("Versão ou coleção", product.version_or_collection)}
          ${detail("Estado", product.product_status)}
          ${detail("Origem", ORIGIN_LABELS[product.primary_or_derived] || product.primary_or_derived)}
          ${detail("Cobertura geográfica", product.geographic_coverage)}
          ${detail("Cobertura temporal", product.temporal_coverage)}
          ${detail("Suporte espacial", product.spatial_support)}
          ${detail("Resolução espacial", product.spatial_resolution)}
          ${detail("Resolução temporal", product.temporal_resolution)}
          ${detail("Frequência de atualização", product.update_frequency)}
          ${detail("Licença(s)", licenses(product))}
          ${detail("Palavras-chave", product.keywords)}
          ${detail("Limitações", product.limitations)}
          ${detail("Provedor", product.source?.official_identity || product.source?.resource_name)}
          ${detail("Registro revisado em", product.last_verified)}
        </div><div class="detail-links">${actionLink("Metodologia", product.methodology_url)}${actionLink("Página do produto", product.product_page_url)}</div></section>
        <section class="detail-group"><h4>Formas de acesso</h4><div class="product-distributions">${(product.distributions || []).map(distribution => `<article class="distribution"><header><h5>${esc(distribution.distribution_name || "Acesso")}</h5>${actionLink("Abrir", distribution.access_url)}</header><div class="distribution-grid">${detail("Formato", distribution.format)}${detail("Protocolo", distribution.access_protocol)}${detail("Ferramenta", distribution.access_tool)}${detail("Download gratuito", ENUM_LABELS[distribution.free_download] || distribution.free_download)}${detail("Autenticação", ENUM_LABELS[distribution.authentication_required] || distribution.authentication_required)}${detail("Licença", distribution.license)}</div></article>`).join("")}</div></section>
      </div>
    </details>
  </article>`;
}

function populateSelect(element, entries, emptyLabel) {
  if (!element) return;
  element.innerHTML = "";
  element.add(new Option(emptyLabel, ""));
  entries.forEach(([value, label, count]) => element.add(new Option(count == null ? label : `${label} (${count})`, value)));
}
function countBy(values) {
  const map = new Map();
  values.filter(Boolean).forEach(value => map.set(value, (map.get(value) || 0) + 1));
  return map;
}
function sortedEntries(map, labeler = value => value) {
  return [...map.entries()].sort((a,b) => String(labeler(a[0])).localeCompare(String(labeler(b[0])), "pt-BR")).map(([value,count]) => [value,labeler(value),count]);
}

function populateFilters() {
  const themeCounts = new Map(THEME_GROUPS.map(group => [group.key, all.filter(p => themeMatches(p, group.key)).length]));
  populateSelect(els.theme, THEME_GROUPS.map(group => [group.key, group.label, themeCounts.get(group.key)]).filter(x => x[2] > 0), "Todos os temas");

  const temporalLabels = {subdiaria:"Subdiária",diaria:"Diária",semanal:"Semanal",mensal:"Mensal",trimestral:"Trimestral",sazonal:"Sazonal",anual:"Anual",continua:"Contínua / tempo real",outra:"Outra / irregular",desconhecida:"Não informada"};
  populateSelect(els.temporal, sortedEntries(countBy(all.map(temporalBucket)), value => temporalLabels[value] || value), "Qualquer resolução temporal");
  const supportLabels = {ponto:"Ponto / estação / parcela",grade:"Pixel / grade / raster",administrativo:"Unidade administrativa",bacia:"Bacia hidrográfica",poligono:"Polígono / feição",regiao:"Região / zona / território",nacional_global:"Nacional / país / global",tabular:"Sem suporte espacial explícito",outro:"Outro",desconhecido:"Não informado"};
  populateSelect(els.support, sortedEntries(countBy(all.map(supportBucket)), value => supportLabels[value] || value), "Qualquer suporte espacial");
  const spatialLabels = {ate10m:"≤ 10 m", "10a30m":"> 10–30 m", "30a100m":"> 30–100 m", "100m1km":"> 100 m–1 km", "1a10km":"> 1–10 km", mais10km:"> 10 km", administrativa:"Administrativa / agregada", variavel:"Variável", outra:"Outra", desconhecida:"Não informada"};
  populateSelect(els.spatial, sortedEntries(countBy(all.map(spatialBucket)), value => spatialLabels[value] || value), "Qualquer resolução espacial");
  const accessLabels = {arquivo:"Download de arquivo",api:"API / acesso programático",ogc:"WMS/WFS/OGC",gee:"Google Earth Engine",banco:"Banco / consulta estruturada",web:"Consulta web / portal",outro:"Outro"};
  populateSelect(els.access, sortedEntries(countBy(all.flatMap(productAccessCategories)), value => accessLabels[value] || value), "Qualquer forma de acesso");
  const formatLabels = {geotiff:"GeoTIFF/TIFF",csv:"CSV",shapefile:"Shapefile",geojson:"GeoJSON",netcdf:"NetCDF",parquet:"Parquet",json:"JSON",kml:"KML/KMZ",excel:"Excel",raster:"Raster",vetor:"Vetor",outro:"Outro / não padronizado"};
  populateSelect(els.format, sortedEntries(countBy(all.flatMap(productFormatCategories)), value => formatLabels[value] || value), "Qualquer formato");
  populateSelect(els.free, sortedEntries(countBy(all.map(p => aggregateEnum((p.distributions || []).map(d => d.free_download)))), value => ENUM_LABELS[value] || value), "Qualquer condição de gratuidade");
  const licenseLabels = {aberta:"Licença aberta identificada",outros_termos:"Outros termos declarados",nao_informada:"Licença não informada"};
  populateSelect(els.license, sortedEntries(countBy(all.map(productLicenseCategory)), value => licenseLabels[value] || value), "Qualquer licença");

  populateSelect(els.area, sortedEntries(countBy(all.flatMap(p => split(p.research_areas))), labelArea), "Todas as áreas de pesquisa");
  populateSelect(els.source, sortedEntries(countBy(all.map(p => p.source?.resource_name))), "Todas as fontes");
  populateSelect(els.kind, sortedEntries(countBy(all.map(p => p.product_kind)), value => KIND_LABELS[value] || value), "Todos os tipos de produto");
  populateSelect(els.auth, sortedEntries(countBy(all.flatMap(p => (p.distributions || []).map(d => d.authentication_required))), value => ENUM_LABELS[value] || value), "Qualquer autenticação");
  populateSelect(els.status, sortedEntries(countBy(all.map(p => p.product_status))), "Todos os estados");
  populateSelect(els.origin, sortedEntries(countBy(all.map(p => p.primary_or_derived)), value => ORIGIN_LABELS[value] || value), "Qualquer origem");
  populateSelect(els.brazil, sortedEntries(countBy(all.map(p => p.covers_brazil)), value => ENUM_LABELS[value] || value), "Qualquer disponibilidade no Brasil");
}

function currentFilters() {
  return {
    parsed: parseQuery(els.q?.value || ""), theme: els.theme?.value || "", coverage: norm(els.coverage?.value || ""),
    yearStart: els.yearStart?.value || "", yearEnd: els.yearEnd?.value || "", temporal: els.temporal?.value || "",
    support: els.support?.value || "", spatial: els.spatial?.value || "", access: els.access?.value || "",
    format: els.format?.value || "", free: els.free?.value || "", license: els.license?.value || "",
    area: els.area?.value || "", source: els.source?.value || "", kind: els.kind?.value || "",
    auth: els.auth?.value || "", status: els.status?.value || "", origin: els.origin?.value || "", brazil: els.brazil?.value || ""
  };
}
function productMatches(product, f) {
  return interpretedQueryMatches(product, f.parsed) &&
    (!f.theme || themeMatches(product, f.theme)) &&
    (!f.coverage || norm(product.geographic_coverage).includes(f.coverage)) &&
    coversRequestedPeriod(product, f.yearStart, f.yearEnd) &&
    (!f.temporal || temporalBucket(product) === f.temporal) &&
    (!f.support || supportBucket(product) === f.support) &&
    (!f.spatial || spatialBucket(product) === f.spatial) &&
    (!f.access || productAccessCategories(product).includes(f.access)) &&
    (!f.format || productFormatCategories(product).includes(f.format)) &&
    (!f.free || aggregateEnum((product.distributions || []).map(d => d.free_download)) === f.free) &&
    (!f.license || productLicenseCategory(product) === f.license) &&
    (!f.area || split(product.research_areas).includes(f.area)) &&
    (!f.source || product.source?.resource_name === f.source) &&
    (!f.kind || product.product_kind === f.kind) &&
    (!f.auth || (product.distributions || []).some(d => d.authentication_required === f.auth)) &&
    (!f.status || product.product_status === f.status) &&
    (!f.origin || product.primary_or_derived === f.origin) &&
    (!f.brazil || product.covers_brazil === f.brazil);
}
function compareRank(a,b,parsed) {
  const q = relevanceScore(b,parsed) - relevanceScore(a,parsed);
  if (q) return q;
  const br = brazilPriority(b) - brazilPriority(a);
  if (br) return br;
  const docs = documentationScore(b) - documentationScore(a);
  if (docs) return docs;
  const origin = sourceOriginScore(b) - sourceOriginScore(a);
  if (origin) return origin;
  return String(a.product_name).localeCompare(String(b.product_name), "pt-BR");
}
function sortResults(parsed) {
  if (els.sort?.value === "name") filtered.sort((a,b) => a.product_name.localeCompare(b.product_name,"pt-BR"));
  else if (els.sort?.value === "source") filtered.sort((a,b) => (a.source?.resource_name || "").localeCompare(b.source?.resource_name || "","pt-BR") || a.product_name.localeCompare(b.product_name,"pt-BR"));
  else if (els.sort?.value === "verified") filtered.sort((a,b) => String(b.last_verified || "").localeCompare(String(a.last_verified || "")) || compareRank(a,b,parsed));
  else filtered.sort((a,b) => compareRank(a,b,parsed));
}

function renderInterpreted(parsed) {
  if (!els.interpreted) return;
  els.interpreted.hidden = !parsed.labels.length;
  els.interpreted.innerHTML = parsed.labels.length ? `<strong>Busca interpretada:</strong> ${parsed.labels.map(label => `<span>${esc(label)}</span>`).join("")}` : "";
}
function topCount(values) {
  const counts = countBy(values);
  return [...counts.entries()].sort((a,b) => b[1]-a[1])[0] || null;
}
function renderInsights() {
  if (!els.insights) return;
  if (!filtered.length) { els.insights.hidden = true; els.insights.innerHTML = ""; return; }
  const items = [];
  const br = filtered.filter(p => p.covers_brazil === "sim").length;
  if (br) items.push({label:`${br} com dados para o Brasil`, type:"brazil", value:"sim"});
  const temporal = topCount(filtered.map(temporalBucket).filter(v => !["desconhecida","outra"].includes(v)));
  const temporalLabels = {subdiaria:"subdiários",diaria:"diários",semanal:"semanais",mensal:"mensais",trimestral:"trimestrais",sazonal:"sazonais",anual:"anuais",continua:"contínuos"};
  if (temporal) items.push({label:`${temporal[1]} ${temporalLabels[temporal[0]] || temporal[0]}`, type:"temporal", value:temporal[0]});
  const format = topCount(filtered.flatMap(productFormatCategories).filter(v => v !== "outro"));
  const formatLabels = {geotiff:"GeoTIFF/TIFF",csv:"CSV",shapefile:"Shapefile",geojson:"GeoJSON",netcdf:"NetCDF",parquet:"Parquet",json:"JSON",kml:"KML/KMZ",excel:"Excel",raster:"raster",vetor:"vetor"};
  if (format) items.push({label:`${format[1]} em ${formatLabels[format[0]] || format[0]}`, type:"format", value:format[0]});
  const access = topCount(filtered.flatMap(productAccessCategories).filter(v => v !== "outro"));
  const accessLabels = {arquivo:"download",api:"API",ogc:"WMS/WFS/OGC",gee:"Earth Engine",banco:"banco/consulta",web:"consulta web"};
  if (access) items.push({label:`${access[1]} com ${accessLabels[access[0]] || access[0]}`, type:"access", value:access[0]});
  els.insights.hidden = !items.length;
  els.insights.innerHTML = items.length ? `<span>Perfil do resultado:</span>${items.map(item => `<button type="button" data-insight-type="${item.type}" data-insight-value="${item.value}">${esc(item.label)}</button>`).join("")}` : "";
  els.insights.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    const target = {brazil:els.brazil, temporal:els.temporal, format:els.format, access:els.access}[button.dataset.insightType];
    if (target) { target.value = button.dataset.insightValue; filter(); target.focus(); }
  }));
}

function filter(syncUrl = true) {
  const f = currentFilters();
  filtered = all.filter(product => productMatches(product,f));
  sortResults(f.parsed);
  visibleCount = PAGE_SIZE;
  render();
  renderInterpreted(f.parsed);
  renderActiveFilters(f);
  renderInsights();
  if (syncUrl) writeUrl();
}
function render() {
  const shown = filtered.slice(0,visibleCount);
  els.list.innerHTML = shown.map(productCard).join("");
  els.empty.hidden = filtered.length > 0;
  els.count.textContent = `${filtered.length} ${filtered.length === 1 ? "produto compatível" : "produtos compatíveis"} · ${all.length} no catálogo`;
  const hasMore = shown.length < filtered.length;
  els.resultsMore.hidden = !hasMore;
  els.shownCount.textContent = hasMore ? `${shown.length} de ${filtered.length} exibidos` : `${shown.length} exibidos`;
  els.list.querySelectorAll("[data-compare]").forEach(input => input.addEventListener("change", handleCompareChange));
}

function activeItem(key,label,value,element) { return value ? {key,label:`${label}: ${element?.selectedOptions?.[0]?.textContent?.replace(/\s+\(\d+\)$/,'') || value}`} : null; }
function renderActiveFilters(f) {
  const items = [];
  if (f.parsed.raw) items.push({key:"q",label:`Busca: ${els.q.value.trim()}`});
  [
    activeItem("theme","Tema",f.theme,els.theme),
    f.coverage ? {key:"coverage",label:`Geografia: ${els.coverage.value.trim()}`} : null,
    f.yearStart ? {key:"yearStart",label:`De: ${f.yearStart}`} : null,
    f.yearEnd ? {key:"yearEnd",label:`Até: ${f.yearEnd}`} : null,
    activeItem("temporal","Tempo",f.temporal,els.temporal), activeItem("support","Suporte",f.support,els.support),
    activeItem("spatial","Resolução",f.spatial,els.spatial), activeItem("access","Acesso",f.access,els.access),
    activeItem("format","Formato",f.format,els.format), activeItem("free","Gratuidade",f.free,els.free), activeItem("license","Licença",f.license,els.license),
    activeItem("area","Área",f.area,els.area), activeItem("source","Fonte",f.source,els.source), activeItem("kind","Tipo",f.kind,els.kind),
    activeItem("auth","Autenticação",f.auth,els.auth), activeItem("status","Estado",f.status,els.status), activeItem("origin","Origem",f.origin,els.origin), activeItem("brazil","Brasil",f.brazil,els.brazil)
  ].filter(Boolean).forEach(item => items.push(item));
  const advancedKeys = ["area","source","kind","auth","status","origin","brazil"];
  const advancedActive = items.filter(item => advancedKeys.includes(item.key)).length;
  els.advancedCount.textContent = advancedActive ? `(${advancedActive} ${advancedActive === 1 ? "ativo" : "ativos"})` : "";
  if (advancedActive) els.advancedFilters.open = true;
  els.activeFilters.hidden = !items.length;
  els.activeFilters.innerHTML = items.length ? `<span>Filtros ativos:</span>${items.map(item => `<button type="button" data-remove="${item.key}">${esc(item.label)} <b aria-hidden="true">×</b></button>`).join("")}` : "";
  els.activeFilters.querySelectorAll("[data-remove]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.remove;
    const target = {q:els.q, theme:els.theme, coverage:els.coverage, yearStart:els.yearStart, yearEnd:els.yearEnd, temporal:els.temporal, support:els.support, spatial:els.spatial, access:els.access, format:els.format, free:els.free, license:els.license, area:els.area, source:els.source, kind:els.kind, auth:els.auth, status:els.status, origin:els.origin, brazil:els.brazil}[key];
    if (target) { target.value = ""; filter(); target.focus(); }
  }));
}

function writeUrl() {
  const values = {q:els.q.value.trim(),theme:els.theme.value,coverage:els.coverage.value.trim(),from:els.yearStart.value,to:els.yearEnd.value,temporal:els.temporal.value,support:els.support.value,spatial:els.spatial.value,access:els.access.value,format:els.format.value,free:els.free.value,license:els.license.value,area:els.area.value,source:els.source.value,kind:els.kind.value,auth:els.auth.value,status:els.status.value,origin:els.origin.value,brazil:els.brazil.value,sort:els.sort.value === "relevance" ? "" : els.sort.value};
  const params = new URLSearchParams();
  Object.entries(values).forEach(([key,value]) => { if (value) params.set(key,value); });
  history.replaceState(null,"",`${location.pathname}${params.toString() ? `?${params}` : ""}${location.hash}`);
}
function setFromParam(element,value) { if (!element || !value) return; if (element.tagName === "SELECT" && ![...element.options].some(o => o.value === value)) return; element.value = value; }
function readUrl() {
  const p = new URLSearchParams(location.search);
  setFromParam(els.q,p.get("q")); setFromParam(els.theme,p.get("theme")); setFromParam(els.coverage,p.get("coverage"));
  setFromParam(els.yearStart,p.get("from")); setFromParam(els.yearEnd,p.get("to")); setFromParam(els.temporal,p.get("temporal"));
  setFromParam(els.support,p.get("support")); setFromParam(els.spatial,p.get("spatial")); setFromParam(els.access,p.get("access"));
  setFromParam(els.format,p.get("format")); setFromParam(els.free,p.get("free")); setFromParam(els.license,p.get("license"));
  setFromParam(els.area,p.get("area")); setFromParam(els.source,p.get("source")); setFromParam(els.kind,p.get("kind"));
  setFromParam(els.auth,p.get("auth")); setFromParam(els.status,p.get("status")); setFromParam(els.origin,p.get("origin")); setFromParam(els.brazil,p.get("brazil")); setFromParam(els.sort,p.get("sort"));
}

function goToCatalog() {
  els.catalogHeading.scrollIntoView({behavior:reducedMotion()?"auto":"smooth",block:"start"});
  els.catalogHeading.focus({preventScroll:true});
}
function handleCompareChange(event) {
  const id = event.target.dataset.compare;
  if (event.target.checked && selected.size >= MAX_COMPARE) {
    event.target.checked = false;
    els.compareStatus.textContent = `Compare no máximo ${MAX_COMPARE} produtos por vez.`;
    return;
  }
  if (event.target.checked) selected.add(id); else selected.delete(id);
  renderCompareBar();
}
function syncCompareCheckboxes() {
  document.querySelectorAll("[data-compare]").forEach(input => { input.checked = selected.has(input.dataset.compare); });
}
function renderCompareBar() {
  const count = selected.size;
  els.compareBar.hidden = count === 0;
  els.compareCount.textContent = `${count} ${count === 1 ? "produto selecionado" : "produtos selecionados"}`;
  els.compareStatus.textContent = count < 2 ? "Selecione mais um produto para comparar." : "Comparação pronta.";
  const open = $("#compare-open"); if (open) open.disabled = count < 2;
}
function comparisonValue(product,key) {
  const values = {
    where:product.geographic_coverage, when:product.temporal_coverage, scale:displayScale(product), access:displayAccess(product),
    source:product.source?.resource_name, version:product.version_or_collection, license:licenses(product),
    limitations:product.limitations, methodology:product.methodology_url ? "Disponível" : "Não localizada", verified:product.last_verified
  };
  return values[key] || "Não informado";
}
function renderComparison() {
  const products = [...selected].map(id => all.find(product => product.product_id === id)).filter(Boolean);
  if (products.length < 2) return false;
  const rows = [["Onde?","where"],["Quando?","when"],["Escala","scale"],["Acesso","access"],["Fonte / provedor","source"],["Versão / coleção","version"],["Licença(s)","license"],["Metodologia","methodology"],["Limitações","limitations"],["Registro revisado em","verified"]];
  els.compareContent.innerHTML = `<div class="compare-table-wrap"><table class="compare-table"><thead><tr><th scope="col">Dimensão</th>${products.map(product => `<th scope="col"><div class="compare-product-head"><span>${esc(product.product_name)}</span><button type="button" data-remove-compare="${esc(product.product_id)}" aria-label="Remover ${esc(product.product_name)} da comparação">Remover</button></div></th>`).join("")}</tr></thead><tbody>${rows.map(([label,key]) => `<tr><th scope="row">${label}</th>${products.map(product => `<td>${esc(comparisonValue(product,key))}</td>`).join("")}</tr>`).join("")}</tbody></table></div><p class="export-note">A comparação organiza metadados catalogados para triagem. Confirme versão, método e condições de uso no provedor original.</p>`;
  els.compareContent.querySelectorAll("[data-remove-compare]").forEach(button => button.addEventListener("click", () => {
    selected.delete(button.dataset.removeCompare);
    syncCompareCheckboxes();
    renderCompareBar();
    if (selected.size < 2) { els.compareDialog.close(); return; }
    renderComparison();
  }));
  return true;
}
function openComparison() {
  if (!renderComparison()) { els.compareStatus.textContent = "Selecione pelo menos dois produtos."; return; }
  if (typeof els.compareDialog.showModal === "function") els.compareDialog.showModal(); else els.compareDialog.setAttribute("open","");
}
function resetComparison() {
  selected.clear(); syncCompareCheckboxes(); renderCompareBar();
  document.dispatchEvent(new CustomEvent("vitrine:comparison-reset"));
}
function closeComparison(reset=true) {
  if (els.compareDialog.open) els.compareDialog.close();
  if (reset) resetComparison();
}

function bind() {
  const controls = [els.q,els.theme,els.coverage,els.yearStart,els.yearEnd,els.temporal,els.support,els.spatial,els.access,els.format,els.free,els.license,els.area,els.source,els.kind,els.auth,els.status,els.origin,els.brazil,els.sort].filter(Boolean);
  controls.forEach(element => element.addEventListener(element === els.q || element === els.coverage || element === els.yearStart || element === els.yearEnd ? "input" : "change", () => filter()));
  els.searchForm.addEventListener("submit", event => { event.preventDefault(); filter(); goToCatalog(); });
  els.showMore.addEventListener("click", () => { visibleCount = Math.min(filtered.length,visibleCount + PAGE_SIZE); render(); });
  $("#product-clear").addEventListener("click", () => {
    $("#product-filters").reset(); els.q.value=""; els.sort.value="relevance"; els.advancedFilters.open=false; filter(); els.q.focus();
  });
  $("#compare-open").addEventListener("click", openComparison);
  $("#compare-clear").addEventListener("click", resetComparison);
  $("#compare-close").addEventListener("click", () => closeComparison(true));
  els.compareDialog.addEventListener("click", event => { if (event.target === els.compareDialog) closeComparison(true); });
  els.compareDialog.addEventListener("close", () => { if (selected.size) resetComparison(); });
  window.addEventListener("popstate", () => { readUrl(); filter(false); });
}

async function init() {
  try {
    const response = await fetch("data/data_products.json");
    if (!response.ok) throw new Error("Não foi possível carregar o catálogo de produtos.");
    all = await response.json();
    all.forEach(product => {
      product._search = productSearchBase(product);
      product._temporalRange = temporalRange(product);
    });
    populateFilters();
    readUrl();
    bind();
    $("#p-total").textContent = all.length;
    $("#p-sources").textContent = new Set(all.map(product => product.resource_id)).size;
    $("#p-free").textContent = all.filter(product => (product.distributions || []).some(item => item.free_download === "sim")).length;
    $("#p-formats").textContent = new Set(all.flatMap(productFormatsRaw)).size;
    filter(false);
  } catch (error) {
    els.count.textContent = "Falha ao carregar produtos";
    els.list.innerHTML = `<div class="empty"><h3>Falha ao carregar os produtos</h3><p>${esc(error.message)}</p></div>`;
    els.resultsMore.hidden = true;
  }
}

init();