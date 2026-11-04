(() => {
  "use strict";
  const https = value => /^https:\/\//i.test(String(value || ""));
  window.VitrinePublicAccess = item => {
    const url = https(item.access_url) ? item.access_url : (https(item.documentation_url) ? item.documentation_url : "");
    if (!url) return null;
    const primary = ["A", "B"].includes(item.access_role) && url === item.access_url;
    return {url, primary, label: primary ? "Acessar dados / download" : "Acessar site"};
  };
})();
