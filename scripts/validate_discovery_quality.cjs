// Regressões de descoberta: contagens, links de acesso e filtros compatíveis.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const json = name => JSON.parse(read(name));
const context = vm.createContext({window:{}});
vm.runInContext(read('assets/public-access.js'), context);
const access = context.window.VitrinePublicAccess;
const items = json('data/applied_priority_gate.json').items;
for (const item of items) {
  assert.equal(access(item).url, item.access_url);
  assert.equal(access(item).label, ['A','B'].includes(item.access_role) ? 'Acessar dados / download' : 'Acessar site');
}
assert.equal(access({access_role:'B',access_url:'javascript:alert(1)'}), null);
assert.equal(access({access_role:'B',documentation_url:'https://example.org/'}).label, 'Acessar site');
vm.runInContext(read('assets/source-discovery-v2.js').replace(/\n  initialize\(\);\n/, '\n'), context);
const facets = context.window.VitrineSourceFacets;
const resources = json('data/data_resources.json');
const byId = id => resources.find(r => r.resource_id === id);
assert(facets.coverageMatches(byId('DR0002'), 'mg'));
assert(!facets.coverageMatches(byId('DR0002'), 'global'));
assert(facets.coverageMatches(byId('DR0002'), byId('DR0002').geographic_coverage));
assert(facets.informationMatches({data_product_types:'mapas | mapas raster | camadas geoespaciais'}, 'mapas'));
assert.equal(facets.informationCategories({data_product_types:'mapas | mapas raster | camadas geoespaciais'}).length, 1);
assert(facets.informationMatches({data_product_types:'camadas geoespaciais'}, 'camadas geoespaciais'));
for (const resource of resources) {
  assert(facets.coverageCategory(resource));
  assert(facets.informationCategories(resource).length > 0);
}
const home = read('_site/index.html');
const counts = {'home-sources':resources.length,'home-all-sources':resources.length,'home-products':json('data/data_products.json').length};
const ids = new Set(resources.map(r => r.resource_id));
counts['home-access'] = new Set(json('data/access_routes.json').routes.filter(r => r.primary && r.target_type === 'resource' && ids.has(r.record_id) && ['A','B'].includes(r.access_assessment)).map(r => r.record_id)).size;
for (const [id,value] of Object.entries(counts)) assert(home.includes(`id="${id}">${value}<`), `Contador ${id}`);
assert.equal(counts['home-access'], 41);
const labels = {'sources.html':'Explorar dados','products.html':'Dados detalhados','about.html':'Sobre a Vitrine','analytics.html':'Sobre o acervo'};
for (const filename of ['index.html','sources.html','products.html','products-list.html','analytics.html','analytics-products.html','about.html']) {
  const nav = read(filename).match(/id="site-nav-links">([\s\S]*?)<\/nav>/)[1];
  for (const [href,label] of Object.entries(labels)) assert(new RegExp(`href="${href}"[^>]*>${label}</a>`).test(nav), `${filename}: ${label}`);
}
console.log(`OK: contagens ${resources.length}/11/41, destinos de acesso, vocabulário agrupado e navegação consistentes`);
