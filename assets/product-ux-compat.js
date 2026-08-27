/* Compatibility bridge: product comparison UX + selective CSV export. */
(() => {
  "use strict";
  const compareButton = document.querySelector("#compare-open");
  const dialog = document.querySelector("#compare-dialog");
  const content = document.querySelector("#compare-content");
  if (!compareButton || !dialog || !content) return;

  // export-selective.js refreshes the table on the next task. Re-apply the
  // canonical interactive comparison after that enrichment so removal controls
  // remain available while the CSV button in the dialog header is preserved.
  compareButton.addEventListener("click", () => {
    setTimeout(() => {
      if (dialog.open && typeof uxRenderComparison === "function") uxRenderComparison();
    }, 30);
  });

  // Keep the export module's independent selection set synchronized when a
  // product is removed programmatically from inside the comparison.
  content.addEventListener("click", event => {
    const button = event.target.closest("[data-remove-compare]");
    if (!button) return;
    const id = button.dataset.removeCompare;
    setTimeout(() => {
      document.querySelectorAll(`[data-compare="${CSS.escape(id)}"]`).forEach(input => {
        input.dispatchEvent(new Event("change", {bubbles:true}));
      });
    }, 0);
  });

  // Closing the dialog is a hard reset by design. Dispatch change events after
  // the product UX clears checkboxes so every module observes the same state.
  dialog.addEventListener("close", () => {
    document.querySelectorAll("[data-compare]").forEach(input => {
      input.checked = false;
      input.dispatchEvent(new Event("change", {bubbles:true}));
    });
  });
})();
