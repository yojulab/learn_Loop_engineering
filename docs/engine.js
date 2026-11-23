/* DECK 모션 슬라이드 엔진 — 1920×1080 순수 함수 렌더러 (revfactory/oss-lecture 패턴 기반)
 * 키보드: → Space PageDown Enter = 다음, ← PageUp Backspace = 이전,
 *         O = 목차, P = 발표자 창, F = 전체 화면, B = 블랙아웃, H = 하단 숨김, A = 현재 슬라이드 모범답안 토글
 * URL: #12 (12번 슬라이드)
 */
(function () {
  'use strict';
  const W = 1920, H = 1080;
  const Q = new URLSearchParams(location.search);
  const MODE = Q.has('print') ? 'print' : 'live';
  const FINAL = 99;
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const ease = {
    linear: x => x,
    outCubic: x => 1 - Math.pow(1 - x, 3),
    outBack: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    snap: x => 1 - Math.pow(1 - x, 3.2),
  };
  const prog = (t, start, dur, e = ease.snap) => reducedMotion ? (t >= start ? 1 : 0) : e(clamp((t - start) / Math.max(1e-6, dur)));

  function css(el, o) {
    if (!el) return el;
    for (const k in o) {
      const v = o[k];
      if (k.startsWith('--')) el.style.setProperty(k, v);
      else el.style[k] = v;
    }
    return el;
  }
  function h(tag, cls, parent, html) {
    const e = document.createElement(tag || 'div');
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    if (parent) parent.appendChild(e);
    return e;
  }
  const SVGNS = 'http://www.w3.org/2000/svg';
  function s(tag, attrs, parent) {
    const e = document.createElementNS(SVGNS, tag);
    if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  const PRESET = {
    fade: (el, p) => css(el, { opacity: p }),
    up: (el, p, o) => css(el, { opacity: p, transform: `translateY(${lerp(o.d ?? 36, 0, p)}px)` }),
    right: (el, p, o) => css(el, { opacity: p, transform: `translateX(${lerp(-(o.d ?? 40), 0, p)}px)` }),
    pop: (el, p) => css(el, { opacity: clamp(p * 1.8), transform: `scale(${lerp(0.78, 1, p)})` }),
    wipe: (el, p) => css(el, { opacity: p > 0 ? 1 : 0, clipPath: `inset(0 ${((1 - p) * 100).toFixed(2)}% 0 0)` }),
    grow: (el, p) => css(el, { opacity: p > 0 ? 1 : 0, transform: `scaleX(${p})`, transformOrigin: '0 50%' }),
  };

  const slides = [];
  const parts = [];
  function part(key, label, color) { parts.push({ key, label, color }); }
  function slide(def) { slides.push(def); }

  let root, stage, chromeEl, railSvg, railPartEl, railNumEl, blackEl, ovEl;
  let cur = 0, step = 0, enterAt = 0, stepAt = [0], rafId = 0;
  let jumpBuf = '', jumpTimer = 0;
  const bc = ('BroadcastChannel' in window) ? new BroadcastChannel('loop-ppt-sync') : null;

  function buildSlideDom(d, idx) {
    d.index = idx;
    const el = h('section', 'slide theme-' + (d.theme || 'paper') + (d.dots ? ' dots' : ''), stage);
    el.setAttribute('aria-label', `${idx + 1}. ${d.title || ''}`);
    d.el = el;
    d.anims = [];
    const A = (target, preset, start = 0, opts = {}) => {
      const fn = typeof preset === 'function' ? preset : (PRESET[preset] || PRESET.up);
      d.anims.push({ el: target, fn, start, dur: opts.dur ?? 0.45, step: opts.step ?? 0, ease: opts.ease || ease.snap, opts });
    };
    if (d.build) d.build(el, A);
  }

  function renderSlide(d, t, curStep, stArr) {
    for (const a of d.anims) {
      const st = a.step || 0;
      const localT = st <= curStep ? (st === 0 ? t : stArr[st] ?? t) : -1;
      const p = localT < 0 ? 0 : prog(localT, a.start, a.dur, a.ease);
      a.fn(a.el, p, a.opts);
    }
    if (d.render) d.render(t, { step: curStep, at: k => stArr[k] ?? -1 });
  }

  function buildChrome() {
    chromeEl = h('div', 'chrome', stage);
    railSvg = s('svg', { width: W, height: 24, viewBox: `0 0 ${W} 24`, class: 'rail' }, chromeEl);
    s('line', { x1: 100, y1: 12, x2: W - 100, y2: 12, class: 'rail-main' }, railSvg);
    railPartEl = h('div', 'rail-part', chromeEl);
    railNumEl = h('div', 'rail-num', chromeEl);
  }

  function updateChrome() {
    const d = slides[cur];
    root.dataset.theme = d.theme || 'paper';
    root.classList.toggle('nochrome', !!d.noChrome);
    while (railSvg.children.length > 1) railSvg.lastChild.remove();
    const x0 = 100, x1 = W - 100, span = x1 - x0;
    const n = Math.max(1, slides.length - 1);
    const curX = x0 + (cur / n) * span;
    const pObj = parts.find(p => p.key === d.part);
    s('line', { x1: x0, y1: 12, x2: curX, y2: 12, stroke: pObj ? pObj.color : 'var(--green)', class: 'rail-branch' }, railSvg);
    slides.forEach((sd, i) => {
      const cx = x0 + (i / n) * span;
      if (i === cur) {
        s('circle', { cx, cy: 12, r: 7, class: 'rail-cur' }, railSvg);
      } else {
        s('circle', { cx, cy: 12, r: 3.5, class: 'rail-dot' + (i < cur ? ' done' : '') }, railSvg);
      }
    });
    railPartEl.textContent = `${pObj ? pObj.label : ''}${d.chap ? '  ·  ' + d.chap : ''}`;
    railNumEl.innerHTML = `<b>${cur + 1}</b> / ${slides.length}`;
  }

  function buildOverview() {
    ovEl = h('div', 'overview', document.body);
    ovEl.setAttribute('aria-label', '전체 슬라이드 목차');
    const grouped = new Map();
    parts.forEach(p => grouped.set(p.key, { label: p.label, color: p.color, items: [] }));
    slides.forEach((sd, i) => {
      const k = sd.part || (parts[0] && parts[0].key) || 'opening';
      if (!grouped.has(k)) grouped.set(k, { label: k, color: '#12B07A', items: [] });
      grouped.get(k).items.push({ sd, i });
    });
    for (const [, g] of grouped) {
      if (!g.items.length) continue;
      const box = h('div', 'ov-g', ovEl);
      const hd = h('div', 'ov-h', box, g.label);
      hd.style.color = g.color;
      g.items.forEach(({ sd, i }) => {
        const btn = h('button', 'ov-i', box, `<b>${String(i + 1).padStart(2, '0')}</b>${sd.title}`);
        btn.type = 'button';
        btn.dataset.idx = String(i);
        btn.addEventListener('click', () => { go(i, { instant: true }); toggleOverview(false); });
      });
    }
  }

  function toggleOverview(force) {
    const show = force !== undefined ? force : !ovEl.classList.contains('show');
    ovEl.classList.toggle('show', show);
    if (show) {
      ovEl.querySelectorAll('.ov-i').forEach(b => b.classList.toggle('active', Number(b.dataset.idx) === cur));
    }
  }

  function sync() {
    if (!bc || !slides[cur]) return;
    bc.postMessage({
      type: 'state',
      i: cur,
      step,
      n: slides.length,
      title: slides[cur].title,
      notes: slides[cur].notes || '',
      steps: slides[cur].steps || 0,
      next: slides[cur + 1] ? slides[cur + 1].title : '',
    });
  }

  function go(idx, opts = {}) {
    const nextIdx = clamp(idx, 0, slides.length - 1);
    slides.forEach((sd, i) => {
      sd.el.classList.toggle('on', i === nextIdx);
      sd.el.classList.remove('off');
    });
    cur = nextIdx;
    step = opts.final ? (slides[cur].steps || 0) : 0;
    const now = performance.now() / 1000;
    enterAt = opts.instant ? now - 5 : now;
    stepAt = [enterAt];
    if (location.hash !== '#' + (cur + 1)) history.replaceState(null, '', '#' + (cur + 1));
    updateChrome();
    sync();
  }

  function next() {
    const maxStep = slides[cur].steps || 0;
    if (step < maxStep) {
      step += 1;
      stepAt[step] = performance.now() / 1000;
      sync();
      return;
    }
    if (cur < slides.length - 1) go(cur + 1);
  }

  function back() {
    if (step > 0) { step -= 1; sync(); return; }
    if (cur > 0) go(cur - 1, { instant: true, final: true });
  }

  function frame() {
    const now = performance.now() / 1000;
    const d = slides[cur];
    if (d) {
      const relSteps = stepAt.map(t0 => now - t0);
      renderSlide(d, now - enterAt, step, relSteps);
    }
    rafId = requestAnimationFrame(frame);
  }

  function fit() {
    const k = Math.min(window.innerWidth / W, window.innerHeight / H);
    css(stage, { transform: `translate(-50%,-50%) scale(${k})` });
  }

  function toggleCurrentAnswer() {
    const det = slides[cur]?.el?.querySelector('details.answer-toggle');
    if (det) {
      det.open = !det.open;
      const lc = slides[cur]?.el?.querySelector('.lab-left-col');
      if (lc) lc.classList.toggle('show-prompt', det.open);
      return;
    }
    const prob = slides[cur]?.el?.querySelector('.prob-reveal');
    if (prob) {
      const next = prob.getAttribute('data-revealed') !== 'true';
      prob.setAttribute('data-revealed', String(next));
      prob.setAttribute('aria-pressed', String(next));
    }
  }

  function toggleFullscreen() {
    const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
    if (fsEl) {
      const exitFn = document.exitFullscreen || document.webkitExitFullscreen;
      if (exitFn) Promise.resolve(exitFn.call(document)).catch(() => {});
    } else {
      const el = document.documentElement;
      const reqFn = el.requestFullscreen || el.webkitRequestFullscreen;
      if (reqFn) Promise.resolve(reqFn.call(el)).catch(() => {});
    }
  }

  function openPresenter() {
    window.open('presenter.html', 'deck-presenter', 'width=1200,height=780');
    setTimeout(sync, 600);
  }

  function readDigit(k, code) {
    if (/^[0-9]$/.test(k)) return k;
    const m = /^(?:Digit|Numpad)([0-9])$/.exec(code || '');
    return m ? m[1] : null;
  }

  function keys(e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const target = e.target && e.target.nodeType === 1 ? e.target : null;
    if (target && target.closest('input, textarea, select, [contenteditable="true"], [contenteditable=""]')) return;

    const k = e.key || '';
    const kl = k.toLowerCase();
    const code = e.code || '';
    const interactiveEl = target && target.closest('summary, button, a[href]');
    const isSpace = code === 'Space' || k === ' ' || k === 'Spacebar';
    const isEnter = code === 'Enter' || code === 'NumpadEnter' || k === 'Enter';

    const digit = readDigit(k, code);
    if (digit !== null) {
      jumpBuf += digit;
      clearTimeout(jumpTimer);
      jumpTimer = setTimeout(() => { jumpBuf = ''; }, 1500);
      return;
    }

    if (isEnter && jumpBuf) {
      e.preventDefault();
      go(parseInt(jumpBuf, 10) - 1, { instant: true });
      jumpBuf = '';
      return;
    }

    // <summary> / <button> 포커스 상태에서도 Enter·Space만 기본 동작에 위임하고 나머지 단축키는 유지
    if (interactiveEl && (isEnter || isSpace)) return;

    if (isSpace && e.shiftKey) { e.preventDefault(); back(); }
    else if (code === 'ArrowRight' || code === 'PageDown' || code === 'ArrowDown' || isSpace || isEnter || ['ArrowRight', 'PageDown', 'ArrowDown'].includes(k)) {
      e.preventDefault();
      next();
    }
    else if (code === 'ArrowLeft' || code === 'PageUp' || code === 'ArrowUp' || code === 'Backspace' || ['ArrowLeft', 'PageUp', 'ArrowUp', 'Backspace'].includes(k)) {
      e.preventDefault();
      back();
    }
    else if (code === 'Home' || k === 'Home') { e.preventDefault(); go(0, { instant: true }); }
    else if (code === 'End' || k === 'End') { e.preventDefault(); go(slides.length - 1, { instant: true }); }
    else if (code === 'KeyF' || kl === 'f') { e.preventDefault(); toggleFullscreen(); }
    else if (code === 'KeyO' || kl === 'o' || code === 'Escape' || k === 'Escape') {
      e.preventDefault();
      toggleOverview((code === 'Escape' || k === 'Escape') ? false : undefined);
    }
    else if (code === 'KeyA' || kl === 'a') { e.preventDefault(); toggleCurrentAnswer(); }
    else if (code === 'KeyB' || code === 'Period' || kl === 'b' || k === '.') { e.preventDefault(); blackEl.classList.toggle('show'); }
    else if (code === 'KeyH' || kl === 'h') { e.preventDefault(); root.classList.toggle('nochrome'); }
    else if (code === 'KeyP' || kl === 'p') { e.preventDefault(); openPresenter(); }
  }

  function buildHud() {
    const hud = h('div', 'hud-actions', document.body);
    const items = [
      ['Home', () => { location.href = 'index.html'; }],
      ['교육 정보 ↗', () => { window.open('https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing', '_blank', 'noopener'); }],
      ['목차 (O)', () => toggleOverview()],
      ['발표자 창 (P)', () => openPresenter()],
    ];
    items.forEach(([label, fn]) => {
      const btn = h('button', 'hud-btn', hud, label);
      btn.type = 'button';
      btn.addEventListener('click', (e) => {
        fn();
        if (e.detail > 0) btn.blur();
      });
    });
  }

  async function start() {
    root = document.getElementById('deck');
    root.classList.add('mode-' + MODE);
    if (MODE === 'print') {
      document.documentElement.classList.add('print');
      slides.forEach((d, idx) => {
        const page = h('div', 'page', root);
        stage = h('div', 'stage', page);
        buildSlideDom(d, idx);
        d.el.classList.add('on');
        d.el.querySelectorAll('details.answer-toggle').forEach(det => { det.open = true; });
        d.el.querySelectorAll('.lab-left-col').forEach(m => m.classList.add('show-prompt'));
        const fin = Array.from({ length: (d.steps || 0) + 1 }, () => FINAL);
        renderSlide(d, FINAL, d.steps || 0, fin);
      });
      return;
    }

    stage = h('div', 'stage', root);
    slides.forEach(buildSlideDom);
    buildChrome();
    blackEl = h('div', 'blackout', stage);
    buildOverview();
    buildHud();
    fit();
    window.addEventListener('resize', fit);
    window.addEventListener('keydown', keys);
    stage.addEventListener('click', e => {
      if (e.target.closest('a, button, summary, details, pre, .lab-answer, .no-advance')) return;
      next();
    });
    stage.addEventListener('contextmenu', e => { e.preventDefault(); back(); });
    if (bc) {
      bc.onmessage = m => {
        const d = m.data || {};
        if (d.type === 'cmd') {
          if (d.cmd === 'next') next();
          else if (d.cmd === 'back') back();
          else if (d.cmd === 'hello') sync();
        }
      };
    }
    const hi = parseInt((location.hash || '#1').slice(1), 10);
    go((isNaN(hi) ? 1 : hi) - 1, { instant: true });
    rafId = requestAnimationFrame(frame);
  }

  window.DECK = { W, H, slide, part, slides, parts, start, go, css, h, s, ease, prog, lerp, clamp };
})();
