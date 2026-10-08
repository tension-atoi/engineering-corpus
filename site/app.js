/* Private-to-browser study state. No network, telemetry or privileged actions. */
(() => {
  const lang = document.body.dataset.locale || 'fr';
  const key = 'engineering-corpus:study:v0.1';
  const ids = JSON.parse(document.body.dataset.studyIds || '[]');
  let state = {};
  const unavailable = () => { const node = document.querySelector('[data-storage-status]'); if (node) node.textContent = lang === 'fr' ? 'Stockage indisponible : progression pour cette page seulement.' : 'Storage unavailable: progress for this page only.'; };
  try { const stored = JSON.parse(localStorage.getItem(key) || '{}'); if (stored && typeof stored === 'object' && !Array.isArray(stored)) for (const id of ids) state[id] = stored[id] === true; }
  catch (_) { state = {}; unavailable(); }
  const save = () => { try { localStorage.setItem(key, JSON.stringify(state)); } catch (_) { unavailable(); } };
  const update = () => {
    const done = ids.filter(id => state[id]).length;
    const text = document.querySelector('[data-progress-text]');
    const bar = document.querySelector('[data-progress-meter]');
    if (text) text.textContent = `${done} / ${ids.length}`;
    if (bar) bar.value = done;
    const button = document.querySelector('[data-progress-id]');
    if (button) {
      const checked = Boolean(state[button.dataset.progressId]);
      button.classList.toggle('done', checked);
      button.setAttribute('aria-pressed', String(checked));
      button.textContent = checked ? (lang === 'fr' ? '✓ Étudié — annuler' : '✓ Studied — undo') : button.dataset.defaultLabel;
    }
  };
  const button = document.querySelector('[data-progress-id]');
  if (button) button.addEventListener('click', () => { const id = button.dataset.progressId; state[id] = !state[id]; save(); update(); });
  const search = document.querySelector('#chapterSearch');
  if (search) search.addEventListener('input', () => {
    const value = search.value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    let count = 0;
    document.querySelectorAll('[data-search]').forEach(a => {
      a.hidden = !a.dataset.search.normalize('NFD').replace(/[\u0300-\u036f]/g, '').includes(value);
      if (!a.hidden) count++;
    });
    document.querySelector('[data-search-status]').textContent = count ? `${count} ${lang === 'fr' ? 'résultats' : 'results'}` : (lang === 'fr' ? 'Aucun résultat. Efface le filtre.' : 'No results. Clear the filter.');
  });
  const menu = document.querySelector('#toggleSidebar');
  const sidebar = document.querySelector('#sidebar');
  const close = document.querySelector('#closeSidebar');
  const mobile = window.matchMedia('(max-width: 800px)');
  const setOpen = (open, restore = false) => {
    sidebar.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
    if (open) close.focus();
    else if (restore) menu.focus();
  };
  if (menu && sidebar && close) {
    menu.addEventListener('click', () => setOpen(!sidebar.classList.contains('open'), true));
    close.addEventListener('click', () => setOpen(false, true));
    document.addEventListener('keydown', event => {
      if (!mobile.matches || !sidebar.classList.contains('open')) return;
      if (event.key === 'Escape') { event.preventDefault(); setOpen(false, true); }
      if (event.key === 'Tab') {
        const nodes = [...sidebar.querySelectorAll('button,input,a[href]')].filter(el => !el.hidden && el.getClientRects().length);
        if (event.shiftKey && document.activeElement === nodes[0]) { event.preventDefault(); nodes.at(-1).focus(); }
        else if (!event.shiftKey && document.activeElement === nodes.at(-1)) { event.preventDefault(); nodes[0].focus(); }
      }
    });
    mobile.addEventListener('change', () => setOpen(false));
  }
  const language = document.querySelector('.lang');
  const syncLanguage = () => { if (language) language.hash = location.hash; };
  syncLanguage();
  window.addEventListener('hashchange', syncLanguage);
  if (language) language.addEventListener('click', syncLanguage);
  update();
})();
