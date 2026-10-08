/* Execute one phase via BrowserOS neo run; phase is supplied by the runner. */
const base = 'http://127.0.0.1:18766';
const locationBase = base;
const mine = (await browser.pages.list()).find(x => x.ownership === 'mine' && x.url.startsWith(base));
const p = mine ? browser.page(mine.pageId) : await browser.open(base + '/fr/chapters/01-mandate.html');
const check = (ok, name) => { if (!ok) throw new Error(name); };
const value = async (fn, arg) => (await p.evaluate(fn, arg)).value;
const result = {phase, checks: []};
const pass = name => result.checks.push({name, result: 'PASS'});
if (phase === 'desktop') {
  await p.cdp('Emulation.setDeviceMetricsOverride', JSON.stringify({width:1440,height:1000,deviceScaleFactor:1,mobile:false}));
  await p.goto(base + '/fr/chapters/01-mandate.html');
  await value(() => { window.__studyBackup = localStorage.getItem('engineering-corpus:study:v0.1'); localStorage.removeItem('engineering-corpus:study:v0.1'); });
  const backup = await value(() => window.__studyBackup);
  await p.reload(); await p.waitForSelector('[data-progress-id][aria-pressed]');
  let s = await p.snapshot({mode:'interactive'});
  await p.fill(s.refs.find(x => x.role === 'searchbox').ref, 'autorite');
  check(await value(() => [...document.querySelectorAll('[data-search]')].filter(x=>!x.hidden).length) === 1, 'accent insensitive search'); pass('accent insensitive search');
  await p.fill(s.refs.find(x => x.role === 'searchbox').ref, 'no-such-chapter');
  check((await value(() => document.querySelector('[data-search-status]').textContent)).includes('Aucun'), 'empty search status'); pass('empty search status');
  await p.fill(s.refs.find(x => x.role === 'searchbox').ref, '');
  check(await value(() => [...document.querySelectorAll('[data-search]')].filter(x=>!x.hidden).length) === 13, 'search reset'); pass('search reset');
  s = await p.snapshot({mode:'interactive'});
  await p.click(s.refs.find(x => x.name === 'Marquer comme étudié').ref);
  check(await value(() => document.querySelector('[data-progress-meter]').value) === 1, 'semantic progress value'); pass('semantic progress value');
  await p.goto(base + '/fr/chapters/01-mandate.html#section-2');
  s = await p.snapshot({mode:'interactive'});
  await p.click(s.refs.find(x => x.name === 'English ↗').ref); await p.waitForSelector('[data-progress-id][aria-pressed]');
  check(await value(() => location.pathname + location.hash) === '/en/chapters/01-mandate.html#section-2', 'FR EN context');
  check(await value(() => document.querySelector('[data-progress-id]').getAttribute('aria-pressed')) === 'true', 'FR EN state'); pass('FR EN context and state');
  for (const stored of ['null','[]','"text"','{broken']) {
    await value(x => localStorage.setItem('engineering-corpus:study:v0.1',x),stored); await p.reload(); await p.waitForSelector('[data-progress-id][aria-pressed]');
    check(await value(() => document.querySelector('[data-progress-id]').getAttribute('aria-pressed')) === 'false', 'corrupt storage '+stored);
  }
  pass('corrupt storage variants');
  await value(() => { Object.defineProperty(Storage.prototype,'setItem',{configurable:true,value(){throw new Error('blocked storage')}}); });
  s=await p.snapshot({mode:'interactive'}); await p.click(s.refs.find(x => x.name === 'Mark as studied').ref);
  check((await value(() => document.querySelector('[data-storage-status]').textContent)).includes('unavailable'), 'blocked storage notice');pass('blocked storage notice');
  await p.reload(); await p.waitForSelector('[data-progress-id][aria-pressed]');
  await p.goto(base + '/fr/chapters/01-mandate.html');
  s=await p.snapshot({mode:'interactive'}); await p.focus(s.refs.find(x => x.name === 'Aller au contenu').ref); await p.press('Enter');
  check(await value(() => document.activeElement.id) === 'content', 'skip link focus');pass('skip link focus');
  result.snapshot=await p.snapshot({mode:'interactive'});
  result.screenshot=await p.cdp('Page.captureScreenshot',JSON.stringify({format:'png'}));
  await value(old => old === null ? localStorage.removeItem('engineering-corpus:study:v0.1') : localStorage.setItem('engineering-corpus:study:v0.1',old),backup);
} else if (phase === 'mobile') {
  await p.cdp('Emulation.setDeviceMetricsOverride', JSON.stringify({width:390,height:844,deviceScaleFactor:1,mobile:true}));
  await p.goto(base + '/fr/labs/03-workspace.html'); await p.waitForSelector('[data-progress-id][aria-pressed]');
  let s=await p.snapshot({mode:'interactive'}); await p.focus(s.refs.find(x=>x.name==='Menu').ref); await p.press('Enter');
  check(await value(()=>document.activeElement.id)==='closeSidebar','mobile opening focus');pass('mobile opening focus');
  await p.press('Shift+Tab');check(await value(()=>document.activeElement.getAttribute('href'))==='/fr/templates.html','mobile focus wrap');pass('mobile focus wrap');
  await p.press('Escape');check(await value(()=>document.activeElement.id)==='toggleSidebar','escape focus return');
  check(await value(()=>document.querySelector('#toggleSidebar').getAttribute('aria-expanded'))==='false','escape state');pass('escape state and focus');
  s=await p.snapshot({mode:'interactive'}); await p.focus(s.refs.find(x=>x.name==='Menu').ref); await p.press('Enter');s=await p.snapshot({mode:'interactive'});
  await p.focus(s.refs.find(x=>x.name==='Fermer le menu').ref); await p.press('Enter');
  check(await value(()=>document.querySelector('#sidebar').classList.contains('open'))===false,'close button');pass('close button');
  check(await value(()=>document.documentElement.scrollWidth <= innerWidth),'mobile overflow');pass('390px overflow');
  result.snapshot=await p.snapshot({mode:'interactive'});
  result.screenshot=await p.cdp('Page.captureScreenshot',JSON.stringify({format:'png'}));
  await p.cdp('Emulation.setDeviceMetricsOverride', JSON.stringify({width:320,height:700,deviceScaleFactor:1,mobile:true}));
  await p.goto(base+'/fr/chapters/03-contract.html');
  check(await value(()=>document.documentElement.scrollWidth<=innerWidth),'320px overflow');pass('320px overflow');
  const point=await value(()=>{const r=document.querySelector('#toggleSidebar').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};});
  await p.cdp('Input.dispatchTouchEvent',JSON.stringify({type:'touchStart',touchPoints:[{x:point.x,y:point.y}]}));
  await p.cdp('Input.dispatchTouchEvent',JSON.stringify({type:'touchEnd',touchPoints:[]}));
  const opened=await p.waitForSelector('#sidebar.open');check(opened.matched,'mobile touch opens menu');pass('mobile touch opens menu');
  await p.press('Escape');

} else if (phase === 'resources') {
  await p.goto(base+'/fr/topologies.html');
  await p.cdp('Network.enable','{}');
  result.resources=await value(()=>performance.getEntriesByType('resource').map(x=>({name:x.name,responseStatus:x.responseStatus})));
  check(result.resources.every(x=>x.name.startsWith(locationBase)), 'same origin resources');
  result.images=await value(()=>[...document.images].map(x=>({src:x.src,loaded:x.complete&&x.naturalWidth>0,alt:x.alt})));
  check(result.images.every(x=>x.loaded&&x.alt),'diagram loading and alt');pass('diagram loading and alt');
  result.screenshot=await p.cdp('Page.captureScreenshot',JSON.stringify({format:'png'}));
  await p.cdp('Network.emulateNetworkConditions',JSON.stringify({offline:true,latency:0,downloadThroughput:0,uploadThroughput:0}));
  result.offline=await value(()=>({text:document.querySelector('h1').textContent,svgLoaded:[...document.images].every(x=>x.complete&&x.naturalWidth>0)}));
  check(result.offline.text==='Topologies'&&result.offline.svgLoaded,'loaded page offline');pass('loaded page offline');
  await p.cdp('Network.emulateNetworkConditions',JSON.stringify({offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1}));
  await p.goto(base+'/unknown-route');
  check((await value(()=>document.querySelector('h1').textContent)).includes('404'),'unknown route');pass('unknown route');
  result.route=await value(()=>({title:document.title,status:performance.getEntriesByType('navigation')[0].responseStatus,links:[...document.querySelectorAll('a')].map(x=>x.pathname)}));
  check(result.route.status===404,'HTTP 404 response');pass('HTTP 404 response');
} else if (phase === 'zoom') {
  await p.cdp('Emulation.setDeviceMetricsOverride',JSON.stringify({width:720,height:1000,deviceScaleFactor:1,mobile:false}));
  await p.goto(base+'/fr/chapters/03-contract.html'); await p.waitForSelector('[data-progress-id][aria-pressed]');
  check(await value(()=>document.documentElement.scrollWidth<=innerWidth),'200% equivalent reflow');pass('720px reflow equivalent to 1440 at 200%');
  await p.cdp('Emulation.setEmulatedMedia',JSON.stringify({features:[{name:'prefers-reduced-motion',value:'reduce'}]}));
  result.motion=await value(()=>({scroll:getComputedStyle(document.documentElement).scrollBehavior,transition:getComputedStyle(document.querySelector('.navlink')).transitionDuration}));
  check(result.motion.scroll==='auto'&&result.motion.transition==='0s','reduced motion');pass('reduced motion');
  result.screenshot=await p.cdp('Page.captureScreenshot',JSON.stringify({format:'png'}));
  await p.cdp('Emulation.setEmulatedMedia',JSON.stringify({features:[]}));
} else if (phase === 'contrast') {
  await p.cdp('Emulation.setDeviceMetricsOverride', JSON.stringify({width:1440,height:1000,deviceScaleFactor:1,mobile:false}));
  await p.goto(base+'/fr/chapters/01-mandate.html');
  result.contrasts=await value(()=>{
    const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
    const luminance=c=>c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
    return ['.nav-duration','.nav-number','.prose p','.eyebrow','.status','.study-button','footer','.sidebar input'].map(selector=>{
      const node=document.querySelector(selector),style=getComputedStyle(node);let parent=node,bg;
      while(parent){const color=rgb(getComputedStyle(parent).backgroundColor);if(color.length===3||color[3]===1){bg=color;break;}parent=parent.parentElement;}
      const a=luminance(rgb(style.color)),b=luminance(bg||[11,15,14]);return {selector,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),color:style.color,background:bg};
    });
  });
  check(result.contrasts.every(x=>x.ratio>=4.5),'text contrast sample');pass('text contrast sample >=4.5');
  result.statusStyles=await value(()=>[...document.querySelectorAll('.top-status,.status,.time-tag')].map(x=>({radius:getComputedStyle(x).borderRadius,border:getComputedStyle(x).borderTopWidth})));
  check(result.statusStyles.every(x=>x.radius==='0px'&&x.border==='0px'),'no status capsules');pass('no status capsules');
} else if (phase.startsWith('pages:')) {
  result.pages=[];
  for (const path of phase.slice(6).split(',')) {
    await p.goto(base+'/'+path);
    const info=await value(()=>({path:location.pathname,lang:document.documentElement.lang,h1:document.querySelectorAll('h1').length,
      overflow:document.documentElement.scrollWidth>innerWidth,resources:performance.getEntriesByType('resource').map(x=>x.name)}));
    check(info.h1===1&&!info.overflow,'page semantics/overflow '+path);
    check(info.resources.every(x=>x.startsWith(locationBase)),'resources '+path);result.pages.push(info);
  }
  pass('bounded page sample');
}
return result;
