(() => {
  "use strict";

  const ensureStylesheet = (href) => {
    if ([...document.styleSheets].some(sheet => String(sheet.href || "").includes(href))) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  };
  ensureStylesheet("assets/ux-v3.css?v=20260827-1");

  if (document.querySelector("#product-catalog") && !document.querySelector('script[src*="product-ui-fixes.js"]')) {
    const script = document.createElement("script");
    script.src = "assets/product-ui-fixes.js?v=20260827-1";
    script.defer = true;
    document.body.appendChild(script);
  }

  const button = document.querySelector(".nav-toggle");
  const links = document.querySelector("#site-nav-links");
  if (!button || !links) return;

  const close = () => {
    button.setAttribute("aria-expanded", "false");
    links.classList.remove("is-open");
  };

  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    links.classList.toggle("is-open", !open);
  });

  links.addEventListener("click", event => {
    if (event.target.closest("a")) close();
  });

  document.addEventListener("keydown", event => {
    if (event.key === "Escape") close();
  });

  document.addEventListener("click", event => {
    if (window.innerWidth <= 820 && links.classList.contains("is-open") && !event.target.closest(".site-nav")) close();
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 820) close();
  });
})();