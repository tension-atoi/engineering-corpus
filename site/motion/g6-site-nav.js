/* GNU6 Site Navigation v1 — source-owned shared browser adapter.
 * Upstream: gnu6-design. Real native destinations only; planned product sites
 * may have an identity but must not be exposed as working navigation.
 * Uses the ratified G6Motion / G6Rig / G6Bar components, never reimplements
 * their animation algorithms or relaxes owner-origin isolation.
 */
(() => {
  "use strict";
  const motion = window.G6Motion;
  const bar = window.G6Bar;
  const rigFactory = window.G6Rig;
  if (!motion || !bar || !rigFactory || !window.GNU6_RIG) return;
  const root = document.documentElement;
  const domain = root.dataset.g6Domain;
  if (!["live", "docs"].includes(domain)) return;
  const host = document.querySelector("[data-g6-site-nav]");
  if (!host || host.dataset.g6SiteNavReady) return;
  const cube = host.querySelector(".g6-bar__cube");
  const rigHost = host.querySelector(".g6-bar__rig");
  const twHost = host.querySelector(".g6-tw");
  const status = host.querySelector("[role='status']");
  const switcher = document.querySelector("[data-g6-site-motion]");
  if (!cube || !rigHost || !twHost || !status || !switcher) return;
  host.dataset.g6SiteNavReady = "true";
  const locale = () => root.lang === "en" ? "en" : "fr";
  const hosts = {live:"gnu6.live",docs:"docs.gnu6.live"};
  const next = domain === "live" ? "docs" : "live";
  // Each service's native anchor is the ONLY destination authority. React
  // updates href on language changes; the shared adapter never hardcodes or
  // caches a second endpoint. Validate fail-closed before visual handoff.
  const destination = () => {
    const link = document.querySelector('a[data-g6-nav-destination="' + next + '"]');
    if (!link || !(link instanceof HTMLAnchorElement)) return null;
    let url;
    try { url = new URL(link.href, location.href); }
    catch { return null; }
    if (url.protocol !== "https:" || url.hostname !== hosts[next]
      || url.username || url.password || url.port) return null;
    return url.href;
  };
  const currentT = domain === "live" ? 0 : 1;
  const incoming = motion.incoming;
  const startT = incoming ? incoming.t : currentT;
  const rig = rigFactory.create(rigHost, window.GNU6_RIG, {
    t0:startT, label:hosts[domain], sdf:"/motion/glyph-sdf.png",
    shouldSnap:()=>motion.mode !== "full",
  });
  const writer = bar.typewriter(twHost, incoming?.from === next ? hosts[next] : hosts[domain]);
  let queued = false;
  let operation = 0;
  const t = (fr,en)=>locale()==="fr"?fr:en;
  const updateChoice = () => {
    const effective = motion.mode;
    for(const input of switcher.querySelectorAll("input[name='g6-site-mode']")) {
      input.checked = input.value === effective;
      input.disabled = matchMedia("(prefers-reduced-motion: reduce)").matches;
    }
    switcher.dataset.g6Mode = effective;
  };
  const stopNavigation = () => {
    queued = false;
    operation++;
    rig.goTo(currentT);
    writer.set(hosts[domain]);
    status.textContent = t("Navigation annulée.","Navigation cancelled.");
  };
  function navigate() {
    if (queued) return;
    if (!destination()) {
      status.textContent = t("Destination indisponible.", "Destination unavailable.");
      return;
    }
    queued = true;
    const ticket = ++operation;
    const targetT = next === "docs" ? 1 : 0;
    const delta = targetT - currentT;
    if (motion.mode === "off") rig.setT(targetT);
    else rig.step(delta);
    writer.write(hosts[next], {
      fromDomain:domain, toDomain:next, erase:38, type:46,
    });
    status.textContent = t("Ouverture de " + hosts[next], "Opening " + hosts[next]);
    // 48 ms acknowledgment, no pause for the full titlewriter sequence.
    const commit = () => {
      if (!queued || ticket !== operation) return;
      motion.noteNavigation();
      const go=()=>{
        if(ticket !== operation || !queued) return;
        const href = destination();
        if(!href){ stopNavigation(); return; }
        motion.handoff.go(href, {
          from:domain,t:currentT,mode:motion.chosen,chain:motion.chain(),
        });
      };
      go();
    };
    setTimeout(commit, 48);
  }
  cube.setAttribute("aria-label",t("Aller vers "+hosts[next],"Go to "+hosts[next]));
  cube.addEventListener("click", navigate);
  // Qualified native links share the cube's visual handoff. Modified clicks
  // retain standard browser semantics; do not intercept unrelated anchors.
  document.querySelectorAll('a[data-g6-nav-destination]').forEach((link)=>{
    link.addEventListener("click",(event)=>{
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey
        || link.hasAttribute("download") || link.target === "_blank") return;
      const target = link.dataset.g6NavDestination;
      if (target !== next) return;
      const intended = new URL(link.href);
      const approved = destination();
      if (!approved || intended.origin !== new URL(approved).origin) return;
      event.preventDefault();
      navigate();
    });
  });
  cube.addEventListener("pointerenter",()=>rig.hover(true));
  cube.addEventListener("pointerleave",()=>rig.hover(false));
  cube.addEventListener("focus",()=>rig.hover(true));
  cube.addEventListener("blur",()=>rig.hover(false));
  document.addEventListener("keydown",(event)=>{
    if(event.key==="Escape" && queued) {
      event.preventDefault();
      stopNavigation();
      // A pending bridge Promise is invalidated by the monotonic operation ID.
    }
  });
  switcher.addEventListener("change",(event)=>{
    if(event.target?.matches("input[name='g6-site-mode']")) {
      motion.setMode(event.target.value);
    }
  });
  motion.on(updateChoice);
  updateChoice();
  // A real document becomes active only when parsed and its own navbar is ready.
  // This is NOT cross-origin DOM persistence or a proof of GPU-first-frame paint.
  if(incoming) {
    rig.goTo(currentT);
    writer.write(hosts[domain], {
      fromDomain:incoming.from,toDomain:domain,erase:38,type:46,
    });
  } else {
    rig.setT(currentT);
    writer.set(hosts[domain]);
  }
  status.textContent = t("Surface active : "+hosts[domain],"Active surface: "+hosts[domain]);
  window.G6SiteNav = {domain, get ready(){return true;}, get eligible(){return ["live","docs"];},navigate};
})();