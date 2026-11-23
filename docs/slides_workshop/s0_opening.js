(function () {
  const { h } = DECK;
  const { title, card, win, chip, text, buildLabSlide } = UI;

  // 1. 표지 (No Chrome)
  DECK.slide({
    id: 'cover',
    part: 'opening',
    chap: '카툰 심화 워크숍',
    theme: 'night',
    dots: true,
    noChrome: true,
    title: '카툰으로 배우는 1인 N프로젝트 운영체제: 루프 엔지니어링 (카툰 심화 워크숍)',
    notes: '카툰 스토리텔링과 함께 12대 AI 에이전트 스택의 이론·실습·모범 답안을 완주하는 심화 워크숍 웹 PPT입니다.',
    build(el, A) {
      const tag = h('div', 'row abs', el);
      tag.style.cssText = 'left:100px;top:85px;width:1060px;gap:12px;flex-wrap:wrap';
      chip(tag, '카툰 심화 워크숍', { bg: 'rgba(75,227,166,.16)', fg: '#4BE3A6' });
      chip(tag, 'GitHub Pages · Web PPT', { bg: 'rgba(47,107,255,.22)', fg: '#9DBBFF' });
      chip(tag, 'Claude · ChatGPT · Gemini 공용', { bg: 'rgba(124,92,255,.22)', fg: '#C7B8FF' });
      h('a', 'edu-sheet-btn', tag, '📊 교육 관련 정보 시트 ↗').setAttribute('href', 'https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing');
      tag.lastElementChild.setAttribute('target', '_blank');
      A(tag, 'fade', 0, { dur: 0.4 });

      const hero = h('div', 'abs', el);
      hero.style.cssText = 'left:100px;top:175px;width:1060px';
      h('div', 'h1', hero, '카툰으로 배우는 1인 N프로젝트 운영체제:<br><span class="hl">루프 엔지니어링</span>').style.cssText = 'font-size:56px;line-height:1.18';
      h('div', 'b1', hero, '<b>1인 멀티 프로젝트의 핵심 원리</b>부터 전 단원 실습·모범 답안까지,<br>시간 제약 없이 내 속도로 끝내는 <b>올인원 가이드</b>').style.cssText = 'margin-top:22px;color:#AEB8D3;font-size:24px';
      A(hero, 'up', 0.12, { dur: 0.55 });

      const qrBox = h('div', 'row abs', el);
      qrBox.style.cssText = 'left:100px;top:495px;gap:20px';
      qrBox.innerHTML = `<a class="qr-slide-card" href="https://www.linkedin.com/in/oh-sanghun-5a5b11b9/" target="_blank" rel="noopener noreferrer">
          <img src="assets/qr_linkedin.svg" alt="LinkedIn QR"><span>LinkedIn</span>
        </a>
        <a class="qr-slide-card" href="https://www.facebook.com/otter.oh" target="_blank" rel="noopener noreferrer">
          <img src="assets/qr_facebook.svg" alt="Facebook QR"><span>Facebook</span>
        </a>`;
      A(qrBox, 'fade', 0.2, { dur: 0.45 });

      const w = win(el, { x: 100, y: 715, w: 1060, h: 255, dark: true, title: 'quickstart.sh — 키보드 조작 & 컨테이너 환경' });
      w.body.innerHTML = `<div class="term"><span class="p">$</span>cd /apps/learn_Loop_engineering && python3 scripts/verify_chapters.py --all
<span class="o"># 웹 PPT 단축키: → / Space(다음) · ←(이전) · A(모범답안) · O(목차) · P(발표자 창) · F(전체 화면)</span></div>`;
      A(w.el, 'up', 0.28, { dur: 0.5 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_00_in.jpg" alt="프롤로그 도입 카툰: AI 에이전트 스택 전체 지도 & 도입 순서" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
    },
  });


  // 2. 최종 목적 아키텍처 (LangGraph + Langfuse 다이어그램 중심 구성)
  DECK.slide({
    id: 'target-architecture',
    part: 'opening',
    chap: '최종 목적 아키텍처',
    theme: 'white',
    title: '최종 목적 아키텍처: LangGraph + Langfuse 프롬프트 개선 루프',
    notes: 'LangGraph(실행) → LiteLLM Proxy(무코드 수집) → Langfuse(모니터링·Eval) → Prompt Registry(Save as Prompt) → LangGraph로 되돌아오는 폐쇄형 개선 루프 다이어그램입니다.',
    build(el, A) {
      const T = title(
        el,
        'TARGET ARCHITECTURE · CLOSED LOOP DIAGRAM',
        '최종 목적 아키텍처: <span class="hb">LangGraph</span> + <span class="hl">Langfuse</span> 개선 루프',
        { y: 56 },
      );
      A(T.t, 'up', 0, { dur: 0.4 });

      const wrap = h('div', 'abs', el);
      wrap.style.cssText = 'left:100px;top:210px;width:1720px;height:760px';
      wrap.innerHTML = `
      <svg viewBox="0 0 1720 740" width="1720" height="740" role="img" aria-label="LangGraph, LiteLLM Proxy, Langfuse, Prompt Registry 폐쇄형 프롬프트 모니터링 및 개선 루프 다이어그램" style="display:block;font-family:var(--sans)">
        <defs>
          <marker id="arr-dark" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M0,1.5 L9,5 L0,8.5 z" fill="#3A4766"/>
          </marker>
          <marker id="arr-mint" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
            <path d="M0,1.5 L9,5 L0,8.5 z" fill="#12B07A"/>
          </marker>
          <filter id="card-sh" x="-4%" y="-6%" width="108%" height="118%">
            <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F1B3D" flood-opacity="0.10"/>
          </filter>
        </defs>

        <!-- 배경 루프 영역 가이드 -->
        <rect x="12" y="12" width="1696" height="536" rx="28" fill="#F3EDE6" stroke="rgba(15,27,61,.12)" stroke-width="2"/>

        <!-- 01. LangGraph -->
        <g filter="url(#card-sh)">
          <rect x="44" y="48" width="350" height="270" rx="22" fill="#FFFFFF" stroke="#2F6BFF" stroke-width="2.5"/>
          <rect x="68" y="70" width="196" height="34" rx="17" fill="#DCE6FF"/>
          <text x="166" y="93" text-anchor="middle" font-size="16" font-weight="800" fill="#1E4FD0">01 · ORCHESTRATION</text>
          <text x="68" y="142" font-size="34" font-weight="850" fill="#0F1B3D">LangGraph</text>
          <!-- 내부 StateGraph 미니 다이어그램 -->
          <rect x="68" y="166" width="88" height="44" rx="10" fill="#EFF4FF" stroke="#2F6BFF" stroke-width="1.5"/>
          <text x="112" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#1E4FD0">Planner</text>
          <line x1="156" y1="188" x2="176" y2="188" stroke="#2F6BFF" stroke-width="2.5" marker-end="url(#arr-dark)"/>
          <rect x="178" y="166" width="84" height="44" rx="10" fill="#EFF4FF" stroke="#2F6BFF" stroke-width="1.5"/>
          <text x="220" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#1E4FD0">Agent</text>
          <line x1="262" y1="188" x2="282" y2="188" stroke="#2F6BFF" stroke-width="2.5" marker-end="url(#arr-dark)"/>
          <rect x="284" y="166" width="86" height="44" rx="10" fill="#EFF4FF" stroke="#2F6BFF" stroke-width="1.5"/>
          <text x="327" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#1E4FD0">Verify</text>
          <text x="68" y="250" font-size="19" font-weight="600" fill="#3A4766">StateGraph 상태 전이 · 분기</text>
          <text x="68" y="280" font-size="17" font-weight="600" fill="#6A728A" font-family="var(--mono)">ch06 ~ ch10 워크플로</text>
        </g>

        <!-- Arrow 1 -> 2 -->
        <line x1="396" y1="183" x2="466" y2="183" stroke="#3A4766" stroke-width="4" marker-end="url(#arr-dark)"/>
        <text x="431" y="164" text-anchor="middle" font-size="15" font-weight="700" fill="#3A4766">LLM 호출</text>

        <!-- 02. LiteLLM Proxy -->
        <g filter="url(#card-sh)">
          <rect x="472" y="48" width="330" height="270" rx="22" fill="#FFFFFF" stroke="#7C5CFF" stroke-width="2.5"/>
          <rect x="496" y="70" width="204" height="34" rx="17" fill="#E6E0FF"/>
          <text x="598" y="93" text-anchor="middle" font-size="16" font-weight="800" fill="#4D2FD0">02 · ZERO-CODE PROXY</text>
          <text x="496" y="142" font-size="34" font-weight="850" fill="#0F1B3D">LiteLLM Proxy</text>
          <rect x="496" y="166" width="88" height="42" rx="21" fill="#F3F0FF" stroke="#7C5CFF" stroke-width="1.5"/>
          <text x="540" y="193" text-anchor="middle" font-size="16" font-weight="700" fill="#4D2FD0">Claude</text>
          <rect x="592" y="166" width="94" height="42" rx="21" fill="#F3F0FF" stroke="#7C5CFF" stroke-width="1.5"/>
          <text x="639" y="193" text-anchor="middle" font-size="16" font-weight="700" fill="#4D2FD0">ChatGPT</text>
          <rect x="694" y="166" width="84" height="42" rx="21" fill="#F3F0FF" stroke="#7C5CFF" stroke-width="1.5"/>
          <text x="736" y="193" text-anchor="middle" font-size="16" font-weight="700" fill="#4D2FD0">Gemini</text>
          <text x="496" y="250" font-size="19" font-weight="600" fill="#3A4766">코드 수정 없는 통합 관측</text>
          <text x="496" y="280" font-size="17" font-weight="600" fill="#6A728A" font-family="var(--mono)">success_callback: langfuse</text>
        </g>

        <!-- Arrow 2 -> 3 -->
        <line x1="804" y1="183" x2="874" y2="183" stroke="#3A4766" stroke-width="4" marker-end="url(#arr-dark)"/>
        <text x="839" y="164" text-anchor="middle" font-size="15" font-weight="700" fill="#3A4766">Trace 전송</text>

        <!-- 03. Langfuse Monitoring & Eval -->
        <g filter="url(#card-sh)">
          <rect x="880" y="48" width="370" height="270" rx="22" fill="#FFFFFF" stroke="#F5A524" stroke-width="2.5"/>
          <rect x="904" y="70" width="228" height="34" rx="17" fill="#FDEFD3"/>
          <text x="1018" y="93" text-anchor="middle" font-size="16" font-weight="800" fill="#9A5B00">03 · MONITORING &amp; EVAL</text>
          <text x="904" y="142" font-size="34" font-weight="850" fill="#0F1B3D">Langfuse</text>
          <rect x="904" y="166" width="102" height="44" rx="10" fill="#FFF8EB" stroke="#F5A524" stroke-width="1.5"/>
          <text x="955" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#9A5B00">Traces</text>
          <rect x="1014" y="166" width="102" height="44" rx="10" fill="#FFF8EB" stroke="#F5A524" stroke-width="1.5"/>
          <text x="1065" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#9A5B00">Latency/Cost</text>
          <rect x="1124" y="166" width="102" height="44" rx="10" fill="#FFF8EB" stroke="#F5A524" stroke-width="1.5"/>
          <text x="1175" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#9A5B00">3-Tier Evals</text>
          <text x="904" y="250" font-size="19" font-weight="600" fill="#3A4766">실패·환각 추적 및 자동 채점</text>
          <text x="904" y="280" font-size="17" font-weight="600" fill="#6A728A" font-family="var(--mono)">Code · LLM-Judge · Human</text>
        </g>

        <!-- Arrow 3 -> 4 -->
        <line x1="1252" y1="183" x2="1322" y2="183" stroke="#3A4766" stroke-width="4" marker-end="url(#arr-dark)"/>
        <text x="1287" y="164" text-anchor="middle" font-size="15" font-weight="700" fill="#3A4766">승격</text>

        <!-- 04. Prompt Registry -->
        <g filter="url(#card-sh)">
          <rect x="1328" y="48" width="348" height="270" rx="22" fill="#FFFFFF" stroke="#12B07A" stroke-width="2.5"/>
          <rect x="1352" y="70" width="218" height="34" rx="17" fill="#D5F2E6"/>
          <text x="1461" y="93" text-anchor="middle" font-size="16" font-weight="800" fill="#0B8A5F">04 · PROMPT REGISTRY</text>
          <text x="1352" y="142" font-size="34" font-weight="850" fill="#0F1B3D">Prompt v2+</text>
          <rect x="1352" y="166" width="144" height="44" rx="10" fill="#EAFBF3" stroke="#12B07A" stroke-width="1.5"/>
          <text x="1424" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#0B8A5F">Save as Prompt</text>
          <rect x="1506" y="166" width="146" height="44" rx="10" fill="#0F1B3D"/>
          <text x="1579" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#4BE3A6">production</text>
          <text x="1352" y="250" font-size="19" font-weight="600" fill="#3A4766">프롬프트 버전 관리 · 라벨 배포</text>
          <text x="1352" y="280" font-size="17" font-weight="600" fill="#6A728A" font-family="var(--mono)">trace_to_prompt · fetch_prompt</text>
        </g>

        <!-- 하단 폐쇄형 피드백 루프 (04 -> 01) -->
        <path d="M 1502 320 L 1502 440 Q 1502 464 1478 464 L 244 464 Q 219 464 219 440 L 219 328"
              fill="none" stroke="#12B07A" stroke-width="5" stroke-linecap="round" marker-end="url(#arr-mint)"/>
        <!-- Eval에서 피드백 합류 점선 -->
        <path d="M 1065 320 L 1065 440 Q 1065 464 1041 464"
              fill="none" stroke="#F5A524" stroke-width="3.5" stroke-dasharray="8 6"/>

        <!-- 중앙 피드백 허브 배지 -->
        <rect x="520" y="422" width="680" height="84" rx="42" fill="#0F1B3D" stroke="#4BE3A6" stroke-width="2.5"/>
        <text x="860" y="458" text-anchor="middle" font-size="21" font-weight="800" fill="#4BE3A6">CLOSED-LOOP IMPROVEMENT (무중단 프롬프트 개선)</text>
        <text x="860" y="488" text-anchor="middle" font-size="17" font-weight="600" fill="#DCE3F5" font-family="var(--mono)">fetch_prompt(name, label="production") → 재배포 없이 즉시 반영</text>

        <!-- 하단 3대 핵심 요약 바 -->
        <rect x="12" y="576" width="548" height="128" rx="20" fill="#FFFFFF" stroke="rgba(15,27,61,.14)" stroke-width="2"/>
        <text x="40" y="618" font-size="22" font-weight="800" fill="#1E4FD0">① 상태 그래프 제어</text>
        <text x="40" y="654" font-size="19" font-weight="600" fill="#3A4766">LangGraph 노드가 최신 프롬프트를 주입해</text>
        <text x="40" y="682" font-size="19" font-weight="600" fill="#3A4766">결정론적 루프와 분기를 실행.</text>

        <rect x="586" y="576" width="548" height="128" rx="20" fill="#FFFFFF" stroke="rgba(15,27,61,.14)" stroke-width="2"/>
        <text x="614" y="618" font-size="22" font-weight="800" fill="#9A5B00">② 실시간 모니터링 &amp; 채점</text>
        <text x="614" y="654" font-size="19" font-weight="600" fill="#3A4766">LiteLLM → Langfuse로 Trace를 수집하고</text>
        <text x="614" y="682" font-size="19" font-weight="600" fill="#3A4766">3종 Eval로 품질 회귀를 탐지.</text>

        <rect x="1160" y="576" width="548" height="128" rx="20" fill="#FFFFFF" stroke="rgba(15,27,61,.14)" stroke-width="2"/>
        <text x="1188" y="618" font-size="22" font-weight="800" fill="#0B8A5F">③ Trace → Prompt 자산화</text>
        <text x="1188" y="654" font-size="19" font-weight="600" fill="#3A4766">우수/개선 Trace를 Save as Prompt로 승격해</text>
        <text x="1188" y="682" font-size="19" font-weight="600" fill="#3A4766">production 라벨로 즉시 되먹임.</text>
      </svg>`;
      A(wrap, 'up', 0.12, { dur: 0.5 });
    },
  });

  // 3. 커리큘럼 로드맵 + 4계층 12대 스택
  DECK.slide({
    id: 'timetable',
    part: 'opening',
    chap: '전체 로드맵',
    theme: 'paper',
    title: '커리큘럼 로드맵 & 4계층 12대 스택',
    notes: '총 6블록으로 구성되어 있으며, 각 단원마다 실습+모범답안 슬라이드가 1:1로 배치되어 있습니다.',
    build(el, A) {
      const T = title(el, 'WORKSHOP CURRICULUM', '커리큘럼 로드맵 & <span class="hl">4계층 12대 스택</span>', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 225, w: 940, h: 740, pad: 30 });
      c1.innerHTML = `<div class="h4" style="margin-bottom:16px">워크숍 모듈 구성 (13개 챕터)</div>
      <table class="tbl tbl-timetable">
        <thead><tr><th>블록</th><th>단원 범위</th><th>핵심 주제 & 실습</th><th>모듈</th></tr></thead>
        <tbody>
          <tr><td><b>Intro</b></td><td><code>ch00</code></td><td>4계층 12대 스택 &amp; Any-Platform 환경 진단</td><td><b>1개</b></td></tr>
          <tr><td><b>Part 1</b></td><td><code>ch01 ~ ch03</code></td><td>에이전트 루프 · MCP &amp; Hooks · 3단계 Skills</td><td><b>3개</b></td></tr>
          <tr><td><b>Part 2</b></td><td><code>ch04 ~ ch05</code></td><td>7항목 프롬프트 · 컨텍스트 예산 · Agentic RAG &amp; Memory</td><td><b>2개</b></td></tr>
          <tr><td><b>Part 3</b></td><td><code>ch06 ~ ch08</code></td><td>서브에이전트 · 하네스 가드레일 · Ralph Loop &amp; <code>/goal</code></td><td><b>3개</b></td></tr>
          <tr><td><b>Part 4A</b></td><td><code>ch09 ~ ch10</code></td><td>3-Agent 블라인드 합의 · 5단계 아우터 루프</td><td><b>2개</b></td></tr>
          <tr><td><b>Part 4B</b></td><td><code>ch11 ~ ch12</code></td><td>LiteLLM + Langfuse Save as Prompt · Eval · Stage 1~4</td><td><b>2개</b></td></tr>
        </tbody>
      </table>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 1070, y: 225, w: 750, h: 740, pad: 30 });
      c2.innerHTML = `<div class="h4" style="margin-bottom:18px">LLM을 감싸는 4계층(Layer 1~4)</div>
      <div class="col" style="gap:16px">
        <div style="padding:18px 20px;border-radius:16px;background:var(--violet-l)">
          <div class="cap" style="color:var(--violet)">Layer 1 · 지식과 기억 (ch04, ch05)</div>
          <div class="b3" style="color:var(--ink);margin-top:4px">① 프롬프트·컨텍스트 · ② Agentic RAG · ③ 지속 Memory</div>
        </div>
        <div style="padding:18px 20px;border-radius:16px;background:var(--blue-l)">
          <div class="cap" style="color:var(--blue-d)">Layer 2 · 행동과 도구 (ch01, ch02)</div>
          <div class="b3" style="color:var(--ink);margin-top:4px">④ 에이전트 루프 · ⑤ MCP · ⑥ Hooks 가드레일</div>
        </div>
        <div style="padding:18px 20px;border-radius:16px;background:var(--green-l)">
          <div class="cap" style="color:var(--green-d)">Layer 3 · 표준과 확장 (ch03, ch04, ch07)</div>
          <div class="b3" style="color:var(--ink);margin-top:4px">⑦ 상시 지침 · ⑧ 온디맨드 Skills · ⑨ 하네스 린터</div>
        </div>
        <div style="padding:18px 20px;border-radius:16px;background:var(--amber-l)">
          <div class="cap" style="color:#9A5B00">Layer 4 · 위임과 검증 (ch06, ch08~11)</div>
          <div class="b3" style="color:var(--ink);margin-top:4px">⑩ 서브에이전트 · ⑪ 이너/아우터 루프 · ⑫ Eval/LLMOps</div>
        </div>
      </div>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // 4. Any-Platform 아키텍처 (Claude · ChatGPT · Gemini)
  DECK.slide({
    id: 'any-platform',
    part: 'opening',
    chap: 'Any-Platform 어댑터',
    theme: 'white',
    title: 'Any-Platform 공용 실행 (Claude · ChatGPT · Gemini)',
    notes: '모든 단원 코드가 platforms/ 공용 어댑터를 통해 Claude, ChatGPT, Gemini 및 키 없는 Offline 폴백으로 동일하게 동작합니다.',
    build(el, A) {
      const T = title(el, 'CROSS-PLATFORM DESIGN', '어느 AI 플랫폼에서도 동작하는 <span class="hb">Any-Platform</span> 설계', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const cards = [
        ['Claude Code', 'CLAUDE.md · .claude/', 'adapter_claude.py', '*_claude.json / *_claude.py', '#E6E0FF', '#4D2FD0'],
        ['ChatGPT / Codex', 'AGENTS.md · CHATGPT.md', 'adapter_chatgpt.py', '*_chatgpt.yaml / *_chatgpt.py', '#D5F2E6', '#0B8A5F'],
        ['Gemini / Antigravity (agy)', 'GEMINI.md · .gemini/', 'adapter_gemini.py', '*_gemini.json / *_gemini.py', '#DCE6FF', '#1E4FD0'],
      ];
      cards.forEach(([name, entry, adp, files, bg, fg], i) => {
        const c = card(el, { x: 100 + i * 585, y: 230, w: 550, h: 330, pad: 30 });
        c.innerHTML = `<span class="chip" style="background:${bg};color:${fg}">${name}</span>
          <div class="h4" style="margin-top:18px">${entry}</div>
          <div class="b3" style="margin-top:14px">어댑터: <code>platforms/${adp}</code></div>
          <div class="b3" style="margin-top:8px">패턴 파일: <code>${files}</code></div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });

      const w = win(el, { x: 100, y: 600, w: 1720, h: 365, dark: true, title: 'platforms/base.py — 플랫폼 자동 감지 & 100% 오프라인 폴백' });
      w.body.innerHTML = `<div class="term"><span class="p">$</span>AGENT_PLATFORM=claude python3 ch06-subagents-workflow/dynamic_workflow.py --platform claude --json
<span class="o">-> claude (키 미설정 시 deterministic offline 시뮬레이터로 자동 폴백)</span>
<span class="p">$</span>AGENT_PLATFORM=chatgpt python3 ch10-outer-loop/loop.py --platform chatgpt
<span class="p">$</span>AGENT_PLATFORM=gemini python3 ch11-eval-and-llmops/fetch_prompt.py --demo --json
<span class="ok">[OK] claude / chatgpt / gemini 3종 모두 API 키 없이 동일 테스트 스위트 통과</span></div>`;
      A(w.el, 'up', 0.34, { dur: 0.45 });
    },
  });

  // 5. 저장소 & GitHub Pages 구조
  DECK.slide({
    id: 'repo-tree',
    part: 'opening',
    chap: 'ch00 구조 안내',
    theme: 'ink',
    dots: true,
    title: '저장소 구조 & GitHub Pages(docs/) 구성',
    notes: '도서 호환 심볼릭 링크(ch01~ch11)와 정식 디렉터리(ch00-prologue~ch12-epilogue), 그리고 docs/ 웹 PPT가 공존합니다.',
    build(el, A) {
      const T = title(el, 'REPOSITORY MAP', '저장소 구조 & <span class="hl">GitHub Pages</span> 정적 번들', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const w1 = win(el, { x: 100, y: 225, w: 840, h: 735, dark: true, title: '/apps/learn_Loop_engineering (Tree)' });
      w1.body.innerHTML = `<pre class="tree" style="background:transparent;border:0;padding:0;font-size:21px"><code>learn_Loop_engineering/
├── AGENTS.md / CLAUDE.md / CHATGPT.md / GEMINI.md
├── platforms/                  # Claude · ChatGPT · Gemini 공용 어댑터
├── scripts/verify_chapters.py  # 전 단원 &amp; 웹 PPT 통합 검증
├── docs/                       # GitHub Pages 루트 (상대경로 100%)
│   ├── .nojekyll               # Jekyll 우회
│   ├── ARCHITECTURE.md         # 4계층 12대 스택 설계서 보존
│   ├── index.html / presenter.html
│   ├── deck.css / engine.js / ui.js
│   └── slides/ (00_manifest, s0..s5)
├── ch00-prologue/ ~ ch12-epilogue/  # 정식 단원 코드
└── ch01/ ~ ch11/               # 도서 『💻 Git 예제』 호환 심볼릭 링크</code></pre>`;
      A(w1.el, 'up', 0.12, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 225, w: 840, h: 735, pad: 34 });
      c2.innerHTML = `<div class="h3" style="margin-bottom:20px">이 웹 PPT의 3가지 실습 원칙</div>
      <div class="col" style="gap:20px">
        <div style="padding:20px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12)">
          <div class="h4"><span class="hl">01.</span> 한 페이지 실습 + 클릭 답안</div>
          <div class="b3" style="margin-top:8px">단원마다 왼쪽에 실습 미션·실행 명령을, 오른쪽에 네이티브 <code>&lt;details&gt;</code> 모범 답안을 배치했습니다.</div>
        </div>
        <div style="padding:20px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12)">
          <div class="h4"><span class="hl">02.</span> Tree + 핵심 구현 동시 제공</div>
          <div class="b3" style="margin-top:8px">답안을 클릭하면 필요한 디렉터리 Tree와 핵심 코드·예상 출력이 즉시 펼쳐집니다. (단축키 <code>A</code> 지원)</div>
        </div>
        <div style="padding:20px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12)">
          <div class="h4"><span class="hl">03.</span> GitHub Pages 무빌드 배포</div>
          <div class="b3" style="margin-top:8px">Repository Settings → Pages → Source: <code>main /docs</code> 또는 <code>develop /docs</code> 지정만으로 즉시 실행됩니다.</div>
        </div>
      </div>`;
      A(c2, 'up', 0.22, { dur: 0.45 });
    },
  });

  // 6. ch00 실습 + 모범 답안
  DECK.slide({
    id: 'ch00-lab',
    part: 'opening',
    chap: 'ch00 실습 & 답안',
    theme: 'paper',
    title: 'ch00 실습: 4계층 12대 스택 & Any-Platform 환경 진단',
    notes: '수강생들에게 stack_check.py와 verify_chapters.py를 먼저 실행하게 한 뒤, 우측 모범 답안을 클릭해 구조와 JSON 출력을 확인하게 합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch00',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더의 AGENTS.md · CLAUDE.md · GEMINI.md 지침을 확인하고 4계층 12대 스택 환경 및 플랫폼 어댑터 진단 결과를 출력해줘.

1) 프롬프트 1 (스택 진단): python3 stack_check.py --json 을 실행해 Python 버전, SQLite FTS5 지원, 4계층(4)/12대 요소(12) 준비 상태를 요약해줘.
2) 프롬프트 2 (플랫폼 점검): AGENT_PLATFORM=offline python3 agent_check.py --json 으로 claude/chatgpt/gemini 오프라인 폴백 응답을 확인해줘.
3) 프롬프트 3 (단위 테스트): python3 -m unittest discover -s tests -p "test_*.py" -v 를 실행해 전체 테스트 통과 여부를 출력해줘.`,
        kicker: 'CH00 PROLOGUE · HANDS-ON LAB',
        heading: '프롤로그 실습: 4계층 스택 진단 & <span class="hl">플랫폼 감지</span>',
        duration: '',
        missionTitle: '챕터 폴더 이동 후 AI CLI 접속 → 사용자 프롬프트로 스택·플랫폼 진단',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서와 플랫폼 폴더, <code>stack_check.py</code> · <code>agent_check.py</code>를 구성.',
          '<code>해당 챕터 폴더로 이동 후 AI CLI 접속</code><br>터미널에서 챕터 폴더로 이동한 뒤 <code>claude</code> · <code>agy</code> · <code>codex</code> CLI를 실행.',
          '<code>사용자 입력 프롬프트로 진단 결과 출력</code><br>아래 3가지 프롬프트 예시(또는 단축키 A 통합 프롬프트)를 입력해 JSON 결과를 확인.',
        ],
        promptExamples: [
          '1) "현재 폴더의 stack_check.py --json을 실행해 4계층 12대 스택과 FTS5 준비 상태를 요약해줘."',
          '2) "agent_check.py로 claude·chatgpt·gemini·offline 폴백 동작을 점검하고 JSON으로 보여줘."',
          '3) "tests/ 단위 테스트를 전체 실행해 모든 항목이 OK인지 검증 리포트를 출력해줘."',
        ],
        runCmd: 'python3 stack_check.py --json\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI에 사용자 프롬프트를 입력하면 <code>stack_check.py</code>와 단위 테스트를 실행해 <code>overall_ready: true</code> 결과를 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/prologue.md · .gemini/settings.json
├── stack_check.py
├── agent_check.py
└── tests/ (test_stack_check.py, test_agent_check.py)`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (stack_check.py --json)',
        answerCode: `{
  "python_version": "3.13.16",
  "sqlite_fts5": true,
  "platforms_supported": ["claude", "chatgpt", "gemini"],
  "layers_count": 4,
  "elements_count": 12,
  "overall_ready": true
}`,
      });
    },
  });
})();
