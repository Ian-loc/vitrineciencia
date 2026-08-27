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
      const baseLabel = labels[option.value];
      if (!baseLabel) return;
      const count = option.textContent.match(/\s+\(\d+\)$/)?.[0] || "";
      const visibleLabel = `${baseLabel}${count}`;
      if (option.label !== visibleLabel) option.label = visibleLabel;
    });
  }

  function start() {
    const select = document.querySelector("#product-kind");
    if (!select) return;
    apply();
    new MutationObserver(apply).observe(select, {childList:true});
    window.setTimeout(apply, 0);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once:true});
  else start();
})();
