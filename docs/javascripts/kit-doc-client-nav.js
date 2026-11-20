/* 使用说明 §2：客户端快捷跳转（高亮当前锚点） */
(function () {
  const nav = document.querySelector(".kit-client-nav");
  if (!nav) return;

  const links = [...nav.querySelectorAll("a[href^='#']")];
  const setActive = (id) => {
    links.forEach((a) => {
      const on = a.getAttribute("href") === `#${id}`;
      a.classList.toggle("is-active", on);
      if (on) a.setAttribute("aria-current", "location");
      else a.removeAttribute("aria-current");
    });
  };

  const fromHash = () => {
    const id = (location.hash || "").replace(/^#/, "");
    if (id && links.some((a) => a.getAttribute("href") === `#${id}`)) setActive(id);
    else if (links[0]) setActive(links[0].getAttribute("href").slice(1));
  };

  links.forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href")?.slice(1);
      if (!id) return;
      const el = document.getElementById(id);
      if (el) {
        e.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        history.replaceState(null, "", `#${id}`);
        setActive(id);
      }
    });
  });

  fromHash();
  window.addEventListener("hashchange", fromHash);
})();