(() => {
  "use strict";
  const dialog = document.querySelector("#compare-dialog");
  const header = dialog?.querySelector(".compare-dialog-header");
  const content = document.querySelector("#compare-content");
  const close = document.querySelector("#compare-close");
  if (!dialog || !header || !content || !close) return;

  const csvCell = value => `"${String(value ?? "").replace(/"/g, '""')}"`;
  const downloadCsv = () => {
    const table = content.querySelector("table.compare-table");
    if (!table) return;
    const rows = [...table.querySelectorAll("tr")].map(row =>
      [...row.querySelectorAll("th,td")].map(cell => csvCell(cell.textContent.trim())).join(",")
    );
    const blob = new Blob(["\uFEFF" + rows.join("\r\n")], {type:"text/csv;charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const productColumns = Math.max(0, (table.querySelectorAll("thead th").length || 1) - 1);
    link.href = url;
    link.download = `vitrine-ciencia_comparacao_${productColumns}-produtos.csv`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  const actions = document.createElement("div");
  actions.className = "compare-dialog-actions";
  const download = document.createElement("button");
  download.type = "button";
  download.id = "compare-download-csv";
  download.className = "download-comparison";
  download.textContent = "Baixar tabela (CSV)";
  download.addEventListener("click", downloadCsv);
  actions.append(download, close);
  header.appendChild(actions);

  const syncDownload = () => {
    const table = content.querySelector("table.compare-table");
    download.disabled = !table;
  };
  new MutationObserver(syncDownload).observe(content, {childList:true, subtree:true});
  dialog.addEventListener("close", () => { download.disabled = true; });
  syncDownload();
})();
