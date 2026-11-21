
(function () {
  const { h } = DECK;
  const { title, card, chip } = UI;

  DECK.part('prologue', 'Prologue · 오프닝 & eBook 핵심 (4장)', '#2F6BFF');

  // p.1: 대형 프로필 이미지 영역 + 소셜 QR 코드 + 교육 정보 시트 링크 + 경력 사항 표
  DECK.slide({
    id: 'prologue-profile',
    part: 'prologue',
    chap: '강사 소개 & 경력',
    theme: 'paper',
    title: "Let's AX with Cartoons. — 오상훈 대표 프로필 & 경력 사항",
    notes: '대형 프로필 이미지, LinkedIn/Facebook QR 코드, 교육 관련 정보 시트 링크 및 주요 경력 사항 표 페이지입니다.',
    build(el, A) {
      const T = title(el, "LET'S AX WITH CARTOONS", '오상훈 대표 <span class="hb">프로필 &amp; 주요 경력</span>', { y: 48 });
      A(T.t, 'up', 0, { dur: 0.4 });

      // 좌측: 프로필 이미지 대형 할당 (w: 520, h: 785)
      const left = card(el, { x: 100, y: 195, w: 520, h: 785, pad: 18 });
      left.innerHTML = `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#F6EFE4;border-radius:18px;overflow:hidden;border:1.5px solid var(--ln)">
        <img src="assets/profile_ohsanghun.jpg" alt="오상훈 대표 대형 프로필 이미지" style="width:100%;height:100%;object-fit:contain;display:block">
      </div>`;
      A(left, 'up', 0.1, { dur: 0.45 });

      // 우측: 상단 소개 & QR & 교육 정보 링크 + 하단 경력 사항 표
      const right = card(el, { x: 650, y: 195, w: 1170, h: 785, pad: 28 });
      right.innerHTML = `<div style="display:flex;justify-content:space-between;align-items:center;gap:20px;padding-bottom:18px;border-bottom:1.5px solid var(--ln)">
        <div>
          <div class="row" style="gap:10px;flex-wrap:wrap">
            <span class="chip" style="background:var(--blue-l);color:var(--blue-d)">Tech-driven Business Architect</span>
            <a class="edu-sheet-pill" href="https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing" target="_blank" rel="noopener noreferrer">📊 교육 관련 정보 시트 열기 ↗</a>
          </div>
          <div class="h3" style="margin-top:12px">오상훈 대표 <span class="b2" style="font-weight:600;color:var(--fg2)">· 22년 차 대형 SI 아키텍트 &amp; AI/RAG 전문 연구원</span></div>
        </div>
        <div style="display:flex;gap:14px;flex:none">
          <a href="https://www.linkedin.com/in/oh-sanghun-5a5b11b9/" target="_blank" rel="noopener noreferrer" style="text-decoration:none;color:inherit;background:#F6F8FC;border:1.5px solid var(--ln);border-radius:14px;padding:10px 14px;text-align:center">
            <img src="assets/qr_linkedin.svg" alt="LinkedIn QR" style="width:104px;height:104px;display:block;margin:0 auto">
            <div class="cap" style="margin-top:6px;font-size:16px;color:var(--blue-d)">LinkedIn</div>
          </a>
          <a href="https://www.facebook.com/otter.oh" target="_blank" rel="noopener noreferrer" style="text-decoration:none;color:inherit;background:#F6F8FC;border:1.5px solid var(--ln);border-radius:14px;padding:10px 14px;text-align:center">
            <img src="assets/qr_facebook.svg" alt="Facebook QR" style="width:104px;height:104px;display:block;margin:0 auto">
            <div class="cap" style="margin-top:6px;font-size:16px;color:var(--blue-d)">Facebook</div>
          </a>
        </div>
      </div>
      <div class="h4" style="margin:18px 0 12px">주요 경력 사항 &amp; 전문 분야</div>
      <table class="tbl">
        <thead><tr><th style="width:220px">구분</th><th>주요 경력 및 핵심 역량</th></tr></thead>
        <tbody>
          <tr><td><b>엔터프라이즈 SI</b></td><td>22년 차 대형 SI 프로젝트 리드 (Samsung, SK, LG 등) 및 로보틱스 자동화 시스템 구축</td></tr>
          <tr><td><b>AI / RAG 연구</b></td><td>점선면 연구소 대표 — AI/RAG &amp; 의사결정지원시스템(DSS) 설계·구축</td></tr>
          <tr><td><b>실전 교육 PM</b></td><td>AI 전문 교육 PM / 누적 <b>7,000시간+</b> 실전 강의 및 기업 AX 컨설팅</td></tr>
          <tr><td><b>아키텍처 핵심</b></td><td>Java/Cloud 대규모 분산 아키텍처 · 지능형 에이전트(MCP · Loop) · Tech-driven 로보틱스 DT 전략</td></tr>
          <tr><td><b>교육 정보 &amp; 웹</b></td><td><a href="https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing" target="_blank" rel="noopener noreferrer" style="color:var(--blue-d);font-weight:700">교육 관련 정보 시트(Google Sheets) ↗</a> · <code>https://cocolabhub.com/</code> · <code>https://lectomate.com</code></td></tr>
        </tbody>
      </table>`;
      A(right, 'up', 0.18, { dur: 0.45 });
    },
  });

  // p.2: AI = Probability ('Probability'는 A 키보드 사용 시 보임)
  DECK.slide({
    id: 'prologue-probability',
    part: 'prologue',
    chap: 'AI의 본질',
    theme: 'night',
    dots: true,
    title: 'AI = Probability (단축키 A로 공개)',
    notes: "키보드 'A' 키(또는 우측 상단 토글)를 누르면 'Probability'가 화면에 나타납니다.",
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:240px;width:1680px;text-align:center';
      chip(box, 'PRESS [A] TO REVEAL', { bg: 'rgba(75,227,166,.16)', fg: '#4BE3A6' });

      const eq = h('div', 'prob-eq', box,
        '<span>AI</span><span class="prob-op">=</span><button type="button" class="prob-reveal" data-revealed="false" aria-pressed="false" title="A 키 또는 클릭으로 공개"><span class="prob-word">Probability</span><span class="prob-mask">? (Press A)</span></button>');
      const btn = eq.querySelector('.prob-reveal');
      btn.addEventListener('click', () => {
        const next = btn.getAttribute('data-revealed') !== 'true';
        btn.setAttribute('data-revealed', String(next));
        btn.setAttribute('aria-pressed', String(next));
      });

      h('div', 'b1', box, '확률적 생성 모델의 결과를 <b>결정론적 검증 루프</b>로 통제하는 것이 에이전트 엔지니어링의 출발점').style.cssText = 'margin-top:44px;color:#AEB8D3';
      A(box, 'up', 0.08, { dur: 0.45 });
    },
  });

  // p.3: 교육 마친 후 희망 사항 (이해의 부채의 늪 -> 진정한 검증자 추구)
  DECK.slide({
    id: 'prologue-goal',
    part: 'prologue',
    chap: '교육 목표 & 희망 사항',
    theme: 'white',
    title: '교육 마친 후 희망 사항: 이해의 부채를 넘어 진정한 검증자로',
    notes: 'AI가 코드를 빨리 짜줄수록 이해의 부채(Comprehension Debt)가 쌓입니다. 과정 후에는 스스로 검증하는 진정한 검증자가 되는 것이 목표입니다.',
    build(el, A) {
      const T = title(el, 'AFTER THIS WORKSHOP', '교육을 마친 후: <span class="hr">이해의 부채</span>에서 <span class="hl">진정한 검증자</span>로', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 240, w: 830, h: 680, pad: 36 });
      c1.innerHTML = `<span class="chip" style="background:var(--red-l);color:var(--red)">피해야 할 함정</span>
      <div class="h3" style="margin-top:20px">이해의 부채(Comprehension Debt)의 늪</div>
      <div class="b2" style="margin-top:20px">AI가 만든 코드를 이해하지 못한 채 복붙·배포만 반복하면, 장애 순간 아무것도 고치지 못하는 <b>기술·이해 부채의 늪</b>에 빠집니다.</div>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 990, y: 240, w: 830, h: 680, pad: 36 });
      c2.innerHTML = `<span class="chip" style="background:var(--green-l);color:var(--green-d)">우리가 추구하는 목표</span>
      <div class="h3" style="margin-top:20px">진정한 검증자 (True Verifier)</div>
      <div class="b2" style="margin-top:20px">작성자(Maker)와 검증자(Checker)를 분리하고, 테스트·린터·Trace·Eval로 근거를 확인하여 <b>AI를 신뢰 가능하게 통제하는 아키텍트</b>로 성장합니다.</div>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // p.4: eBook 프롤로그 내용 정리
  DECK.slide({
    id: 'prologue-ebook',
    part: 'prologue',
    chap: 'eBook 프롤로그 요약',
    theme: 'paper',
    title: 'eBook 프롤로그: 프롬프트를 넘어 시스템을 엔지니어링하라',
    notes: 'eBook 프롤로그의 핵심 메시지(프롬프트 → 12대 스택 4계층 시스템 엔지니어링 → 탐험 순서)를 정리한 페이지입니다.',
    build(el, A) {
      const T = title(el, 'EBOOK PROLOGUE SUMMARY', '프롬프트를 넘어 <span class="hb">12대 스택 4계층</span> 시스템을 엔지니어링하라', { y: 56 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const layers = [
        ['1계층 · 지식과 기억', 'RAG · Context · Memory', '답변 전 외부 지식을 찾고(RAG), 현재 시야(Context)와 세션 간 기억(Memory)을 유지', '#E6E0FF', '#4D2FD0'],
        ['2계층 · 행동과 도구', 'Agent · Agentic AI · Tools', '단발 응답을 넘어 계획·결정·자기 수정 루프와 외부 함수(Tools)로 직접 행동', '#DCE6FF', '#1E4FD0'],
        ['3계층 · 표준과 확장', 'MCP · Skills · Hooks', '개방형 도구 표준(MCP), 온디맨드 노하우(Skills), 정해진 시점 강제 트리거(Hooks)', '#D5F2E6', '#0B8A5F'],
        ['4계층 · 위임과 검증', 'Subagents · Orchestration · Eval', '역할 분리 위임(Subagents), 다단계 조율(Orchestration), 동작·품질 측정(Eval)', '#FDEFD3', '#9A5B00'],
      ];
      layers.forEach(([l, elems, desc, bg, fg], i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const c = card(el, { x: 100 + col * 880, y: 220 + row * 320, w: 840, h: 290, pad: 30 });
        c.innerHTML = `<div class="row" style="justify-content:space-between"><span class="chip" style="background:${bg};color:${fg}">${l}</span><code style="font-size:20px">${elems}</code></div>
          <div class="b2" style="margin-top:20px">${desc}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });

      const foot = card(el, { x: 100, y: 870, w: 1720, h: 95, pad: 22 });
      foot.innerHTML = `<div class="b3" style="color:var(--ink)"><b>탐험 순서:</b> Part 1(행동과 표준: Agent·MCP·Hooks·Skills) → Part 2(지식과 기억: Context·RAG·Memory) → Part 3~4(위임과 검증: Subagents·Loop·Orchestration·Eval)</div>`;
      A(foot, 'up', 0.42, { dur: 0.4 });
    },
  });
})();
