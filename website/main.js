/** 首页可变数字 SSOT：/content/site-metrics.json */
function fillMetricTemplate(template, counts) {
  if (!template || !counts) return template;
  return template.replace(/\{(\w+)\}/g, (_, key) =>
    counts[key] != null ? String(counts[key]) : `{${key}}`
  );
}

async function loadSiteMetrics() {
  try {
    const res = await fetch("/content/site-metrics.json", { cache: "no-cache" });
    if (!res.ok) return;
    const data = await res.json();
    const counts = data.counts || {};
    const labels = data.labels_zh || {};
  const ver = data.release_version;

    document.querySelectorAll("[data-kit-stat]").forEach((el) => {
      const key = el.getAttribute("data-kit-stat");
      const strong = el.querySelector("strong");
      const span = el.querySelector("span");
      if (strong && counts[key] != null) strong.textContent = String(counts[key]);
      if (span && labels[key]) span.textContent = labels[key];
    });
    /* Hero 信任条文案由 home-copy.zh.json 的 hero_trust 注入 */
    document.querySelectorAll("[data-kit-stat-inline]").forEach((el) => {
      const key = el.getAttribute("data-kit-stat-inline");
      if (key && counts[key] != null && labels[key]) {
        el.textContent = `${counts[key]} ${labels[key]}`;
      }
    });
    document.querySelectorAll("[data-kit-version]").forEach((el) => {
      if (ver) el.textContent = `v${ver}`;
    });

    const meta = document.querySelector('meta[name="description"][data-kit-meta]');
    if (meta && data.meta_description_zh) {
      meta.setAttribute("content", fillMetricTemplate(data.meta_description_zh, counts));
    }

    const snippets = data.copy_zh || {};
    document.querySelectorAll("[data-kit-copy]").forEach((el) => {
      const key = el.getAttribute("data-kit-copy");
      const tpl = snippets[key];
      if (tpl) el.textContent = fillMetricTemplate(tpl, counts);
    });
  } catch {
    /* 使用 HTML 内默认数字 */
  }
}

function setByPath(obj, path) {
  return path.split(".").reduce((o, k) => (o && o[k] != null ? o[k] : null), obj);
}

async function loadHomeCopy() {
  if (document.body.getAttribute("data-kit-nav") !== "home") return;
  let counts = {};
  try {
    const m = await fetch("/content/site-metrics.json", { cache: "no-cache" });
    if (m.ok) counts = ((await m.json()).counts) || {};
  } catch {
    /* 无指标则用 HTML 默认 */
  }

  const fill = (tpl) => fillMetricTemplate(tpl, counts);

  try {
    const res = await fetch("/content/home-copy.zh.json", { cache: "no-cache" });
    if (!res.ok) return;
    const data = await res.json();

    document.querySelectorAll("[data-kit-copy-text]").forEach((el) => {
      const path = el.getAttribute("data-kit-copy-text");
      const text = setByPath(data, path);
      if (typeof text === "string" && text) {
        el.textContent = fill(text);
      } else if (text === "") {
        el.remove();
      }
    });

    const heroLead = setByPath(data, "hero.lead_primary");
    document.querySelectorAll("[data-kit-copy-text='hero.lead_primary']").forEach((el) => {
      if (heroLead) el.textContent = fill(heroLead);
    });

    const ctaP = setByPath(data, "hero.cta_primary");
    const ctaS = setByPath(data, "hero.cta_secondary");
    document.querySelectorAll("[data-kit-cta='primary']").forEach((el) => {
      if (ctaP) el.textContent = fill(ctaP);
    });
    document.querySelectorAll("[data-kit-cta='secondary']").forEach((el) => {
      if (ctaS) el.textContent = fill(ctaS);
    });

    const trust = data.hero_trust || {};
    const trustMap = {
      mit: trust.mit,
      skills: trust.skills,
      workflows: trust.workflows,
      token: trust.token,
    };
    Object.entries(trustMap).forEach(([key, tpl]) => {
      if (!tpl) return;
      document.querySelectorAll(`[data-kit-trust='${key}']`).forEach((el) => {
        const icon = el.querySelector("svg");
        el.textContent = "";
        if (icon) el.appendChild(icon);
        el.appendChild(document.createTextNode(` ${fill(tpl)}`));
      });
    });

    const statsSubline = data.stats_subline;
    document.querySelectorAll("[data-kit-copy-text='stats_subline']").forEach((el) => {
      if (!statsSubline) el.remove();
      else el.textContent = fill(statsSubline);
    });

    const compare = data.compare;
    if (compare) {
      document.querySelectorAll("[data-kit-compare='before']").forEach((el) => {
        if (compare.col_before) el.textContent = compare.col_before;
      });
      document.querySelectorAll("[data-kit-compare='after']").forEach((el) => {
        if (compare.col_after) el.textContent = compare.col_after;
      });
      if (Array.isArray(compare.rows)) {
        document.querySelectorAll("#why .compare-table tbody tr").forEach((tr, i) => {
          const row = compare.rows[i];
          if (!row) return;
          const th = tr.querySelector("th");
          const bad = tr.querySelector(".cell-bad .cell-with-icon span:last-child");
          const good = tr.querySelector(".cell-good .cell-with-icon span:last-child");
          if (th) th.textContent = row.scene;
          if (bad) bad.textContent = row.before;
          if (good) good.textContent = row.after;
        });
      }
    }

    const howCards = data.how_cards;
    if (Array.isArray(howCards)) {
      document.querySelectorAll("#how .grid-3 .card").forEach((article, i) => {
        const card = howCards[i];
        if (!card) {
          article.remove();
          return;
        }
        const h3 = article.querySelector("h3");
        const p = article.querySelector("p");
        if (h3 && card.title) h3.textContent = card.title;
        if (p && card.body) p.textContent = fill(card.body);
      });
    }

    const capCards = data.capability_cards;
    if (Array.isArray(capCards)) {
      document.querySelectorAll("#capabilities .feature-card-lg").forEach((article, i) => {
        const card = capCards[i];
        if (!card) {
          article.remove();
          return;
        }
        const h3 = article.querySelector("h3");
        const p = article.querySelector("p");
        if (h3 && card.title) h3.textContent = card.title;
        if (p && card.body) p.textContent = fill(card.body);
      });
    }

    const faqItems = data.faq_items;
    if (Array.isArray(faqItems)) {
      document.querySelectorAll(".faq details").forEach((details, i) => {
        const item = faqItems[i];
        if (!item) {
          details.remove();
          return;
        }
        const summary = details.querySelector("summary");
        const p = details.querySelector("p");
        if (summary) {
          const icon = summary.querySelector("svg");
          summary.textContent = "";
          if (icon) summary.appendChild(icon);
          summary.appendChild(document.createTextNode(` ${item.summary}`));
        }
        if (p && item.body) p.textContent = item.body;
      });
    }

    const demoMock = data.demo_mock_line;
    document.querySelectorAll("[data-kit-copy-text='demo_mock_line']").forEach((el) => {
      if (demoMock) el.textContent = demoMock;
    });
  } catch {
    /* HTML 默认文案 */
  }
}

