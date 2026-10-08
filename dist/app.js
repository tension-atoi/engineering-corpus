/* Private-to-browser study state. No network, telemetry or privileged actions. */
(() => {
  const lang = document.body.dataset.locale || 'fr';
  const key = 'engineering-corpus:study:v0.1';
  const ids = ['01-mandate', '02-authority', '03-contract', '04-delivery', '05-evidence', '06-documentation', '07-llm', '08-hygiene', 'lab-change', 'lab-api'];
  let state = {};
  try { state = JSON.parse(localStorage.getItem(key) || '{}'); }
  catch (_) { state = {}; }
  const save = () => { try { localStorage.setItem(key, JSON.stringify(state)); } catch (_) {} };
  const update = () => {
    const done = ids.filter(id => state[id]).length;
    const text = document.querySelector('[data-progress-text]');
    const bar = document.querySelector('[data-progress-meter]');
    if (text) text.textContent = `${done} / ${ids.length}`;
    if (bar) bar.style.width = `${done / ids.length * 100}%`;
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
    document.querySelectorAll('[data-search]').forEach(a => {
      a.hidden = !a.dataset.search.normalize('NFD').replace(/[\u0300-\u036f]/g, '').includes(value);
    });
  });
  const menu = document.querySelector('#toggleSidebar');
  const sidebar = document.querySelector('#sidebar');
  if (menu && sidebar) menu.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  update();
})();
