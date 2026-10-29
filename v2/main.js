// contact sheet: any [data-write] opens it, backdrop / Escape / a chosen link closes it
const body = document.body;
const sheet = document.querySelector('.sheet');
const open = () => { body.classList.add('sheet-open'); sheet.querySelector('a').focus({ preventScroll: true }); };
const close = () => body.classList.remove('sheet-open');
document.querySelectorAll('[data-write]').forEach(b => b.addEventListener('click', open));
document.querySelector('.sheet-bg').addEventListener('click', close);
sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
addEventListener('keydown', e => { if (e.key === 'Escape') close(); });

// the floating button steps aside once the contacts block itself is on screen
const fab = document.querySelector('.fab');
const seen = new Set();
if (fab) {
  const io = new IntersectionObserver(es => {
    es.forEach(e => e.isIntersecting ? seen.add(e.target) : seen.delete(e.target));
    fab.classList.toggle('hide', seen.size > 0);
  }, { threshold: .1 });
  document.querySelectorAll('.contact, .foot').forEach(el => io.observe(el));
}

// reels: the poster is a button, the player is created on the first tap so the page stays light
document.querySelectorAll('.reel [data-src]').forEach(frame => {
  const start = () => {
    if (frame.querySelector('video')) return;
    document.querySelectorAll('.reel video').forEach(v => v.pause());
    const v = document.createElement('video');
    Object.assign(v, { src: frame.dataset.src, controls: true, playsInline: true, autoplay: true });
    frame.removeAttribute('role');
    frame.removeAttribute('tabindex');
    frame.replaceChildren(v);
    v.play().catch(() => {});
  };
  frame.addEventListener('click', start);
  frame.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); start(); } });
});
