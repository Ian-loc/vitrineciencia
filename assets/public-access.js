(() => {
  "use strict";
  const https = value => /^https:\/\//i.test(String(value || ""));
  window.VitrinePublicAccess = item => {
    const url = https(item.access_url) ? item.access_url : (https(item.documentation_url) ? item.documentation_url : "");
    if (!url) return null;
    const primary = ["A", "B"].includes(item.access_role) && url === item.access_url;
    return {url, primary, label: primary ? "Acessar dados" : "Acessar site"};
  };
  window.VitrineIsDataDownload = (distribution, roles) =>
    https(distribution.access_url) && roles[distribution.distribution_name]?.access_class === "A";

  const sourceRoles = {A: "direct_data", B: "data_page", C: "data_service", D: "viewer"};
  const supports = (route, mode) =>
    route.status === "active" && https(route.url) && route.roles.includes(sourceRoles[mode]);

  function index(routes) {
    const sources = new Map();
    for (const route of routes) {
      if (route.target_type !== "resource") continue;
      if (!sources.has(route.record_id)) sources.set(route.record_id, []);
      sources.get(route.record_id).push(route);
    }
    return sources;
  }

  function modes(routes) {
    const available = Object.keys(sourceRoles).filter(mode => routes.some(route => supports(route, mode)));
    return available.length || !routes.some(route => route.primary && route.access_assessment === "E")
      ? available : ["E"];
  }

  function destination(routes, mode) {
    const matches = routes.filter(route => supports(route, mode));
    // A dedicated data page is more useful than a general portal.
    if (mode === "B") return matches.find(route => !route.roles.includes("official_site")) || matches[0];
    return matches.find(route => route.primary) || matches[0];
  }

  window.VitrineSourceAccess = {index, modes, destination};
})();
