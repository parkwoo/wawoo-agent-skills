/* 文档目次：展开含当前锚点的章；拦截 summary 内链的冒泡 */
(function () {
  const toc = document.querySelector(".kit-doc-toc");
  if (!toc) return;

  const branches = toc.querySelectorAll(".kit-toc-branch");
  const active = toc.querySelector(".md-nav__link--active, a[aria-current='true']");

  branches.forEach((details) => {
    if (active && details.contains(active)) {
      details.open = true;
    }
    const link = details.querySelector(".kit-toc-branch__label");
    if (link) {
      link.addEventListener("click", (e) => e.stopPropagation());
    }
  });

  if (![...branches].some((d) => d.open) && branches[0]) {
    branches[0].open = true;
  }
})();