/* GNU6 Shared Spine v1: progressive enhancement only; no secret or service requests. */
(()=>{"use strict";
const D=document,shell=D.querySelector(".g6-spine-shell"),map=window.GNU6_MAP;
if(!shell||!map||!Array.isArray(map.pages))return;
const nav=shell.querySelector(".g6-spine"),mobile=D.querySelector("[data-g6-spine-toggle]");
const locale=D.documentElement.lang==="en"?"en":"fr";
const txt=(fr,en)=>locale==="fr"?fr:en;
const norm=s=>String(s).normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
const safe=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const links=map.pages.filter(p=>p.locale===locale && (p.domain==="docs"||p.domain==="live"));
function setNav(open){if(!nav||!mobile)return;nav.classList.toggle("is-open",open);mobile.setAttribute("aria-expanded",String(open));if(open)nav.querySelector("a,button")?.focus();else mobile.focus();}
mobile?.addEventListener("click",()=>setNav(!nav.classList.contains("is-open")));
const overlay=D.createElement("section");overlay.className="g6-spine-overlay";overlay.hidden=true;
overlay.innerHTML='<div class="g6-spine-dialog" role="dialog" aria-modal="true" aria-labelledby="g6-spine-title"><div class="g6-spine-dialog__top"><h2 id="g6-spine-title"></h2><button type="button" data-g6-dismiss aria-label="'+txt("Fermer","Close")+'">×</button></div><label for="g6-spine-query">'+txt("Rechercher les pages GNU6","Search GNU6 pages")+'</label><input id="g6-spine-query" type="search" autocomplete="off" spellcheck="false"><p class="g6-spine__result-count" role="status"></p><ol class="g6-spine__results"></ol></div>';
/* Mount lazily after hydration; React Router hydrates the document root. */
const input=overlay.querySelector("input"),res=overlay.querySelector("ol"),count=overlay.querySelector("[role=status]"),heading=overlay.querySelector("h2");
let opened=false,restore=null;
function render(){const q=norm(input.value.trim());const rows=links.filter(p=>!q||norm(p.title+" "+p.path+" "+(p.sections||[]).map(s=>s.title).join(" ")).includes(q)).slice(0,75);res.innerHTML=rows.map(p=>'<li><a href="'+safe(map.origins[p.domain]+p.path)+'"><strong>'+safe(p.title)+'</strong><small>'+safe(p.domain)+" · "+safe(p.path)+'</small></a></li>').join("");count.textContent=rows.length+" "+txt("résultats","results");}
function close(){if(!opened)return;opened=false;overlay.hidden=true;D.body.classList.remove("g6-spine-modal-open");(restore?.isConnected?restore:D.querySelector("[data-g6-open-search]"))?.focus();}
function show(atlas=false){if(!overlay.isConnected)D.body.append(overlay);restore=D.activeElement;opened=true;overlay.hidden=false;overlay.dataset.kind=atlas?"atlas":"search";heading.textContent=atlas?txt("Atlas · explorer GNU6","Atlas · explore GNU6"):txt("Recherche globale","Global search");D.body.classList.add("g6-spine-modal-open");input.value="";render();input.focus();}
input.addEventListener("input",render);
overlay.addEventListener("click",ev=>{if(ev.target===overlay||ev.target.closest("[data-g6-dismiss]"))close();});
D.addEventListener("click",ev=>{if(ev.target.closest("[data-g6-open-atlas]")){ev.preventDefault();show(true);}else if(ev.target.closest("[data-g6-open-search]")){ev.preventDefault();show(false);}});
D.addEventListener("keydown",ev=>{
if(ev.key==="Escape"){if(opened){ev.preventDefault();close();}else if(nav?.classList.contains("is-open"))setNav(false);return;}
if(opened&&ev.key==="Tab"){const focus=[...overlay.querySelectorAll("input,button,a[href]")].filter(el=>el.getClientRects().length);const i=focus.indexOf(D.activeElement);if(ev.shiftKey&&i===0){ev.preventDefault();focus.at(-1).focus();}else if(!ev.shiftKey&&i===focus.length-1){ev.preventDefault();focus[0].focus();}}
if((ev.ctrlKey||ev.metaKey)&&ev.key.toLowerCase()==="k"){ev.preventDefault();opened?input.focus():show();}
else if(ev.key==="/"&&!opened&&!/input|textarea|select/i.test(D.activeElement?.tagName||"")&&!D.activeElement?.isContentEditable){ev.preventDefault();show();}
});
/* aria-current is rendered by each authoritative site adapter. */
})();
