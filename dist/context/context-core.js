// packages/gnu6-context-core/src/observations.ts
var compact = (value) => (value ?? "").trim().replace(/\s+/g, " ").slice(0, 160);
var native = (el) => Boolean(
  el.closest(
    'input,textarea,select,[contenteditable]:not([contenteditable="false"]),[role="textbox"],[data-g6-native-context],[data-scenelab-stage],.scenelab-context-menu,iframe'
  )
);
function contextFacts(target) {
  const el = target instanceof Element ? target : null;
  if (!el || native(el)) return null;
  const link = el.closest("a[href]");
  const image = el.closest("img[src]");
  const button = el.closest('button,[role="button"]');
  const heading = el.closest("h1,h2,h3,h4,h5,h6");
  const kind = link ? "link" : image ? "image" : button ? "button" : heading ? "heading" : "document";
  const selection = window.getSelection();
  const selected = selection?.rangeCount && selection.getRangeAt(0).intersectsNode(el) ? selection.toString().slice(0, 8192) : "";
  const section = heading?.id ? new URL("#" + encodeURIComponent(heading.id), document.baseURI).href : void 0;
  return {
    kind: selected && kind === "document" ? "selection" : kind,
    pageUrl: location.href,
    ...selected ? { selection: selected } : {},
    ...link?.href ? { link: link.href } : {},
    ...image?.currentSrc || image?.src ? { image: image.currentSrc || image.src } : {},
    ...section ? { section } : {},
    label: compact(
      link?.textContent || image?.alt || button?.getAttribute("aria-label") || button?.textContent || heading?.textContent || document.title
    )
  };
}

// packages/gnu6-context-core/src/policy.ts
var compact2 = (value) => (value ?? "").trim().slice(0, 160);
var allowed = (candidate) => {
  if (!candidate) return null;
  try {
    const url = new URL(candidate);
    return ["https:", "http:"].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
};
function resolveContext(facts) {
  const actions = [];
  const addCopy = (id, raw) => {
    const value = raw?.trim();
    if (value) actions.push({ id, capability: "clipboard:write", value: value.slice(0, 8192) });
  };
  const selection = facts.selection?.trim().slice(0, 8192);
  if (selection) addCopy("copy-selection", selection);
  const link = allowed(facts.link), image = allowed(facts.image), section = allowed(facts.section), page = allowed(facts.pageUrl);
  if (link) {
    addCopy("copy-link", link);
    actions.push({ id: "open-link", capability: "navigation:open", value: link });
  } else if (image) {
    addCopy("copy-image-url", image);
    actions.push({ id: "open-image", capability: "navigation:open", value: image });
  } else if (facts.kind === "heading" && section) addCopy("copy-section", section);
  else if (facts.kind === "button" || facts.kind === "spatial")
    addCopy("copy-label", compact2(facts.label || facts.subjectId));
  if (page) addCopy("copy-page", page);
  const labels = {
    selection: "Selection",
    link: "Link",
    image: "Media",
    button: "Control",
    heading: "Section",
    spatial: "Spatial subject",
    document: "Page"
  };
  return {
    kind: facts.kind,
    label: compact2(facts.label) || labels[facts.kind],
    actions,
    source: facts.kind === "spatial" && facts.provenance === "in.gnu6" ? "in.gnu6" : "dom"
  };
}

// packages/gnu6-context-core/src/handoff.ts
var HOSTS = { live: "gnu6.live", docs: "docs.gnu6.live" };
function domainFor(url) {
  if (url.protocol !== "https:" || url.username || url.password || url.port) return null;
  return url.hostname === HOSTS.live ? "live" : url.hostname === HOSTS.docs ? "docs" : null;
}
function crossDomainPlan(sourceHref, destinationHref) {
  try {
    const source = new URL(sourceHref);
    const target = new URL(destinationHref, source);
    const from = domainFor(source);
    const to = domainFor(target);
    if (!from || !to || from === to) return null;
    return { from, to, target: target.href, fromT: from === "live" ? 0 : 1 };
  } catch {
    return null;
  }
}
var pending = false;
var operation = 0;
function beginCrossDomainHandoff(href, motion, anchor = null, currentHref = location.href) {
  const plan = crossDomainPlan(currentHref, href);
  if (!plan || !motion || motion.domain !== plan.from) return false;
  if (pending) return true;
  if (!motion.handoff?.go || !motion.bridge?.cover) return false;
  pending = true;
  const ticket = ++operation;
  const r = anchor?.getBoundingClientRect();
  const point = r ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : { x: 22, y: 22 };
  const state = { from: plan.from, t: plan.fromT, mode: motion.chosen, chain: motion.chain() };
  motion.noteNavigation();
  const cleanup = () => {
    document.documentElement.removeAttribute("data-g6-bridge");
    document.documentElement.style.removeProperty("--g6-bridge-x");
    document.documentElement.style.removeProperty("--g6-bridge-y");
    pending = false;
    ++operation;
  };
  const cancel = (event) => {
    if (event.key !== "Escape") return;
    event.preventDefault();
    document.removeEventListener("keydown", cancel, true);
    cleanup();
  };
  document.addEventListener("keydown", cancel, true);
  const accepted = pending;
  void (motion.bridge.active ? motion.bridge.cover(point) : Promise.resolve()).then(() => {
    document.removeEventListener("keydown", cancel, true);
    if (!pending || ticket !== operation) return;
    motion.handoff.go(plan.target, state);
  }).catch(() => {
    document.removeEventListener("keydown", cancel, true);
    if (!pending || ticket !== operation) return;
    cleanup();
    location.assign(plan.target);
  });
  return accepted;
}
export {
  beginCrossDomainHandoff,
  contextFacts,
  crossDomainPlan,
  resolveContext
};