async function loadChangelogCopy() {
  if (document.body.getAttribute("data-kit-page") !== "changelog") return;
  try {
    const res = await fetch("/content/changelog.zh.json", { cache: "no-cache" });
    if (!res.ok) return;
    const data = await res.json();
    document.querySelectorAll("[data-kit-copy-text]").forEach((el) => {
      const path = el.getAttribute("data-kit-copy-text");
      const text = setByPath(data, path);
      if (typeof text === "string" && text) {
        el.textContent = text;
      }
    });
    const title = setByPath(data, "page.title");
    if (title) document.title = title.includes("wawoo-skills") ? title : `${title} | wawoo-skills`;
    const ver = setByPath(data, "page.currentVersion");
    if (ver) {
      document.querySelectorAll("[data-kit-changelog-version]").forEach((el) => {
        el.textContent = ver;
      });
    }
  } catch {
    /* HTML 默认 */
  }
}

function initChangelogAnchorCopy() {
  if (document.body.getAttribute("data-kit-page") !== "changelog") return;
  document.querySelectorAll("[data-changelog-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-changelog-copy");
      if (!id) return;
      const url = `${window.location.origin}${window.location.pathname}#${id}`;
      try {
        await navigator.clipboard.writeText(url);
        const prev = btn.textContent;
        btn.textContent = "已复制链接";
        setTimeout(() => {
          btn.textContent = prev;
        }, 1500);
      } catch {
        /* clipboard unavailable */
      }
    });
  });
}

async function loadSkillsCatalogCopy() {
  const page = document.body.getAttribute("data-kit-page");
  if (page !== "skills-catalog" && page !== "guides") return;
  const hasCopySlots =
    document.querySelector("[data-kit-copy-text]") || document.getElementById("guides-catalog-body");
  if (!hasCopySlots) return;
  try {
    const res = await fetch("/content/skills-catalog.zh.json", { cache: "no-cache" });
    if (!res.ok) return;
    const data = await res.json();
    document.querySelectorAll("[data-kit-copy-text]").forEach((el) => {
      const path = el.getAttribute("data-kit-copy-text");
      const text = setByPath(data, path);
      if (typeof text !== "string" || !text) return;
      if (el.querySelector("a, strong, code, em")) return;
      el.textContent = text;
    });
    if (page === "skills-catalog") {
      const guidesBody = document.getElementById("guides-catalog-body");
      const title = setByPath(data, "page.title");
      if (title && guidesBody && !guidesBody.querySelector(".guides-capability-row")) {
        document.title =
          title.length > 30 ? title : `${title} — wawoo-skills 专家技能库`;
      }
    }
  } catch {
    /* HTML 默认 */
  }
}

