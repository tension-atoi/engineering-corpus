/* GNU6 web motion runtime — MOTION-STANDARD.md (slice 1, RESEARCH).
 *
 * Load synchronously in <head>: it reads an incoming handoff before first paint so the arriving page never
 * shows its content in place before the arrival motion has positioned it.
 * No dependencies. No opacity anywhere (WM-01): every keyframe passed through Motion.animate is checked.
 */
(() => {
  "use strict";
  const root = document.documentElement;
  const DOMAINS = ["live", "docs", "gnosix"];
  const MODES = ["full", "off", "auto"];
  const KEY = "g6-motion-mode", CHAIN = "g6-motion-chain";
  const store = (area) => ({
    get(k) { try { return area().getItem(k); } catch { return null; } },
    set(k, v) { try { area().setItem(k, v); } catch { /* storage blocked: the choice lasts for this page only */ } },
  });
  const local = store(() => localStorage), session = store(() => sessionStorage);
  const reducedQuery = matchMedia("(prefers-reduced-motion: reduce)");
  const listeners = new Set();

  const Motion = {
    curves: { out: "cubic-bezier(.2,.7,.2,1)", inout: "cubic-bezier(.6,0,.3,1)", in: "cubic-bezier(.5,0,.9,.4)" },
    domains: DOMAINS,
    // Cut-on-motion is the ratified cross-origin handoff; no full-page rotation.
    // Ratified default: cut-the-curve. Wheel remains opt-in for research comparisons only.
    get seam() { const v = root.dataset.g6Seam || new URLSearchParams(location.search).get("seam"); return v === "wheel" ? "wheel" : "cut"; },
    // The cube rotates by 120°, not the page. Content uses a bounded orbital
    // projection: short consistent travel with a slight curved parallax.
    // Wheel is a research comparator, but it is bounded as well.
    seams: {
      wheel: { multiplier: 1.25, bow: 8, easeOut: "cubic-bezier(.4,0,1,.6)", easeIn: "cubic-bezier(0,.4,.3,1)" },
      cut: { multiplier: 1, bow: 4, easeOut: "cubic-bezier(.4,0,1,.65)", easeIn: "cubic-bezier(0,.35,.25,1)" },
    },
    travel(mode = this.mode, width = innerWidth) {
      const distance = Math.max(16, Math.min(30, width * 0.04));
      return distance * this.seams[this.seam].multiplier;
    },
    // Opportunistic destination prefetch; not guaranteed and never an authority boundary.
    prefetch(url) {
      try {
        const href = new URL(url, location.href).href;
        if (document.querySelector(`link[rel="prefetch"][href="${CSS.escape(href)}"]`)) return;
        const l = document.createElement("link"); l.rel = "prefetch"; l.as = "document"; l.href = href; document.head.append(l);
      } catch { /* prefetch is an optimisation only */ }
    },

    // ── Cross-document geometric bridge: a matching, opaque canvas-colour
    // radial shutter on either side of the unavoidable top-level navigation.
    // It covers both the header and content while they are reconstructed, without
    // sharing DOM, cookies or pixels between isolated origins.
    bridge: {
      get active() { return Motion.seam === "cut" && Motion.mode !== "off"; },
      get arriving() { return Boolean(Motion.incoming && this.active); },
      cover(point = { x: 22, y: 22 }) {
        if (!this.active) return Promise.resolve();
        root.style.setProperty("--g6-bridge-x", `${Math.round(point.x)}px`);
        root.style.setProperty("--g6-bridge-y", `${Math.round(point.y)}px`);
        root.dataset.g6Bridge = "covering";
        // Force the initial clip geometry to become an actual CSS state.
        getComputedStyle(root, "::after").clipPath;
        const ms = Math.max(36, Math.round(105 * Motion.scale()));
        root.style.setProperty("--g6-bridge-cover-ms", `${ms}ms`);
        return new Promise((resolve) => {
          requestAnimationFrame(() => {
            root.dataset.g6Bridge = "covered";
            setTimeout(resolve, ms + 10);
          });
        });
      },
      reveal(point = { x: 62, y: 22 }) {
        if (!this.arriving || root.dataset.g6Bridge !== "covered") return Promise.resolve();
        root.style.setProperty("--g6-bridge-x", `${Math.round(point.x)}px`);
        root.style.setProperty("--g6-bridge-y", `${Math.round(point.y)}px`);
        const ms = Math.max(54, Math.round(155 * Motion.scale()));
        root.style.setProperty("--g6-bridge-reveal-ms", `${ms}ms`);
        return new Promise((resolve) => {
          requestAnimationFrame(() => {
            root.dataset.g6Bridge = "uncovering";
            setTimeout(() => { root.removeAttribute("data-g6-bridge"); resolve(); }, ms + 15);
          });
        });
      },
    },

    // ── WM-05 Animated / Off. Auto follows system reduced-motion preference.
    get chosen() { const c = local.get(KEY); return MODES.includes(c) ? c : "auto"; },
    get mode() { return this.chosen === "off" || reducedQuery.matches ? "off" : "full"; },
    setMode(m) { if (!MODES.includes(m)) return; local.set(KEY, m); apply(); },
    on(fn) { listeners.add(fn); return () => listeners.delete(fn); },

    // ── WM-04 degressive budget: 1, .6, .35 for chained navigations within 8 s
    chain() {
      try { const c = JSON.parse(session.get(CHAIN) || "null"); if (c && Date.now() - c.at < 8000) return c.n; } catch { /* corrupt: no chain */ }
      return 0;
    },
    noteNavigation(n = this.chain() + 1) { session.set(CHAIN, JSON.stringify({ n, at: Date.now() })); },
    // chain counts navigations in the current burst, the current one included: 1st = full length
    scale() { return [1, 0.6, 0.35][Math.min(Math.max(0, this.chain() - 1), 2)]; },
    dur(full) { return this.mode === "off" ? 0 : Math.round(full * this.scale()); },

    // ── WM-01 guarded animation: transform/clip-path/size/position only
    animate(el, keyframes, opts) {
      for (const k of keyframes) if ("opacity" in k || "filter" in k) throw new Error("WM-01: opacity/filter keyframes are not allowed on content");
      return el.animate(keyframes, opts);
    },

    // ── geometry correspondence inside one document (FLIP)
    flip(elements, mutate, { duration = 280, easing = this.curves.inout } = {}) {
      const before = new Map(elements.map((e) => [e, e.getBoundingClientRect()]));
      mutate();
      const d = this.dur(duration);
      if (!d) return [];
      return elements.map((e) => {
        const a = before.get(e), b = e.getBoundingClientRect();
        const dx = a.left - b.left, dy = a.top - b.top, sx = a.width / (b.width || 1), sy = a.height / (b.height || 1);
        return this.animate(e, [{ transform: `translate(${dx}px,${dy}px) scale(${sx},${sy})`, transformOrigin: "0 0" }, { transform: "none", transformOrigin: "0 0" }], { duration: d, easing });
      });
    },

    // ── "the world turns around the logo": blocks travel on a 120° arc centred on the cube, text upright
    arc(blocks, { origin, dir = 1, phase = "out", duration } = {}) {
      const m = this.mode;
      const vh = innerHeight, vw = innerWidth;
      const full = phase === "out" ? 160 : 360;
      const d = this.dur(duration || full, phase === "out" ? 110 : 160);
      const anims = [], seam = this.seams[this.seam];
      const travel = this.travel(m, vw);
      if (!d) return { anims, finished: Promise.resolve() };
      const rects = blocks.map((b) => b.getBoundingClientRect());
      blocks.forEach((b, i) => {
        const r = rects[i];
        const onScreen = r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw;
        if (!onScreen) return;                                                    // off-screen blocks are not animated
        const cy = r.top + r.height / 2;
        // A subtle optical orbit: x stays directional and every block has the
        // same start/end displacement; only the intermediate y parallax varies.
        // Never rotate, scale, or sweep text off the screen. No staggered rows.
        const curvature = Math.max(-seam.bow, Math.min(seam.bow, (cy - origin.y) / Math.max(1, vh) * seam.bow));
        const frames = [];
        for (let k = 0; k <= 12; k++) {
          const p = k / 12;
          const x = phase === "out" ? -dir * travel * p : dir * travel * (1 - p);
          const y = curvature * Math.sin(Math.PI * p);
          frames.push({ transform: `translate3d(${x.toFixed(2)}px,${y.toFixed(2)}px,0)`, offset: p });
        }
        anims.push(this.animate(b, frames, { duration: d, delay: 0, easing: phase === "out" ? seam.easeOut : seam.easeIn, fill: phase === "out" ? "forwards" : "backwards" }));
      });
      return { anims, finished: Promise.all(anims.map((a) => a.finished.catch(() => {}))) };
    },

    // ── handoff contract (transport 1: URL fragment)
    handoff: {
      encode({ from, t, mode, chain, anchor }) {
        const ts = Math.floor(Date.now() / 1000);
        return `#g6:v1.${from}.${t}.${mode}.${Math.min(9, chain)}.${ts}${anchor ? "." + anchor : ""}`;
      },
      decode(hash, nowSec = Date.now() / 1000) {
        const m = /^#g6:v1\.(live|docs|gnosix)\.([0-2])\.(full|calm|off|auto)\.([0-9])\.(\d{9,11})(?:\.([A-Za-z0-9_-]{1,64}))?$/.exec(hash || "");
        if (!m) return null;
        const ts = Number(m[5]);
        if (Math.abs(nowSec - ts) > 10) return null;                              // stale: render at rest
        return { from: m[1], t: Number(m[2]), mode: m[3] === "calm" ? "off" : m[3], chain: Number(m[4]), ts, anchor: m[6] || null };
      },
      // Navigate to `url` carrying the departing state. The destination's own fragment becomes `anchor`.
      go(url, state) {
        const u = new URL(url, location.href);
        const anchor = /^#[A-Za-z0-9_-]{1,64}$/.test(u.hash) ? u.hash.slice(1) : null;
        u.hash = this.encode({ ...state, anchor });
        location.assign(u.href);
      },
    },
  };

  function apply() {
    root.dataset.g6Motion = Motion.mode;
    root.dataset.g6MotionChoice = Motion.chosen;
    for (const fn of listeners) fn(Motion.mode);
  }
  reducedQuery.addEventListener("change", apply);

  // ── arrival: runs before first paint
  const incoming = Motion.handoff.decode(location.hash);
  if (location.hash.startsWith("#g6:")) {
    // consume the fragment whatever its validity; restore the real anchor if there was one
    const anchor = incoming && incoming.anchor ? "#" + incoming.anchor : "";
    history.replaceState(history.state, "", location.pathname + location.search + anchor);
  }
  if (incoming) {
    if (incoming.mode !== Motion.chosen && incoming.mode !== "auto") local.set(KEY, incoming.mode);
    Motion.noteNavigation(incoming.chain);
    if (Motion.bridge.active) {
      // The very first styled frame must match the departing covered canvas.
      root.dataset.g6Bridge = "covered";
    } else if (Motion.mode !== "off") {
      const from = DOMAINS.indexOf(incoming.from), cur = DOMAINS.indexOf(root.dataset.g6Domain || root.dataset.domain);
      const dir = cur < 0 || ((cur - from + 3) % 3) === 1 ? 1 : -1;
      root.style.setProperty("--g6-arrival-x", `${dir * Motion.travel()}px`);
      root.dataset.g6Arriving = "";
    }
  }
  Motion.incoming = incoming;
  Motion.domain = root.dataset.g6Domain || root.dataset.domain || null;
  if (incoming && Motion.mode !== "off" && !Motion.bridge.active) {
    // readyState "interactive" fires when parsing ends, before deferred scripts: no blank gap waiting for them
    const start = () => {
      if (Motion.arrival || document.readyState === "loading") return;
      const anchor = document.querySelector("[data-g6-origin]") || document.querySelector("#g6-bar, .g6-bar");
      const r = anchor ? anchor.getBoundingClientRect() : { left: 0, top: 0, height: 44 };
      const origin = { x: r.left + 22, y: r.top + (r.height || 44) / 2 };
      const from = DOMAINS.indexOf(incoming.from), cur = DOMAINS.indexOf(Motion.domain);
      const dir = cur < 0 || ((cur - from + 3) % 3) === 1 ? 1 : -1;
      Motion.arrival = Motion.arc([...document.querySelectorAll("[data-g6-block]")], { origin, dir, phase: "in" });
      root.removeAttribute("data-g6-arriving");
    };
    document.addEventListener("readystatechange", start);
    document.addEventListener("DOMContentLoaded", start);
  }
  apply();
  window.G6Motion = Motion;
})();
