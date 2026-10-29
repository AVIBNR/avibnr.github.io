const body = document.body;
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

// contact sheet: any [data-write] opens it, backdrop / Escape / a chosen link closes it
const sheet = document.querySelector('.sheet');
const openSheet = () => { body.classList.add('sheet-open'); sheet.querySelector('a').focus({ preventScroll: true }); };
const closeSheet = () => body.classList.remove('sheet-open');
document.querySelectorAll('[data-write]').forEach(b => b.addEventListener('click', openSheet));
document.querySelector('.sheet-bg').addEventListener('click', closeSheet);
sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', closeSheet));
addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });

// the floating button steps aside once the contacts block itself is on screen
const fab = document.querySelector('.fab');
const seen = new Set();
const fabIO = new IntersectionObserver(es => {
  es.forEach(e => e.isIntersecting ? seen.add(e.target) : seen.delete(e.target));
  fab.classList.toggle('hide', seen.size > 0);
}, { threshold: .1 });
document.querySelectorAll('.contact, .foot').forEach(el => fabIO.observe(el));

// editor: the timeline follows the video that is actually playing
document.querySelectorAll('.editor').forEach(ed => {
  const video = ed.querySelector('video');
  const tl = ed.querySelector('.tl');
  const tc = ed.querySelector('.tc');
  const subs = [...ed.querySelectorAll('.sub')];
  const len = +ed.dataset.len;
  let raf = 0;
  const pad = n => String(n).padStart(2, '0');
  const tick = () => {
    const t = video.currentTime % len;
    tl.style.setProperty('--p', (t / len).toFixed(4));
    tc.textContent = `00:${pad(Math.floor(t))}:${pad(Math.floor((t % 1) * 30))}`;
    subs.forEach(s => s.classList.toggle('on', t >= +s.dataset.a && t < +s.dataset.b));
    raf = requestAnimationFrame(tick);
  };
  const run = on => {
    cancelAnimationFrame(raf);
    if (on && !still) { video.play().catch(() => {}); raf = requestAnimationFrame(tick); }
    else video.pause();
  };
  ed.run = run;
  if (still) video.removeAttribute('autoplay');
  // only play while the editor is on screen and its tab is shown
  new IntersectionObserver(([e]) => { ed.visible = e.isIntersecting; run(ed.visible && !ed.closest('[data-show=p]')); }).observe(ed);
  document.addEventListener('visibilitychange', () => run(!document.hidden && ed.visible && !ed.closest('[data-show=p]')));
});

// fan: real project screens take turns at the front
document.querySelectorAll('.fan').forEach(fan => {
  const figs = [...fan.querySelectorAll('figure')];
  const cap = fan.querySelector('.fan-cap');
  const names = figs.map(f => f.querySelector('img').alt.split(': '));
  let front = 0, timer = 0;
  const place = () => {
    figs.forEach((f, i) => {
      const pos = (i - front + figs.length) % figs.length;
      f.style.setProperty('--pos', pos);
      f.dataset.pos = pos;
    });
    const [n, d] = names[front];
    cap.innerHTML = `<b>${n}</b><span>${d}</span>`;
  };
  const next = () => { front = (front + 1) % figs.length; place(); };
  const start = () => { clearInterval(timer); if (!still) timer = setInterval(next, 2600); };
  place();
  fan.addEventListener('click', () => { next(); start(); });
  new IntersectionObserver(([e]) => e.isIntersecting ? start() : clearInterval(timer)).observe(fan);
});

// home: Монтаж / Проекты tabs swap the stage and the text under them
const tabs = document.querySelector('.tabs');
if (tabs) {
  const stage = document.querySelector('.stage');
  const btns = [...tabs.querySelectorAll('[role=tab]')];
  const select = btn => {
    const key = btn.id.slice(4);
    btns.forEach(b => {
      const on = b === btn;
      b.setAttribute('aria-selected', on);
      b.tabIndex = on ? 0 : -1;
      document.getElementById(b.getAttribute('aria-controls')).hidden = !on;
    });
    tabs.dataset.at = key;
    stage.dataset.show = key;
    const ed = stage.querySelector('.editor');
    if (ed && ed.run) ed.run(key === 'm' && ed.visible);
  };
  btns.forEach(b => b.addEventListener('click', () => select(b)));
  tabs.addEventListener('keydown', e => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    const i = btns.indexOf(document.activeElement);
    const n = btns[(i + (e.key === 'ArrowRight' ? 1 : btns.length - 1)) % btns.length];
    n.focus(); select(n);
  });
}

// works: a silent preview on hover (mouse only), the full video with sound in a lightbox on click
const lb = document.querySelector('.lb');
const lbBox = lb.querySelector('.lb-box');
const closeLb = () => { lbBox.replaceChildren(); if (lb.open) lb.close(); };
lb.querySelector('.lb-x').addEventListener('click', closeLb);
lb.addEventListener('click', e => { if (e.target === lb || e.target === lbBox) closeLb(); });
lb.addEventListener('close', () => lbBox.replaceChildren());

document.querySelectorAll('.work-play').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.querySelector('video')?.pause();
    const v = document.createElement('video');
    Object.assign(v, { src: btn.dataset.src, controls: true, playsInline: true, autoplay: true });
    lbBox.replaceChildren(v);
    lb.showModal();
    v.play().catch(() => {});
  });
  if (!finePointer || still) return;
  let pv;
  btn.addEventListener('pointerenter', () => {
    if (!pv) {
      pv = document.createElement('video');
      Object.assign(pv, { src: btn.dataset.src, muted: true, loop: true, playsInline: true, preload: 'auto' });
      pv.addEventListener('playing', () => pv.classList.add('on'));
      btn.prepend(pv);
    }
    pv.play().catch(() => {});
  });
  btn.addEventListener('pointerleave', () => { if (pv) { pv.pause(); pv.classList.remove('on'); } });
});
