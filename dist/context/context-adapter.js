import { contextFacts, resolveContext, beginCrossDomainHandoff } from "./context-core.js";
const labels = {
  fr: {selection:"Sélection",link:"Lien",image:"Média",button:"Contrôle",heading:"Section",document:"Page",spatial:"Sujet spatial"},
  en: {selection:"Selection",link:"Link",image:"Media",button:"Control",heading:"Section",document:"Page",spatial:"Spatial subject"}
};
const actions = {
  fr: {"copy-selection":"Copier la sélection","copy-link":"Copier l’adresse du lien","open-link":"Ouvrir le lien","copy-image-url":"Copier l’adresse du média","open-image":"Ouvrir le média","copy-label":"Copier le libellé","copy-section":"Copier le lien de section","copy-page":"Copier le lien de la page"},
  en: {"copy-selection":"Copy selection","copy-link":"Copy link address","open-link":"Open link","copy-image-url":"Copy media address","open-image":"Open media","copy-label":"Copy label","copy-section":"Copy section link","copy-page":"Copy page link"}
};
const locale = document.documentElement.lang === "en" ? "en" : "fr";
let menu = null, restore = null, generation = 0;
const status = document.createElement("div");
status.className = "g6-context-plane__announcement";
status.setAttribute("role","status");
status.setAttribute("aria-live","polite");
document.body.append(status);
function close(returnFocus=false) {
  if (!menu) return;
  menu.remove(); menu = null;
  if (returnFocus && restore?.isConnected) restore.focus({preventScroll:true});
}
function open(target,x,y) {
  const facts = contextFacts(target);
  if (!facts) return false;
  const resolution = resolveContext(facts);
  if (!resolution.actions.length) return false;
  close();
  restore = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  const box=document.createElement("div");
  box.className="g6-context-plane";
  box.dataset.g6ContextMenu="";
  box.dataset.g6ContextKind=resolution.kind;
  box.dataset.g6ContextSource=resolution.source;
  box.setAttribute("role","menu");
  box.setAttribute("aria-label",labels[locale][resolution.kind]+": "+resolution.label);
  box.tabIndex=-1;
  box.style.left=Math.max(8,Math.min(x,innerWidth-Math.min(320,innerWidth-16)-8))+"px";
  box.style.top=Math.max(8,Math.min(y,innerHeight-Math.min(innerHeight-16,56+resolution.actions.length*40)-8))+"px";
  const header=document.createElement("div");header.className="g6-context-plane__heading";
  const kind=document.createElement("span");kind.textContent=labels[locale][resolution.kind];
  const subject=document.createElement("span");subject.className="g6-context-plane__subject";subject.title=resolution.label;subject.textContent=resolution.label;
  header.append(kind,subject);box.append(header);
  const rows=document.createElement("div");rows.className="g6-context-plane__rows";
  for(const action of resolution.actions) {
    const el=document.createElement(action.capability==="navigation:open"?"a":"button");
    el.setAttribute("role","menuitem");
    if(el.tagName==="A") el.href=action.value;
    else el.type="button";
    const label=document.createElement("span");label.textContent=actions[locale][action.id];
    const arrow=document.createElement("span");arrow.setAttribute("aria-hidden","true");arrow.textContent="↗";el.append(label,arrow);
    el.addEventListener("click",async ev=>{
      if(action.capability==="navigation:open"){close();return;}
      ev.preventDefault();
      try{await navigator.clipboard.writeText(action.value);status.textContent=locale==="fr"?"Copié":"Copied";}
      catch{status.textContent=locale==="fr"?"Copie impossible : Maj + clic droit pour le menu natif.":"Copy unavailable: Shift + right-click for native menu.";}
      close(true);
    });
    rows.append(el);
  }
  box.append(rows);
  const footer=document.createElement("div");footer.className="g6-context-plane__footer";footer.textContent="GNU6 / CONTEXT · 02";box.append(footer);
  box.addEventListener("keydown",ev=>{
    const items=[...box.querySelectorAll('[role="menuitem"]')];
    const i=items.indexOf(document.activeElement);
    const next=ev.key==="ArrowDown"?(i+1)%items.length:ev.key==="ArrowUp"?(i-1+items.length)%items.length:ev.key==="Home"?0:ev.key==="End"?items.length-1:-1;
    if(next>=0){ev.preventDefault();items[next].focus();}
    if(ev.key==="Tab")close();
    if(ev.key==="Escape"){ev.preventDefault();ev.stopPropagation();close(true);}
  });
  document.body.append(box);menu=box;generation++;
  rows.querySelector('[role="menuitem"]')?.focus({preventScroll:true});
  return true;
}
document.addEventListener("contextmenu",ev=>{
  if(ev.defaultPrevented||ev.shiftKey||ev.target?.closest?.("[data-g6-context-menu]"))return;
  if(open(ev.target,ev.clientX,ev.clientY))ev.preventDefault();
});
document.addEventListener("keydown",ev=>{
  if(ev.key==="Escape"){if(menu){ev.preventDefault();close(true);}return;}
  if(ev.defaultPrevented)return;
  if(ev.key!=="ContextMenu"&&!(ev.key==="F10"&&ev.shiftKey))return;
  const el=document.activeElement;
  if(!(el instanceof HTMLElement))return;
  const rect=el.getBoundingClientRect();
  if(open(el,Math.max(8,rect.left+16),Math.max(8,rect.top+Math.min(rect.height,28))))ev.preventDefault();
});
document.addEventListener("pointerdown",ev=>{if(!ev.target?.closest?.("[data-g6-context-menu]"))close();});
for(const kind of ["wheel","touchmove","resize","popstate","hashchange"]){
  window.addEventListener(kind,()=>close(),{passive:true});
}

// Native anchors are the URL authority. Only ordinary user clicks to the
// exact peer GNU6 origin enter the existing geometric handoff; all other
// destinations preserve browser semantics, including modifier keys.
document.addEventListener("click", event => {
  if (event.defaultPrevented || event.button !== 0 ||
      event.metaKey || event.ctrlKey || event.altKey || event.shiftKey ||
      !(event.target instanceof Element)) return;
  const anchor = event.target.closest("a[href]");
  if (!anchor || anchor.hasAttribute("download") ||
      (anchor.target && anchor.target !== "_self")) return;
  if (beginCrossDomainHandoff(
    anchor.href, window.G6Motion, document.querySelector(".g6-brand")
  )) event.preventDefault();
});
