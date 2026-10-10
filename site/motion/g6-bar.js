/* GNU6 living title bar — cube control + typewriter title (MOTION-STANDARD.md §7). Needs G6Motion and G6Rig. */
(() => {
  "use strict";
  const M = window.G6Motion;
  const mod3 = (n) => ((n % 3) + 3) % 3;
  const suffixLen = (a, b) => { let n = 0; while (n < a.length && n < b.length && a[a.length - 1 - n] === b[b.length - 1 - n]) n++; return n; };
  const T = (loc, fr, en) => (loc === "en" ? en : fr);
  // Existing versioned GNU6 identity artwork; no new icon variant or font.
  const ICONS = {live: "gnu6-live", docs: "gnuinlabs", gnosix: "gnosix"};
  const domainForHost = (name) => /^docs\./.test(name) ? "docs" : /^gnosix\./.test(name) ? "gnosix" : "live";
  function favicon(domain) {
    if (!Object.hasOwn(ICONS, domain)) return;
    let link = document.head.querySelector('link[rel="icon"][data-g6-surface-icon]');
    if (!link) {
      link = document.createElement("link");
      link.rel = "icon"; link.type = "image/png"; link.sizes = "64x64";
      link.dataset.g6SurfaceIcon = "";
      document.head.append(link);
    }
    const href = new URL("../motion/identity/" + ICONS[domain] + "-64.png", document.baseURI);
    // Script is classic (not a JS module); its own base is the page's motion path
    // and identical ../.. depth for both /motion/demo and /motion/shell.
    link.href = href.href;
    link.dataset.g6Surface = domain;
  }

  // ── The title's edit plane has two explicitly distinct identity phases:
  // erase in the origin's ink, type in the destination's ink.
  // Keep only ".live" stable: retaining the entire "gnu6.live" would make
  // live -> docs have ZERO erase frames, contradicting the requested handoff.
  function typewriter(el, initial) {
    el.innerHTML = '<span class="g6-tw__pre" aria-hidden="true"></span><span class="g6-tw__caret" aria-hidden="true" hidden></span><span class="g6-tw__suf" aria-hidden="true"></span>';
    const pre = el.children[0], caret = el.children[1], suf = el.children[2];
    let shown = initial, raf = 0, settleTimer = 0, pendingDone = null;
    const setPhase = (phase, domain) => {
      if (phase) { el.dataset.g6TwPhase = phase; el.dataset.g6TwDomain = domain; }
      else { delete el.dataset.g6TwPhase; delete el.dataset.g6TwDomain; }
    };
    const stop = () => {
      cancelAnimationFrame(raf);
      clearTimeout(settleTimer);
      if (pendingDone) { const done = pendingDone; pendingDone = null; done(); }
    };
    const paint = (p, s, editing) => {
      pre.textContent = p; suf.textContent = s; caret.hidden = !editing;
      if (editing) el.dataset.editing = "";
      else { el.removeAttribute("data-editing"); setPhase("rest", domainForHost(shown)); }
    };
    paint(initial.endsWith(".live") ? initial.slice(0, -5) : "", initial.endsWith(".live") ? ".live" : initial, false);
    const atRest = (target) => {
      shown = target;
      paint(target.endsWith(".live") ? target.slice(0, -5) : "", target.endsWith(".live") ? ".live" : target, false);
    };
    return {
      get text() { return shown; },
      write(target, { erase = 38, type = 46, cap = 520, hold = 0, minScale = 0,
        fromDomain = domainForHost(shown), toDomain = domainForHost(target) } = {}) {
        stop();
        const from = shown, n = Math.min(5, suffixLen(from, target));
        const suffix = target.slice(target.length - n), oldPre = from.slice(0, from.length - n), newPre = target.slice(0, target.length - n);
        const steps = oldPre.length + newPre.length, mode = M.mode;
        if (!steps) { atRest(target); return Promise.resolve(); }
        if (mode === "off") { atRest(target); return Promise.resolve(); }
        const k = Math.min(1, cap / (oldPre.length * erase + newPre.length * type)) * Math.max(minScale, M.scale());
        const te = erase * k, tt = type * k, t0 = performance.now();
        return new Promise((done) => {
          pendingDone = done;
          setPhase(oldPre.length ? "erase" : "type", oldPre.length ? fromDomain : toDomain);
          paint(oldPre, suffix, true); // outgoing identity already visible in the event
          const complete = () => { pendingDone = null; done(); };
          const tick = (now) => {
            const e = now - t0, erased = Math.min(oldPre.length, Math.floor(e / te));
            let p = oldPre.slice(0, oldPre.length - erased);
            if (erased >= oldPre.length) {
              setPhase("type", toDomain); // exact turn from origin to destination color
              p = newPre.slice(0, Math.min(newPre.length, Math.floor((e - oldPre.length * te) / tt)));
            }
            shown = p + suffix; paint(p, suffix, true);
            if (erased >= oldPre.length && p.length === newPre.length) {
              shown = target;
              paint(newPre, suffix, hold > 0);
              if (hold > 0) settleTimer = setTimeout(() => { paint(newPre, suffix, false); complete(); }, hold);
              else complete();
              return;
            }
            raf = requestAnimationFrame(tick);
          };
          raf = requestAnimationFrame(tick);
        });
      },
      set(target) { stop(); atRest(target); },
    };
  }

  /* mount(host, {
   *   domain: "live" | "docs" | "gnosix",     current domain (cycle order live → docs → gnosix)
   *   hosts:  { live, docs, gnosix },          full host names shown by the typewriter
   *   homes:  { live, docs, gnosix },          URLs of each domain's home
   *   rig, sdf, locale, commitDelay = 48,   near-immediate navigation after visual acknowledgement
   *   blocks: () => Element[],                 content blocks that travel on the arc
   * }) */
  function mount(host, o) {
    const D = M.domains, cur = D.indexOf(o.domain), loc = o.locale || "fr", delay = o.commitDelay ?? 48;
    host.classList.add("g6-bar");
    host.innerHTML = `<button type="button" class="g6-bar__cube"><span class="g6-bar__rig"></span></button>
<a class="g6-bar__title" href="${o.homes[o.domain]}" aria-label="${o.hosts[o.domain]}"><span class="g6-tw"></span></a>
<span class="g6-bar__hint" hidden></span><p class="g6-visually-hidden" role="status" aria-live="polite"></p>`;
    const btn = host.querySelector(".g6-bar__cube"), title = host.querySelector(".g6-bar__title"), hint = host.querySelector(".g6-bar__hint"), live = host.querySelector("[role=status]");
    const incoming = M.incoming;
    const startT = incoming ? incoming.t : cur;                                     // arrive from the departing pose
    const rig = window.G6Rig.create(host.querySelector(".g6-bar__rig"), o.rig, { t0: startT, sdf: o.sdf, label: o.hosts[D[mod3(startT)]], noWebGL: o.noWebGL, shouldSnap: () => M.mode !== "full" });
    const tw = typewriter(title.querySelector(".g6-tw"), o.hosts[D[mod3(startT)]]);
    let pending = null, timer = 0, longPressed = false, keyHandledAt = 0;

    const label = (target) => { btn.setAttribute("aria-label", T(loc, `Domaine : ${o.hosts[D[target]]}. Suivant : ${o.hosts[D[mod3(target + 1)]]}. Maj+Entrée : précédent.`, `Domain: ${o.hosts[D[target]]}. Next: ${o.hosts[D[mod3(target + 1)]]}. Shift+Enter: previous.`)); };
    label(cur);

    function preview(dir) {                                                      // WM-02: never blocks; retargets from the current state
      if (M.mode === "off") rig.setT(Math.round(rig.state.target) + dir); else rig.step(dir);
      const target = mod3(Math.round(rig.state.target));
      tw.write(o.hosts[D[target]]);
      clearTimeout(timer);
      if (target === cur) { pending = null; hint.hidden = true; live.textContent = T(loc, `Vous restez sur ${o.hosts[D[cur]]}.`, `Staying on ${o.hosts[D[cur]]}.`); return; }
      pending = { target, dir };
      M.prefetch(o.homes[D[target]]);                                            // opportunistic fetch during the brief 48 ms acknowledgement
      // The 48 ms retarget window is intentionally not presented as a one-second wait.
      hint.hidden = true;
      live.textContent = T(loc, `Navigation vers ${o.hosts[D[target]]}.`, `Navigating to ${o.hosts[D[target]]}.`);
      timer = setTimeout(commit, delay);
    }
    function cancel() {
      if (!pending) return;
      clearTimeout(timer); pending = null; hint.hidden = true;
      rig.goTo(cur); tw.write(o.hosts[D[cur]]);
      live.textContent = T(loc, `Annulé. Vous restez sur ${o.hosts[D[cur]]}.`, `Cancelled. Staying on ${o.hosts[D[cur]]}.`);
    }
    function commit() {
      if (!pending) return;
      const { target, dir } = pending; pending = null; hint.hidden = true;
      api.depart(o.homes[D[target]], target, dir);
    }

    // ── pointer: left = clockwise, right = counter-clockwise, long press (touch) = counter-clockwise
    let lastDown = null;
    btn.addEventListener("pointerdown", (e) => { lastDown = { type: e.pointerType, button: e.button, at: performance.now() }; longPressed = false; if (e.button === 0 || e.button === 2) rig.press(true); });
    btn.addEventListener("pointerup", (e) => {
      rig.press(false);
      if (longPressed) { longPressed = false; return; }                          // the long press already turned the cube
      if (e.button === 0) preview(+1); else if (e.button === 2) preview(-1);
    });
    btn.addEventListener("contextmenu", (e) => {                                 // suppressed on the cube only (D13)
      e.preventDefault();
      const recent = lastDown && performance.now() - lastDown.at < 1500;
      if (recent && lastDown.type === "mouse") return;                           // mouse right button: handled on pointerup
      if (recent && lastDown.type !== "mouse") { longPressed = true; rig.press(false); preview(-1); return; }   // touch/pen long press
      preview(-1);                                                               // keyboard Menu key / Shift+F10
    });
    // ── keyboard: Enter/Space = next, Shift+Enter/Space = previous
    btn.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); keyHandledAt = performance.now(); preview(e.shiftKey ? -1 : +1); }
    });
    // assistive-technology activation (no key or pointer event): next
    btn.addEventListener("click", (e) => { if (e.detail === 0 && performance.now() - keyHandledAt > 300) preview(+1); });
    btn.addEventListener("pointerenter", () => rig.hover(true)); btn.addEventListener("pointerleave", () => { rig.hover(false); rig.press(false); });
    btn.addEventListener("focus", () => rig.hover(true)); btn.addEventListener("blur", () => rig.hover(false));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && pending) { e.preventDefault(); cancel(); } });

    const api = {
      rig, tw, get pending() { return pending; }, cancel,
      // Native browser navigation; no asynchronous screen-cover stage.
      depart(url) {
        M.noteNavigation();
        M.handoff.go(url, { from: o.domain, t: cur, mode: M.chosen, chain: M.chain() });
      },
      // navigation started by a link (Spine, palette): turn + type while retiring, then hop
      navigate(url, domain) {
        const target = D.indexOf(domain);
        if (target < 0 || target === cur) { location.assign(url); return; }
        rig.goTo(target); tw.write(o.hosts[D[target]]);
        this.depart(url, target, mod3(target - cur) === 1 ? 1 : -1);
      },
    };

    // ── arrival
    if (incoming) {
      const from = D.indexOf(incoming.from), fwd = mod3(cur - from) === 1, dir = fwd ? 1 : -1;
      const r = btn.getBoundingClientRect(), origin = { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      const finished = (M.arrival || M.arc(o.blocks ? o.blocks() : [], {
        origin, dir, phase: "in"
      })).finished;
      document.documentElement.removeAttribute("data-g6-arriving");
      rig.goTo(cur); tw.write(o.hosts[o.domain]);
      finished.then(() => {
        const main = document.querySelector("main");
        if (main) { if (!main.hasAttribute("tabindex")) main.tabIndex = -1; main.focus({ preventScroll: true }); }     // WM-07
        live.textContent = T(loc, `Vous êtes sur ${o.hosts[o.domain]}.`, `You are on ${o.hosts[o.domain]}.`);
      });
    }
    return api;
  }

  window.G6Bar = { mount, typewriter, favicon };
})();