function applyGuidesCatalogCounts(c) {
  if (!c) return;
  document.querySelectorAll("[data-kit-stat='skills'] strong").forEach((el) => {
    if (c.skills != null) el.textContent = String(c.skills);
  });
  document.querySelectorAll("[data-kit-stat-inline='agent_roles']").forEach((el) => {
    if (c.agents != null) el.textContent = `${c.agents} 角色`;
  });
  document.querySelectorAll("[data-kit-stat-inline='workflows']").forEach((el) => {
    if (c.workflows != null) el.textContent = `${c.workflows} 工作流`;
  });
  if (document.body.getAttribute("data-kit-page") !== "skills-catalog") return;
  const titleCounts = `${c.skills} Skills / ${c.agents} Agents / ${c.workflows} Workflows`;
  if (c.skills != null) {
    document.title = `wawoo-skills 专家技能收录（${titleCounts}）— AI 编程工程实践库`;
  }
}

function initGuidesCatalogFilter() {
  if (document.body.getAttribute("data-kit-page") !== "skills-catalog") return;
  const input = document.getElementById("guides-filter");
  const chips = document.querySelectorAll(".skill-chip");
  if (!input || !chips.length) return;

  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    chips.forEach((chip) => {
      const li = chip.closest("li");
      if (!li) return;
      li.hidden = Boolean(q && !chip.textContent.toLowerCase().includes(q));
    });
    document.querySelectorAll(".skills-catalog-section").forEach((sec) => {
      const any =
        !q || [...sec.querySelectorAll(".skill-chip")].some((c) => !c.closest("li")?.hidden);
      sec.classList.toggle("is-filter-empty", Boolean(q) && !any);
    });
  });
}

function loadCapabilitiesCatalog() {
  if (document.body.getAttribute("data-kit-page") !== "skills-catalog") return;
  initGuidesCatalogFilter();
}

function initDemoTabs() {
  const tabs = document.querySelectorAll("[data-demo-tab]");
  const panels = document.querySelectorAll("[data-demo-panel]");
  if (!tabs.length) return;

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const key = tab.getAttribute("data-demo-tab");
      tabs.forEach((t) => {
        const on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.forEach((panel) => {
        const show = panel.getAttribute("data-demo-panel") === key;
        panel.classList.toggle("is-active", show);
        panel.hidden = !show;
      });
    });
  });
}

async function loadGithubBadge() {
  const el = document.querySelector("[data-kit-github-badge]");
  if (!el) return;
  const base = "GitHub Stars";
  try {
    const res = await fetch("https://api.github.com/repos/parkwoo/wawoo-agent-skills", {
      headers: { Accept: "application/vnd.github+json" },
    });
    if (!res.ok) return;
    const data = await res.json();
    const stars = data.stargazers_count;
    if (stars == null) return;
    const icon = el.querySelector("svg");
    el.textContent = "";
    if (icon) el.appendChild(icon);
    el.appendChild(document.createTextNode(` ${base} ${stars.toLocaleString("zh-CN")}`));
  } catch {
    /* 保留默认 … */
  }
}

(async () => {
  await loadSiteMetrics();
  await loadHomeCopy();
  await loadSkillsCatalogCopy();
  await loadChangelogCopy();
  loadCapabilitiesCatalog();
  initDemoTabs();
  initChangelogAnchorCopy();
  loadGithubBadge();
})();

// FAQ: single-open accordion (progressive enhancement)
document.querySelectorAll(".faq details").forEach((el) => {
  el.addEventListener("toggle", () => {
    if (!el.open) return;
    document.querySelectorAll(".faq details").forEach((other) => {
      if (other !== el) other.open = false;
    });
  });
});

const navKey = document.body.getAttribute("data-kit-nav");
if (navKey) {
  document.querySelectorAll(`.nav a[data-nav="${navKey}"]`).forEach((a) => {
    a.classList.add("is-active");
  });
}

document.querySelectorAll("[data-kit-lang-select]").forEach((sel) => {
  const current = sel.getAttribute("data-current") || "zh";
  if (sel.querySelector(`option[value="${current}"]`)) {
    sel.value = current;
  }
  sel.addEventListener("change", () => {
    const opt = sel.selectedOptions[0];
    if (!opt || opt.disabled) {
      sel.value = current;
      return;
    }
    const href = opt.getAttribute("data-href");
    if (!href || href === "#") {
      sel.value = current;
      return;
    }
    window.location.assign(href);
  });
});

function textFromCopyTarget(el) {
  if (!el) return "";
  const lines = [...el.querySelectorAll(".mock-line")]
    .map((p) => p.textContent.replace(/^\$\s*/, "").trim())
    .filter(Boolean);
  return lines.length ? lines.join("\n") : el.textContent.trim();
}

document.querySelectorAll("[data-copy]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const sel = btn.getAttribute("data-copy");
    const el = sel ? document.querySelector(sel) : btn.previousElementSibling;
    const text = textFromCopyTarget(el) || (el && "textContent" in el ? el.textContent.trim() : "");
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      const label = btn.getAttribute("data-copied-label") || "已复制";
      const prev = btn.textContent;
      btn.textContent = label;
      setTimeout(() => {
        btn.textContent = prev;
      }, 1500);
    } catch {
      /* clipboard unavailable */
    }
  });
});