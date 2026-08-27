(() => {
  "use strict";
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

  window.addEventListener("resize", () => {
    if (window.innerWidth > 820) close();
  });
})();
