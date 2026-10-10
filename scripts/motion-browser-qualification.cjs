// Bounded local qualification, no production writes or cross-domain framing.
const path=require("node:path");
const modules=process.env.PLAYWRIGHT_ROOT || process.cwd();
const {chromium}=require(path.join(modules,"node_modules/playwright"));
const Axe=require(path.join(modules,"node_modules/@axe-core/playwright")).default;
const fs=require("fs");
const base=process.env.MOTION_DOCS_BASE_URL || "http://127.0.0.1:4702";
const routes=["/fr/hub.html","/en/hub.html","/fr/projects/gnosix/index.html","/en/api.html"];
(async()=>{
const b=await chromium.launch({args:["--use-gl=swiftshader","--enable-unsafe-swiftshader"]}),out=[];
try{
 for(const path of routes)for(const viewport of ["desktop","mobile"])for(const scheme of ["light","dark"]){
 const c=await b.newContext({viewport:viewport==="mobile"?{width:390,height:780}:{width:1365,height:780},colorScheme:scheme});
 const p=await c.newPage(),errors=[];
 p.on("pageerror",e=>errors.push(e.message));
 p.on("console",m=>m.type()==="error"&&errors.push(m.text()));
 const response=await p.goto(base+path,{waitUntil:"networkidle"});if(response.status()!==200)throw Error(path+" HTTP "+response.status());
 const state=await p.evaluate(()=>{const brand=document.querySelector(".g6-sysbar .g6-brand"),name=brand?.querySelector(".g6-brand__word"),favicon=document.querySelector('link[rel="icon"]');
 return {name:name?.textContent,href:brand?.getAttribute("href"),icon:favicon?.getAttribute("href"),iconSize:favicon?.getAttribute("sizes"),color:getComputedStyle(name).color,
 token:getComputedStyle(document.documentElement).getPropertyValue("--g6-accent-labs-text").trim(),
 motionLinks:[...document.querySelectorAll('a[href="https://gnu6.live/motion/index.html"]')].length,
 frameCount:document.querySelectorAll("iframe").length,
 width:document.documentElement.scrollWidth,viewport:innerWidth};});
 if(state.name!=="docs.gnu6.live"||!state.href.endsWith("/hub.html")||!state.icon.endsWith("gnuinlabs-64.png")||
 state.iconSize!=="64x64"||state.motionLinks!==2||state.frameCount!==0||state.width>state.viewport+1)
 throw Error("contract "+JSON.stringify({path,viewport,scheme,state}));
 const icon=await p.evaluate(async()=>{const img=new Image();img.src=document.querySelector('link[rel="icon"]').href;await img.decode();return img.naturalWidth});
 if(icon!==64)throw Error("favicon decode="+icon);
 const violations=(await new Axe({page:p}).withTags(["wcag2a","wcag2aa","wcag21aa","wcag22aa"]).analyze()).violations.map(x=>x.id);
 if(errors.length||violations.length)throw Error("quality "+JSON.stringify({path,viewport,scheme,errors,violations}));
 out.push({path,viewport,scheme,state,axeViolations:violations,consoleErrors:errors});console.log("DOCS_PASS",path,viewport,scheme);
 await c.close();
 }
}finally{await b.close();fs.writeFileSync(process.env.MOTION_DOCS_PROOF || "/tmp/gnu6-motion-docs-browser.json",JSON.stringify({at:new Date().toISOString(),cases:out},null,2));}
console.log("QUALIFIED",out.length,"/16");if(out.length!==16)process.exit(1);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
