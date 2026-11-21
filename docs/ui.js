/* UI 컴포넌트 헬퍼 — 타이틀, 창(.win), 터미널(.term), 카드(.card), 칩(.chip), 단원 실습+모범답안 토글(.labSlide) */
(function () {
  'use strict';
  const { css, h } = DECK;

  function place(el, x, y, w, hh) {
    el.classList.add('abs');
    css(el, { left: x + 'px', top: y + 'px' });
    if (w != null) el.style.width = w + 'px';
    if (hh != null) el.style.height = hh + 'px';
    return el;
  }

  function box(parent, x, y, w, hh, cls = '', html = '') {
    return place(h('div', cls, parent, html), x, y, w, hh);
  }

  function text(parent, cls, html, x, y, w) {
    const e = h('div', cls, parent, html);
    place(e, x, y, w);
    return e;
  }

  function title(parent, kicker, html, o = {}) {
    const x = o.x ?? 100, y = o.y ?? 70, w = o.w ?? 1720;
    const wrap = place(h('div', 'ttl', parent), x, y, w);
    if (kicker) h('div', 'k', wrap, kicker);
    const t = h('div', o.cls || 'h2', wrap, html);
    if (kicker) css(t, { marginTop: '14px' });
    if (o.align) css(wrap, { textAlign: o.align });
    return { wrap, t };
  }

  function card(parent, o = {}) {
    const c = h('div', 'card', parent);
    place(c, o.x ?? 100, o.y ?? 240, o.w ?? 520, o.h ?? null);
    if (o.pad != null) css(c, { padding: o.pad + 'px' });
    return c;
  }

  function win(parent, o = {}) {
    const w = h('div', 'win' + (o.dark ? ' dark' : ''), parent);
    place(w, o.x ?? 100, o.y ?? 240, o.w ?? 800, o.h ?? 500);
    const bar = h('div', 'win-bar', w);
    h('div', 'win-dots', bar, '<i></i><i></i><i></i>');
    if (o.title) h('span', '', bar, o.title);
    if (o.right) { const r = h('span', '', bar, o.right); css(r, { marginLeft: 'auto' }); }
    const body = h('div', 'win-body', w);
    return { el: w, body };
  }

  function chip(parent, txt, o = {}) {
    const c = h('span', 'chip' + (o.size ? ' ' + o.size : ''), parent, txt);
    css(c, { background: o.bg || '#DCE6FF', color: o.fg || '#1E4FD0' });
    if (o.x != null) place(c, o.x, o.y);
    return c;
  }

  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function copyTextToClipboard(text, btn) {
    const done = () => {
      const prev = btn.textContent;
      btn.textContent = '✓ 복사 완료!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = prev; btn.classList.remove('copied'); }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  }

  function fallbackCopy(text, done) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;left:-9999px;top:0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (_) {}
    ta.remove();
  }

  /* 단원별 실습 + 클릭 토글 모범 답안 한 페이지 빌더 */
  function buildLabSlide(el, A, spec) {
    const T = title(el, spec.kicker, spec.heading, { y: 60 });
    A(T.t, 'up', 0, { dur: 0.4 });

    const grid = h('div', 'lab-grid', el);

    // 좌측: 실습 미션 카드
    const left = h('section', 'lab-mission', grid);
    left.setAttribute('aria-label', spec.missionTitle || '실습 과제');
    h('div', 'row', left, `<span class="chip" style="background:var(--blue-l);color:var(--blue-d)">실습 미션</span><span class="cap" style="margin-left:12px">${esc(spec.duration || '15분')}</span><span class="cap" style="margin-left:auto;color:var(--green)">[A] 모범답안 &amp; 해결 프롬프트</span>`);
    h('h3', 'h4', left, esc(spec.missionTitle));
    const ul = h('ul', 'lab-steps', left);
    (spec.steps || []).forEach(st => h('li', '', ul, st));
    if (spec.runCmd) {
      h('div', 'cap', left, '컨테이너 실행 명령');
      const cmdPre = h('pre', 'lab-cmd', left);
      cmdPre.setAttribute('role', 'region');
      cmdPre.setAttribute('aria-label', '실습 실행 명령어');
      cmdPre.setAttribute('tabindex', '0');
      h('code', '', cmdPre, esc(spec.runCmd));
    }

    // 'A' 모범 답안 열기 시 실습 미션 카드 내부에 표시되는 해결용 사용자 프롬프트 + Copy 버튼
    const promptText = spec.userPrompt || (
      `[${spec.id || '실습'}] ${spec.missionTitle} 과제를 해결해줘. 실행 명령(${(spec.runCmd || '').replace(/\n/g, ' && ')})으로 동작과 테스트 통과 여부를 끝까지 검증해줘.`
    );
    const pBox = h('div', 'lab-prompt-box no-advance', left);
    const pHead = h('div', 'lab-prompt-head', pBox);
    h('span', 'lab-prompt-title', pHead, '💬 실습 해결용 사용자 프롬프트 (AI 에이전트 입력용)');
    const copyBtn = h('button', 'btn-copy-prompt no-advance', pHead, '📋 프롬프트 복사');
    copyBtn.type = 'button';
    copyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      copyTextToClipboard(promptText, copyBtn);
    });
    const pPre = h('pre', 'lab-prompt-text', pBox);
    pPre.setAttribute('role', 'region');
    pPre.setAttribute('aria-label', '실습 해결용 사용자 프롬프트');
    pPre.setAttribute('tabindex', '0');
    h('code', '', pPre, esc(promptText));

    A(left, 'up', 0.12, { dur: 0.45 });

    // 우측: 클릭 시 열리는 모범 답안 (<details>/<summary>, heading 금지)
    const right = h('section', 'lab-solution', grid);
    right.setAttribute('aria-label', '모범 답안 토글');
    const det = h('details', 'answer-toggle', right);
    const sum = h('summary', '', det);
    h('span', '', sum, spec.answerLabel || '모범 답안 확인하기 (클릭하여 열기/닫기)');
    h('span', 'answer-badge', sum, spec.answerType || 'Tree + Code');
    det.addEventListener('toggle', () => {
      left.classList.toggle('show-prompt', det.open);
    });

    const body = h('div', 'answer-body', det);
    if (spec.answerSummary) {
      h('div', 'answer-hint', body, spec.answerSummary);
    }
    if (spec.tree) {
      const cap1 = h('div', 'cap', body, '파일 구조 (Tree)');
      cap1.id = spec.id + '-tree-cap';
      const preT = h('pre', 'tree', body);
      preT.setAttribute('role', 'region');
      preT.setAttribute('aria-labelledby', cap1.id);
      preT.setAttribute('tabindex', '0');
      h('code', '', preT, esc(spec.tree));
    }
    if (spec.answerCode) {
      const cap2 = h('div', 'cap', body, spec.codeCaption || '핵심 구현 / 실행 결과');
      cap2.id = spec.id + '-code-cap';
      const preC = h('pre', 'code-block', body);
      preC.setAttribute('role', 'region');
      preC.setAttribute('aria-labelledby', cap2.id);
      preC.setAttribute('tabindex', '0');
      h('code', '', preC, esc(spec.answerCode));
    }
    A(right, 'up', 0.22, { dur: 0.45 });
  }

  window.UI = { place, box, text, title, card, win, chip, esc, buildLabSlide };
})();
