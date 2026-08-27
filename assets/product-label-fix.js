(() => {
  "use strict";
  const labels = {
    map_layer_collection: "Coleção de camadas cartográficas",
    indicator_family: "Família de indicadores",
    software_output: "Saída de software"
  };

  function apply() {
    const select = document.querySelector("#product-kind");
    if (!select) return;
    [...select.options].forEach(option => {
      if (!labels[option.value]) return;
      const count = option.textContent.match(/\s+\(\d+\)$/)?.[0] || "";
      option.textContent = `${labels[option.value]}${count}`;
    });
  }

  function start() {
    const select = document.querySelector("#product-kind");
    if (!select) return;
    apply();
    new MutationObserver(apply).observe(select, {childList:true, subtree:true});
    window.setTimeout(apply, 0);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once:true});
  else start();
})();
