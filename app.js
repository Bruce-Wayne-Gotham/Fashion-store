(() => {
  "use strict";

  const { STORES, PRODUCTS, AMAZON_TAG } = window.AFFILIATE_CONFIG;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canHover = window.matchMedia("(hover: hover)").matches;
  const $ = (sel, root = document) => root.querySelector(sel);

  /* ───────── Affiliate links ───────── */
  function affiliateUrl(raw, store) {
    let url;
    try {
      url = new URL(raw);
    } catch {
      return "#";
    }
    if (url.protocol !== "https:" && url.protocol !== "http:") return "#";
    if (store === "amazon" && AMAZON_TAG && /(^|\.)amazon\./.test(url.hostname) && !url.searchParams.has("tag")) {
      url.searchParams.set("tag", AMAZON_TAG);
    }
    return url.toString();
  }

  const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /* ───────── Product card ───────── */
  function productCard(p) {
    const store = STORES[p.store];
    const card = el("article", "card");

    const media = el("div", "card__media");
    media.append(el("span", "card__fallback", p.brand.charAt(0)));
    const img = el("img");
    img.alt = `${p.brand} ${p.title}`;
    img.loading = "lazy";
    img.decoding = "async";
    img.addEventListener("load", () => img.classList.add("is-loaded"));
    img.addEventListener("error", () => {
      // Fall back to the bundled illustration (e.g. AI image not generated yet).
      if (p.art && !img.src.endsWith(p.art)) img.src = p.art;
      else img.remove();
    });
    img.src = p.image || p.art;
    media.append(img);
    if (p.badge) media.append(el("span", "badge", p.badge));
    const pill = el("span", "store-pill", store.name);
    pill.dataset.store = p.store;
    pill.style.setProperty("--pill", store.color);
    media.append(pill);

    const body = el("div", "card__body");
    body.append(el("span", "card__brand", p.brand), el("h3", "card__title", p.title));
    const price = el("div", "price");
    price.append(
      p.price ? el("span", "price__now", inr.format(p.price)) : el("span", "price__ask", `See price on ${store.name}`)
    );
    if (p.price && p.mrp > p.price) {
      price.append(
        el("span", "price__mrp", inr.format(p.mrp)),
        el("span", "price__off", `${Math.round((1 - p.price / p.mrp) * 100)}% off`)
      );
    }
    body.append(price, el("span", "card__cta", `Buy on ${store.name}`));

    const link = el("a", "card__link");
    link.href = affiliateUrl(p.url, p.store);
    link.target = "_blank";
    link.rel = "sponsored noopener noreferrer";
    const priceLabel = p.price ? `, ${inr.format(p.price)}` : "";
    link.setAttribute("aria-label", `${p.brand} ${p.title}${priceLabel} — buy on ${store.name}`);

    card.append(media, body, link);
    if (canHover && !reduceMotion) attachTilt(card);
    return card;
  }

  function attachTilt(card) {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top) / r.height;
      card.classList.add("is-tilting");
      card.style.setProperty("--ry", `${(x - 0.5) * 8}deg`);
      card.style.setProperty("--rx", `${(0.5 - y) * 8}deg`);
      card.style.setProperty("--mx", `${x * 100}%`);
      card.style.setProperty("--my", `${y * 100}%`);
    });
    card.addEventListener("pointerleave", () => {
      card.classList.remove("is-tilting");
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  }

  /* ───────── Filters + grid ───────── */
  const grid = $("#grid");
  const empty = $("#empty");
  const segmented = $("#storeFilter");
  const thumb = $(".segmented__thumb", segmented);
  const chipsWrap = $("#categoryFilter");
  const state = { store: "all", category: "All" };

  const categories = ["All", ...new Set(PRODUCTS.map((p) => p.category))];
  categories.forEach((c) => {
    const chip = el("button", "chip", c);
    chip.type = "button";
    chip.setAttribute("aria-pressed", String(c === state.category));
    chip.addEventListener("click", () => {
      state.category = c;
      chipsWrap.querySelectorAll(".chip").forEach((b) => b.setAttribute("aria-pressed", String(b === chip)));
      renderGrid();
    });
    chipsWrap.append(chip);
  });

  function moveThumb() {
    const active = $('[aria-selected="true"]', segmented);
    thumb.style.width = `${active.offsetWidth}px`;
    thumb.style.transform = `translateX(${active.offsetLeft}px)`;
  }

  segmented.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-store]");
    if (!btn) return;
    state.store = btn.dataset.store;
    segmented.querySelectorAll("button").forEach((b) => b.setAttribute("aria-selected", String(b === btn)));
    moveThumb();
    renderGrid();
  });

  function renderGrid() {
    const list = PRODUCTS.filter(
      (p) => (state.store === "all" || p.store === state.store) && (state.category === "All" || p.category === state.category)
    );
    grid.replaceChildren(
      ...list.map((p, i) => {
        const c = productCard(p);
        c.classList.add("is-entering");
        c.style.setProperty("--i", i);
        return c;
      })
    );
    empty.hidden = list.length > 0;
  }

  /* ───────── Trending carousel (biggest discount first) ───────── */
  const carousel = $("#carousel");
  const discount = (p) => (p.price && p.mrp ? p.mrp / p.price : 0);
  [...PRODUCTS]
    .filter((p) => discount(p) > 1)
    .sort((a, b) => discount(b) - discount(a))
    .slice(0, 8)
    .forEach((p) => carousel.append(productCard(p)));

  document.querySelectorAll(".carousel-nav .circle-btn").forEach((btn) =>
    btn.addEventListener("click", () => {
      const step = carousel.querySelector(".card")?.offsetWidth ?? 300;
      carousel.scrollBy({ left: Number(btn.dataset.dir) * (step + 20), behavior: reduceMotion ? "auto" : "smooth" });
    })
  );

  /* ───────── Store tiles ───────── */
  const tiles = $("#storeTiles");
  Object.entries(STORES).forEach(([key, s], i) => {
    const a = el("a", "store-tile reveal");
    a.dataset.store = key;
    a.style.setProperty("--d", `${i * 0.12}s`);
    a.href = affiliateUrl(s.url, key);
    a.target = "_blank";
    a.rel = "sponsored noopener noreferrer";
    const n = PRODUCTS.filter((p) => p.store === key).length;
    a.append(
      el("span", "count", `${n} picks`),
      el("h3", null, s.name),
      el("p", null, s.tagline),
      el("span", "go", `Shop ${s.name} ›`)
    );
    tiles.append(a);
  });

  /* ───────── Reveal on scroll ───────── */
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-visible");
          io.unobserve(en.target);
        }
      }),
    { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
  );
  document.querySelectorAll(".hero .reveal").forEach((n, i) => n.style.setProperty("--d", `${i * 0.12}s`));
  document.querySelectorAll(".reveal").forEach((n) => io.observe(n));

  /* ───────── Scroll-driven motion ───────── */
  const nav = $("#nav");
  const progress = $(".progress");
  const zoom = $("#zoom");
  const zoomFrame = $(".zoom__frame");
  const zoomImg = $(".zoom__frame img");
  const zoomCap = $(".zoom__caption");
  const floats = [...document.querySelectorAll(".float")];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  let ticking = false;
  function onScroll() {
    const y = window.scrollY;
    const vh = window.innerHeight;
    const max = document.documentElement.scrollHeight - vh;

    nav.classList.toggle("is-scrolled", y > 10);
    progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;

    if (!reduceMotion) {
      // Hero parallax
      if (y < vh * 1.2) {
        floats.forEach((f) => {
          const depth = parseFloat(f.dataset.depth);
          f.style.transform = `translate3d(0, ${-y * depth}px, 0)`;
        });
      }
      // Apple-style expanding image (not every page has one)
      if (zoom) {
        const r = zoom.getBoundingClientRect();
        const t = clamp(-r.top / (r.height - vh));
        const ease = 1 - Math.pow(1 - clamp(t / 0.6), 3);
        zoomFrame.style.setProperty("--inset", `${18 * (1 - ease)}%`);
        zoomFrame.style.setProperty("--zr", `${40 * (1 - ease)}px`);
        zoomImg.style.setProperty("--zs", (1.25 - 0.25 * ease).toFixed(4));
        zoomCap.style.setProperty("--co", clamp((t - 0.45) / 0.25).toFixed(3));
      }
    }
    ticking = false;
  }
  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );
  window.addEventListener("resize", () => {
    moveThumb();
    onScroll();
  });

  // Hero images fail gracefully
  document.querySelectorAll(".float img, .zoom__frame img").forEach((img) => {
    const fallback = img.dataset.fallback;
    const hide = () => {
      if (fallback && !img.src.endsWith(fallback)) img.src = fallback;
      else img.style.visibility = "hidden";
    };
    if (img.complete && img.naturalWidth === 0) hide();
    else img.addEventListener("error", hide);
  });

  $("#year").textContent = new Date().getFullYear();
  renderGrid();
  moveThumb();
  onScroll();
})();
