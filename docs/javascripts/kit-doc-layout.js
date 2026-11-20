/* 文档布局：顶栏高度 → CSS 变量；取消 Material 侧栏错位 transform */
(function () {
  if (!document.body.classList.contains("kit-docs")) return;

  const root = document.documentElement;

  function syncTopbarOffset() {
    const bar = document.querySelector(".kit-topbar");
    const h = bar ? Math.ceil(bar.getBoundingClientRect().height) : 80;
    root.style.setProperty("--kit-docs-topbar-offset", `${h}px`);
  }

  function resetSidebarGeometry() {
    document.querySelectorAll(".kit-sidebar-toc").forEach((el) => {
      el.style.transform = "none";
      el.style.height = "auto";
      el.style.top = "auto";
      el.style.left = "auto";
    });
  }

  syncTopbarOffset();
  resetSidebarGeometry();
  window.addEventListener("resize", syncTopbarOffset, { passive: true });

  /* Material 在 resize/scroll 时可能重写 sidebar 样式 */
  const obs = new MutationObserver(() => resetSidebarGeometry());
  const sidebar = document.querySelector(".kit-sidebar-toc");
  if (sidebar) {
    obs.observe(sidebar, { attributes: true, attributeFilter: ["style", "class"] });
  }

  /* Skill 收录：速查句一键复制 */
  const catalogRoot = document.querySelector(".kit-catalog-root");
  if (catalogRoot) {
    catalogRoot.querySelectorAll("[data-kit-copy-cmd]").forEach((el) => {
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.setAttribute("title", "点击复制");
      const copy = () => {
        const text = el.getAttribute("data-kit-copy-cmd") || el.textContent || "";
        navigator.clipboard.writeText(text).then(
          () => {
            el.classList.add("is-copied");
            window.setTimeout(() => el.classList.remove("is-copied"), 1200);
          },
          () => {}
        );
      };
      el.addEventListener("click", copy);
      el.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          copy();
        }
      });
    });
  }
})();