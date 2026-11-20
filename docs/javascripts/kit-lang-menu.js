/* 文档 URL 契约: cn /cn/docs/{slug}/ · en /en/docs/ · ja /ja/docs/ · ko /ko/docs/ */
(function () {
  const LABELS = { zh: "简体中文", en: "English", ja: "日本語", ko: "한국어" };
  const URL_LOCALE = { zh: "cn", en: "en", ja: "ja", ko: "ko" };
  const DEFAULT_DOC = "usage";

  function parseDocsPath(pathname) {
    const clean = (pathname || "").split("#")[0].split("?")[0];
    let m = clean.match(/^\/(cn|en|ja|ko)\/docs\/([^/]+)\/?$/);
    if (m) {
      const loc = m[1] === "cn" ? "zh" : m[1];
      return { locale: loc, slug: m[2].toLowerCase() };
    }
    m = clean.match(/^\/docs\/(en|ja|ko)\/([^/]+)\/?$/);
    if (m) {
      return { locale: m[1], slug: m[2].toLowerCase(), legacy: true };
    }
    m = clean.match(/^\/docs\/([^/]+)\/?$/);
    if (m) {
      const slug = m[1].toLowerCase();
      if (slug === "en" || slug === "ja" || slug === "ko" || slug === "zh" || slug === "cn") return null;
      if (slug === "assets" || slug === "stylesheets" || slug === "javascripts" || slug === "search") {
        return null;
      }
      return { locale: "zh", slug, legacy: true };
    }
    return null;
  }

  function urlForLocale(locale, slug) {
    const hash = window.location.hash || "";
    const seg = URL_LOCALE[locale] || locale;
    return `/${seg}/docs/${slug}/` + hash;
  }

  const doc = parseDocsPath(window.location.pathname);
  let current = doc ? doc.locale : "zh";
  if (!doc) {
    const p = window.location.pathname || "";
    if (p.includes("/en/docs/") || p.includes("/docs/en/")) current = "en";
    else if (p.includes("/ja/docs/") || p.includes("/docs/ja/")) current = "ja";
    else if (p.includes("/ko/docs/") || p.includes("/docs/ko/")) current = "ko";
    else if (p.includes("/cn/docs/")) current = "zh";
  }

  if (doc?.legacy) {
    window.location.replace(urlForLocale(doc.locale, doc.slug));
    return;
  }

  document.querySelectorAll("[data-kit-lang]").forEach((root) => {
    root.setAttribute("data-current", current);
    const cur = root.querySelector(".kit-lang-current");
    if (cur && LABELS[current]) cur.textContent = LABELS[current];

    const slug = doc?.slug || DEFAULT_DOC;

    root.querySelectorAll("[data-kit-lang-switch]").forEach((a) => {
      const loc = a.getAttribute("data-kit-lang-switch");
      if (!loc) return;
      a.setAttribute("href", urlForLocale(loc, slug));
      a.setAttribute("aria-selected", loc === current ? "true" : "false");
    });

    const btn = root.querySelector(".kit-lang-trigger");
    const menu = root.querySelector(".kit-lang-menu");
    if (!btn || !menu) return;

    const close = () => {
      root.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      menu.hidden = true;
    };

    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = root.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      menu.hidden = !open;
    });

    menu.querySelectorAll("a[href]").forEach((a) => {
      a.addEventListener("click", (e) => {
        if (a.getAttribute("aria-disabled") === "true") {
          e.preventDefault();
          return;
        }
        const href = a.getAttribute("href");
        if (href && href !== "#") window.location.assign(href);
      });
    });

    document.addEventListener("click", (e) => {
      if (!root.contains(e.target)) close();
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  });
})();