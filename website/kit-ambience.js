/**
 * 全页深海氛围：泡泡 + 指针视差；Hero 正本 PNG 游动（不用 SVG 重绘角色，保持线稿一致）
 */
(function () {
  const body = document.body;
  if (!body.hasAttribute("data-kit-ambience")) return;

  const docsMode = body.classList.contains("kit-docs");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mascot = document.querySelector("[data-hero-mascot]");
  const swim = mascot && mascot.querySelector(".hero-mascot-swim");
  const heroEl = document.querySelector(".hero");

  let pointer = { x: 0, y: 0, active: false };
  let scrollY = 0;
  let maxScroll = 1;
  let raf = 0;
  const start = performance.now();
  let offX = 0;
  let offY = 0;
  const home = { cx: 0, cy: 0, half: 96 };

  /** 开场 15s：手电光有、无海沟图，角色静止；之后进入完整演绎 */
  const INTRO_MS = 15000;

  /** 人物动作节奏：相对初版放慢 70%（速度 ×0.3） */
  const MOTION = 0.3;
  const CHASE_FOLLOW = 0.038 * MOTION;
  const FLEE_FOLLOW = 0.044 * MOTION;
  const RETURN = 0.032 * MOTION;
  /** 平移上限体感：单层 PNG，偏移宜小 */
  const POINTER_PULL = 0.1;
  const FLEE_PUSH = 1.15;
  /** 指针落在光斑内、且离角色中心足够近 → 触发逃跑 */
  const BEAM_HIT = 0.52;
  let mascotFleeing = false;
  const HERO_PAD = 10;

  function measureHome() {
    if (!mascot || !swim) return;
    const m = mascot.getBoundingClientRect();
    home.cx = m.left + m.width / 2 - offX;
    home.cy = m.top + m.height / 2 - offY;
    home.half = Math.max(m.width, m.height) * 0.46;
  }

  function heroRect() {
    return heroEl ? heroEl.getBoundingClientRect() : null;
  }

  function pointerInHero(hr) {
    if (!hr || !pointer.active) return false;
    return (
      pointer.x >= hr.left &&
      pointer.x <= hr.right &&
      pointer.y >= hr.top &&
      pointer.y <= hr.bottom
    );
  }

  function clampOffset(ox, oy, hr) {
    if (!hr) return { x: ox, y: oy };
    const half = home.half;
    const cx = home.cx + ox;
    const cy = home.cy + oy;
    const minX = hr.left + HERO_PAD + half;
    const maxX = hr.right - HERO_PAD - half;
    const minY = hr.top + HERO_PAD + half;
    const maxY = hr.bottom - HERO_PAD - half;
    const clampedCx = Math.min(maxX, Math.max(minX, cx));
    const clampedCy = Math.min(maxY, Math.max(minY, cy));
    return { x: clampedCx - home.cx, y: clampedCy - home.cy };
  }

  /* —— Canvas 海底 —— */
  const canvas = document.createElement("canvas");
  canvas.className = "kit-ambience-canvas";
  canvas.setAttribute("aria-hidden", "true");
  /* 文档页未必加载 styles.css；内联兜底，避免 canvas 撑开整页布局 */
  Object.assign(canvas.style, {
    position: "fixed",
    inset: "0",
    top: "0",
    left: "0",
    width: "100%",
    height: "100%",
    maxWidth: "none",
    maxHeight: "none",
    margin: "0",
    padding: "0",
    zIndex: "0",
    pointerEvents: "none",
    display: "block",
  });
  body.prepend(canvas);
  const ctx = canvas.getContext("2d");
  const trenchLayer = document.createElement("canvas");
  const trenchCtx = trenchLayer.getContext("2d");

  const bubbles = [];
  const BUBBLE_N = reduced ? 18 : 48;
  const OCEAN_BG_SRC = "/assets/marketing/ocean-trench-panorama.png";
  let oceanBg = null;
  let oceanBgReady = false;
  const oceanImg = new Image();
  oceanImg.decoding = "async";
  oceanImg.src = OCEAN_BG_SRC;
  oceanImg.onload = () => {
    oceanBg = oceanImg;
    oceanBgReady = true;
  };

  function updateScroll() {
    scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    maxScroll = Math.max(
      1,
      (document.documentElement.scrollHeight || 0) - innerHeight
    );
  }

  /** 下滚 = 下潜：海水渐变随页轻微上移变暗 */
  function fillDarkSea(w, h) {
    const dive = reduced ? 0 : scrollY * 0.18;
    const g = ctx.createLinearGradient(0, -dive, 0, h + dive * 0.35);
    const deep = Math.min(0.12, (scrollY / maxScroll) * 0.12);
    g.addColorStop(0, "#0a0e0d");
    g.addColorStop(0.45, `rgb(${16 - deep * 40}, ${22 - deep * 40}, ${21 - deep * 40})`);
    g.addColorStop(1, "#050706");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
  }

  /** 全景海沟：柔边光斑内绘制，无硬圈；随滚动下潜 */
  function drawTrenchInBeam(w, h, px, py, beamR) {
    if (!oceanBgReady || !oceanBg) return;
    const iw = oceanBg.naturalWidth;
    const ih = oceanBg.naturalHeight;
    const scale = Math.max((h / ih) * 2.4, (w * 1.15) / iw);
    const dw = iw * scale;
    const dh = ih * scale;
    const parallaxX = (px / w - 0.5) * Math.max(0, dw - w) * 0.4;
    const scrollFrac = scrollY / maxScroll;
    const diveTravel = Math.max(0, dh - h);
    const diveY = scrollFrac * diveTravel + scrollY * 0.28;
    const dx = (w - dw) / 2 - parallaxX;
    let dy = (h - dh) / 2 - diveY;
    const minDy = h - dh - 24;
    const maxDy = 24;
    dy = Math.min(maxDy, Math.max(minDy, dy));

  const outerR = beamR * 1.18;
  const pad = outerR + 4;
  const tw = Math.ceil(w);
  const th = Math.ceil(h);
  if (trenchLayer.width !== tw || trenchLayer.height !== th) {
    trenchLayer.width = tw;
    trenchLayer.height = th;
  }
  trenchCtx.setTransform(1, 0, 0, 1, 0, 0);
  trenchCtx.clearRect(0, 0, tw, th);
  trenchCtx.globalAlpha = 0.58;
  trenchCtx.drawImage(oceanBg, dx, dy, dw, dh);
  trenchCtx.globalAlpha = 1;
  trenchCtx.globalCompositeOperation = "destination-in";
  const tMask = trenchCtx.createRadialGradient(px, py, 0, px, py, outerR);
    tMask.addColorStop(0, "rgba(255, 255, 255, 1)");
    tMask.addColorStop(0.32, "rgba(255, 255, 255, 0.62)");
    tMask.addColorStop(0.58, "rgba(255, 255, 255, 0.18)");
    tMask.addColorStop(0.82, "rgba(255, 255, 255, 0.04)");
    tMask.addColorStop(1, "rgba(255, 255, 255, 0)");
    trenchCtx.fillStyle = tMask;
    trenchCtx.fillRect(px - pad, py - pad, pad * 2, pad * 2);
    trenchCtx.globalCompositeOperation = "source-over";
    trenchCtx.fillStyle = "rgba(0, 0, 0, 0.3)";
    trenchCtx.fillRect(0, 0, tw, th);

    ctx.drawImage(trenchLayer, 0, 0, w, h);
  }

  function drawFlashlightGlow(w, h, px, py, beamR) {
    const outerR = beamR * 1.22;
    const glow = ctx.createRadialGradient(px, py, 0, px, py, outerR);
    glow.addColorStop(0, "rgba(240, 252, 246, 0.12)");
    glow.addColorStop(0.2, "rgba(55, 185, 110, 0.17)");
    glow.addColorStop(0.48, "rgba(35, 153, 86, 0.065)");
    glow.addColorStop(0.72, "rgba(35, 153, 86, 0.022)");
    glow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, w, h);
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(innerWidth * dpr);
    canvas.height = Math.floor(innerHeight * dpr);
    canvas.style.width = `${innerWidth}px`;
    canvas.style.height = `${innerHeight}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (bubbles.length === 0) seedBubbles();
    measureHome();
  }

  function seedBubbles() {
    bubbles.length = 0;
    for (let i = 0; i < BUBBLE_N; i++) {
      const r = 2 + Math.random() * 7;
      bubbles.push({
        x: Math.random() * innerWidth,
        y: innerHeight + Math.random() * innerHeight * 0.5,
        r,
        vy: 0.14 + Math.random() * 0.38 + r * 0.025,
        wobble: Math.random() * Math.PI * 2,
        ink: 0.1 + Math.random() * 0.1,
      });
    }
  }

  /** 线稿泡：空心白圈 + 左上短弧，与 Q 版章鱼 PNG 线宽气质一致 */
  function drawBubble(b) {
    const { x, y, r, ink } = b;
    const lw = Math.max(0.7, Math.min(1.25, 0.55 + r * 0.09));
    ctx.save();
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255, 255, 255, ${ink})`;
    ctx.lineWidth = lw;
    ctx.stroke();

    if (r > 2.2) {
      ctx.beginPath();
      ctx.arc(x, y, r * 0.94, -Math.PI * 0.78, -Math.PI * 0.42);
      ctx.strokeStyle = `rgba(255, 255, 255, ${Math.min(0.28, ink + 0.06)})`;
      ctx.lineWidth = lw * 0.88;
      ctx.stroke();
    }
    ctx.restore();
  }

  function tickBubbles(t) {
    const w = innerWidth;
    const h = innerHeight;
    for (const b of bubbles) {
      b.y -= b.vy;
      b.x += Math.sin(t * 0.9 + b.wobble) * 0.12;
      if (b.y < -b.r - 8) {
        b.y = h + b.r + 8 + Math.random() * 40;
        b.x = Math.random() * w;
      }
    }
  }

  function drawOcean(now) {
    const w = innerWidth;
    const h = innerHeight;
    fillDarkSea(w, h);

    const beamR = Math.min(300, Math.max(160, Math.min(w, h) * 0.26));
    const canBeam = !reduced && (pointer.active || docsMode);
    const px = pointer.active ? pointer.x : w * 0.5;
    const py = pointer.active ? pointer.y : h * 0.38;
    const showTrench =
      oceanBgReady && (docsMode ? true : introLive(now));

    if (canBeam) {
      if (showTrench) {
        drawTrenchInBeam(w, h, px, py, beamR);
      }
      drawFlashlightGlow(w, h, px, py, beamR);
    }

    const t = now * 0.001;
    if (!reduced) tickBubbles(t);
    for (const b of bubbles) drawBubble(b);
  }

  function beamRadius() {
    return Math.min(300, Math.max(160, Math.min(innerWidth, innerHeight) * 0.26));
  }

  function tickMascotChaseOrFlee() {
    mascotFleeing = false;
    if (!swim || reduced) {
      offX += (0 - offX) * RETURN;
      offY += (0 - offY) * RETURN;
      return;
    }

    measureHome();

    const hr = heroRect();
    if (!pointer.active) {
      offX += (0 - offX) * RETURN;
      offY += (0 - offY) * RETURN;
      return;
    }

    const mx = home.cx + offX;
    const my = home.cy + offY;
    const dx = pointer.x - mx;
    const dy = pointer.y - my;
    const dist = Math.hypot(dx, dy);
    const beamR = beamRadius();
    const lit = dist < beamR * BEAM_HIT;

    if (!lit) {
      const wantX = (pointer.x - home.cx) * POINTER_PULL;
      const wantY = (pointer.y - home.cy) * POINTER_PULL;
      const clamped = clampOffset(wantX, wantY, hr);
      offX += (clamped.x - offX) * CHASE_FOLLOW;
      offY += (clamped.y - offY) * CHASE_FOLLOW;
      return;
    }

    if (dist < 1) {
      offX += (0 - offX) * RETURN;
      offY += (0 - offY) * RETURN;
      return;
    }

    mascotFleeing = true;
    const closeness = 1 - dist / (beamR * BEAM_HIT);
    const ux = -dx / dist;
    const uy = -dy / dist;
    const push = FLEE_PUSH * (0.65 + closeness * 0.85);
    offX += ux * push;
    offY += uy * push;
    const clamped = clampOffset(offX, offY, hr);
    offX += (clamped.x - offX) * FLEE_FOLLOW;
    offY += (clamped.y - offY) * FLEE_FOLLOW;
  }

  function introLive(now) {
    return now - start >= INTRO_MS;
  }

  function applyMascot(now) {
    if (!swim) return;
    if (!introLive(now)) {
      offX = 0;
      offY = 0;
      swim.style.transform = "translate(0px, 0px) scale(1)";
      return;
    }
    tickMascotChaseOrFlee();

    const t = (now - start - INTRO_MS) * 0.001 * MOTION;
    const w = innerWidth;
    const h = innerHeight;
    const px = pointer.active ? pointer.x : w * 0.5;
    const py = pointer.active ? pointer.y : h * 0.33;
    const mx = home.cx + offX;
    const my = home.cy + offY;
    let nx;
    let ny;
    if (mascotFleeing && pointer.active) {
      nx = (mx - px) / w;
      ny = (my - py) / h;
    } else {
      nx = px / w - 0.5;
      ny = py / h - 0.5;
    }

    const swimAmp = mascotFleeing ? 1.08 : 1;
    const swimX =
      (Math.sin(t * 1.05) * 4 + Math.sin(t * 2.1) * 1.5) * swimAmp;
    const swimY =
      (Math.sin(t * 0.85) * 3 + Math.cos(t * 1.4) * 1) * swimAmp;
    const rotZ =
      Math.sin(t * 0.9) * 2 + (mascotFleeing ? Math.sin(t * 4.2) * 1.5 : 0);
    const tilt = mascotFleeing ? 4 : 3;
    const rotY = reduced ? 0 : nx * tilt;
    const rotX = reduced ? 0 : -ny * (tilt - 0.5);
    const scale = 1 + Math.sin(t * 1.35) * 0.012 + (mascotFleeing ? 0.008 : 0);

    swim.style.transform =
      `translate(${offX + swimX}px, ${offY + swimY}px) ` +
      `rotateX(${rotX}deg) rotateY(${rotY}deg) rotate(${rotZ}deg) ` +
      `scale(${scale})`;
  }

  function frame(now) {
    drawOcean(now);
    applyMascot(now);
    if (!reduced) raf = requestAnimationFrame(frame);
    else raf = 0;
  }

  resize();
  measureHome();
  updateScroll();
  window.addEventListener("resize", () => {
    resize();
    updateScroll();
  }, { passive: true });
  window.addEventListener(
    "scroll",
    () => {
      updateScroll();
      measureHome();
    },
    { passive: true }
  );
  window.addEventListener("load", () => {
    measureHome();
    updateScroll();
  }, { once: true });

  window.addEventListener(
    "pointermove",
    (e) => {
      pointer = { x: e.clientX, y: e.clientY, active: true };
    },
    { passive: true }
  );
  document.addEventListener(
    "pointerleave",
    () => {
      pointer.active = false;
    },
    { passive: true }
  );

  if (reduced) {
    frame(performance.now());
  } else {
    raf = requestAnimationFrame(frame);
  }
})();