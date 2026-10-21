(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (sel, root = document) => root.querySelector(sel);
  const SVG_NS = "http://www.w3.org/2000/svg";
  const COLORS = ["#ffd23f", "#ff8a1f", "#ff2d6f", "#ffe29a", "#7be0ff", "#c38bff"];

  /* ───────── Decorative SVGs ───────── */
  const DEFS = `
    <defs>
      <linearGradient id="dGold" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#ffe29a"/><stop offset=".5" stop-color="#e0a83a"/><stop offset="1" stop-color="#9c6a12"/>
      </linearGradient>
      <radialGradient id="dFlame" cx=".5" cy=".7" r=".6">
        <stop offset="0" stop-color="#fff6c8"/><stop offset=".45" stop-color="#ffc23d"/><stop offset="1" stop-color="#ff6a00"/>
      </radialGradient>
      <radialGradient id="dGlow"><stop offset="0" stop-color="#ffcf6b" stop-opacity=".7"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient>
    </defs>`;

  function diyaSvg(i) {
    return `<svg viewBox="-80 -90 160 140" style="--f:${(1.2 + (i % 4) * 0.25).toFixed(2)}s">
      <ellipse class="flame-glow" cx="0" cy="-30" rx="70" ry="60" fill="url(#dGlow)"/>
      <path d="M-70 0 Q-64 44 0 48 Q64 44 70 0 Q0 14 -70 0 Z" fill="url(#dGold)"/>
      <path d="M-70 0 Q0 14 70 0 Q0 -10 -70 0 Z" fill="#7a3f0c"/>
      <path d="M70 0 Q84 -3 88 -9 Q80 -1 70 0Z" fill="url(#dGold)"/>
      <g class="flame"><path d="M0 -58 Q15 -34 9 -19 Q4 -8 0 -6 Q-4 -8 -9 -19 Q-15 -34 0 -58Z" fill="url(#dFlame)"/>
      <path d="M0 -34 Q5 -22 2 -15 Q0 -12 -2 -15 Q-5 -22 0 -34Z" fill="#fff"/></g>
    </svg>`;
  }

  function lanternSvg(c1, c2) {
    const tassels = [-26, -16, -6, 4, 14, 24]
      .map((x, i) => `<line x1="${x}" y1="${78 - Math.abs(x) * 1.2}" x2="${x}" y2="${118 + (i % 3) * 14}" stroke="${COLORS[i % 3]}" stroke-width="2.5" stroke-linecap="round"/>`)
      .join("");
    return `<svg viewBox="-50 -10 100 160">
      <line x1="0" y1="-400" x2="0" y2="0" stroke="#e0a83a" stroke-width="1.5"/>
      <rect x="-8" y="-4" width="16" height="8" rx="2" fill="url(#dGold)"/>
      <path d="M0 2 L40 40 L0 80 L-40 40 Z" fill="${c1}"/>
      <path d="M0 2 L20 40 L0 80 L-20 40 Z" fill="${c2}"/>
      <path d="M0 2 L9 40 L0 80 L-9 40 Z" fill="#ffd27a" opacity=".85"/>
      <path d="M-40 40 H40" stroke="url(#dGold)" stroke-width="3"/>
      ${tassels}
    </svg>`;
  }

  function rangoliSvg() {
    const rings = [
      [16, 380, 70, 130, "#7a5cff"],
      [12, 290, 58, 115, "#ff2d6f"],
      [12, 200, 50, 90, "#ff8a1f"],
      [8, 115, 38, 64, "#ffd23f"],
    ];
    let petals = "";
    rings.forEach(([n, r, rx, ry, c], ring) => {
      for (let k = 0; k < n; k++) {
        const a = (360 / n) * k + (ring % 2) * (180 / n);
        petals += `<ellipse cx="0" cy="${-r + ry}" rx="${rx}" ry="${ry}" fill="${c}" transform="rotate(${a.toFixed(1)})"/>`;
      }
    });
    let dots = "";
    for (let k = 0; k < 32; k++) {
      const a = (Math.PI * 2 * k) / 32;
      dots += `<circle cx="${(460 * Math.cos(a)).toFixed(0)}" cy="${(460 * Math.sin(a)).toFixed(0)}" r="12" fill="${k % 2 ? "#22c3a6" : "#ffd23f"}"/>`;
    }
    return `<svg viewBox="-500 -500 1000 1000">${petals}${dots}<circle r="60" fill="#ffd23f"/></svg>`;
  }

  // Shared gradient defs, once per page.
  const defsHost = document.createElementNS(SVG_NS, "svg");
  defsHost.setAttribute("width", "0");
  defsHost.setAttribute("height", "0");
  defsHost.setAttribute("aria-hidden", "true");
  defsHost.style.position = "absolute";
  defsHost.innerHTML = DEFS;
  document.body.prepend(defsHost);

  $("#diyaRow").innerHTML = Array.from({ length: 7 }, (_, i) => diyaSvg(i)).join("");
  $("#rangoliBg").innerHTML = rangoliSvg();

  const lanterns = [
    { left: "6%", w: 64, len: 90, c1: "#d6283f", c2: "#ff5b3a", dur: 4.6, delay: -1 },
    { left: "20%", w: 48, len: 40, c1: "#ff8a1f", c2: "#ffd23f", dur: 5.4, delay: -3, hideSm: true },
    { left: "78%", w: 52, len: 60, c1: "#7a5cff", c2: "#ff2d6f", dur: 5, delay: -2, hideSm: true },
    { left: "90%", w: 66, len: 110, c1: "#d6283f", c2: "#ffb200", dur: 4.2, delay: -0.5 },
  ];
  $("#lanterns").innerHTML = lanterns
    .map(
      (l) => `<div class="lantern${l.hideSm ? " lantern--hide-sm" : ""}" style="left:${l.left};--w:${l.w}px;--dur:${l.dur}s;--delay:${l.delay}s;top:${l.len}px">${lanternSvg(l.c1, l.c2)}</div>`
    )
    .join("");

  /* ───────── Countdown ───────── */
  const countdown = $("#countdown");
  const target = new Date(`${window.AFFILIATE_CONFIG.DIWALI_DATE}T00:00:00+05:30`);
  if (!Number.isNaN(target.getTime())) {
    const days = Math.ceil((target - Date.now()) / 86400000);
    if (days > 1) countdown.textContent = `${days} days to Diwali`;
    else if (days === 1) countdown.textContent = "Diwali is tomorrow";
    else if (days > -5) countdown.textContent = "Happy Diwali!";
    countdown.hidden = !countdown.textContent;
  }

  /* ───────── Decor shortcut ───────── */
  $("#decorBtn").addEventListener("click", () => {
    const chip = [...document.querySelectorAll("#categoryFilter .chip")].find((c) => c.textContent === "Decor");
    chip?.click();
    $("#shop").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  });

  /* ───────── Fireworks ───────── */
  if (reduceMotion) return;

  const hero = $("#hero");
  const canvas = $("#fireworks");
  const ctx = canvas.getContext("2d");
  const particles = [];
  const MAX_PARTICLES = 900;
  let width = 0;
  let height = 0;
  let running = false;
  let nextBurst = 0;
  let last = 0;

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = hero.clientWidth;
    height = hero.clientHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function burst(x, y) {
    const color = COLORS[(Math.random() * COLORS.length) | 0];
    const count = 60 + ((Math.random() * 40) | 0);
    const power = 2.2 + Math.random() * 2;
    for (let i = 0; i < count && particles.length < MAX_PARTICLES; i++) {
      const a = (Math.PI * 2 * i) / count + Math.random() * 0.1;
      const v = power * (0.6 + Math.random() * 0.4);
      particles.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, decay: 0.008 + Math.random() * 0.01, color });
    }
  }

  function frame(t) {
    if (!running) return;
    const dt = Math.min((t - last) / 16.67, 3);
    last = t;

    if (t > nextBurst) {
      burst(width * (0.12 + Math.random() * 0.76), height * (0.08 + Math.random() * 0.38));
      nextBurst = t + 700 + Math.random() * 1100;
    }

    ctx.globalCompositeOperation = "destination-out";
    ctx.fillStyle = "rgba(0,0,0,0.22)";
    ctx.fillRect(0, 0, width, height);
    ctx.globalCompositeOperation = "lighter";

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.vx *= 0.985;
      p.vy = p.vy * 0.985 + 0.035 * dt;
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= p.decay * dt;
      if (p.life <= 0) {
        particles.splice(i, 1);
        continue;
      }
      ctx.globalAlpha = p.life;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.6 + p.life * 1.2, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(frame);
  }

  function setRunning(on) {
    if (on === running) return;
    running = on;
    if (on) {
      last = performance.now();
      requestAnimationFrame(frame);
    }
  }

  // Only animate while the hero is on screen and the tab is visible.
  let heroVisible = true;
  new IntersectionObserver(([entry]) => {
    heroVisible = entry.isIntersecting;
    setRunning(heroVisible && !document.hidden);
  }).observe(hero);
  document.addEventListener("visibilitychange", () => setRunning(heroVisible && !document.hidden));

  hero.addEventListener("pointerdown", (e) => {
    if (e.target.closest("a, button")) return;
    const r = hero.getBoundingClientRect();
    burst(e.clientX - r.left, e.clientY - r.top);
  });

  window.addEventListener("resize", resize);
  resize();
  setRunning(true);
})();
