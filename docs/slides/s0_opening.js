(function () {
  const { h } = DECK;
  const { title, card, win, chip, text, buildLabSlide } = UI;

  // 1. 표지 (No Chrome)
  DECK.slide({
    id: 'cover',
    part: 'opening',
    chap: '5시간 완성 부트캠프',
    theme: 'night',
    dots: true,
    noChrome: true,
    title: '2026 모던 AI 에이전트 스택 & Hermes Engineering (5시간 과정)',
    notes: '총 300분(5시간) 실전 강의. 각 단원(ch00~ch12)의 이론을 익힌 뒤, 바로 다음 한 페이지에서 실습 미션과 클릭 토글 모범 답안을 확인합니다.',
    build(el, A) {
      const tag = h('div', 'row abs', el);
      tag.style.cssText = 'left:110px;top:96px;gap:14px';
      chip(tag, '5시간 (300분) 실전 워크숍', { bg: 'rgba(75,227,166,.16)', fg: '#4BE3A6' });
      chip(tag, 'GitHub Pages · Web PPT', { bg: 'rgba(47,107,255,.22)', fg: '#9DBBFF' });
      chip(tag, 'Claude · ChatGPT · Gemini 공용', { bg: 'rgba(124,92,255,.22)', fg: '#C7B8FF' });
      A(tag, 'fade', 0, { dur: 0.4 });

      const hero = h('div', 'abs', el);
      hero.style.cssText = 'left:110px;top:210px;width:1280px';
      h('div', 'h1', hero, '2026 모던 AI 에이전트 스택<br><span class="hl">Hermes Engineering</span>');
      h('div', 'b1', hero, '프롤로그(ch00)부터 LLMOps·로드맵(ch12)까지 —<br>이론 · 단원별 실습 · 클릭형 모범 답안을 <b>한 화면에서</b> 완주하는 5시간 웹 PPT').style.cssText = 'margin-top:32px;color:#AEB8D3';
      A(hero, 'up', 0.12, { dur: 0.55 });

      const w = win(el, { x: 110, y: 635, w: 1700, h: 280, dark: true, title: 'quickstart.sh — 키보드 조작 & 컨테이너 환경' });
      w.body.innerHTML = `<div class="term"><span class="p">$</span><span class="ok">docker exec -it graphrag_agent_app_fullstack bash</span>
<span class="p">$</span>cd /apps/learn_hermes_engineering && python3 scripts/verify_chapters.py --all
<span class="o"># 웹 PPT 단축키: → / Space(다음) · ←(이전) · A(모범답안 열기/닫기) · O(전체 목차) · N(발표자 메모) · P(발표자 창) · ?print(PDF)</span></div>`;
      A(w.el, 'up', 0.28, { dur: 0.5 });
    },
  });

  // 2. 5시간 (300분) 커리큘럼 타임테이블 + 4계층 12대 스택
  DECK.slide({
    id: 'timetable',
    part: 'opening',
    chap: '전체 로드맵',
    theme: 'paper',
    title: '5시간(300분) 커리큘럼 & 4계층 12대 스택',
    notes: '총 5블록으로 휴식 포함 5시간을 운영합니다. 각 단원마다 실습+모범답안 슬라이드가 1:1로 배치되어 있습니다.',
    build(el, A) {
      const T = title(el, '5-HOUR CURRICULUM', '5시간(300분) 커리큘럼 & <span class="hl">4계층 12대 스택</span>', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 225, w: 940, h: 740, pad: 30 });
      c1.innerHTML = `<div class="h4" style="margin-bottom:16px">시간 배분 타임테이블 (총 300분)</div>
      <table class="tbl">
        <thead><tr><th>시간 블록</th><th>단원 범위</th><th>핵심 주제 & 실습</th><th>배분</th></tr></thead>
        <tbody>
          <tr><td><b>Intro</b></td><td><code>ch00</code></td><td>4계층 12대 스택 &amp; Any-Platform 환경 진단</td><td><b>30분</b></td></tr>
          <tr><td><b>Part 1</b></td><td><code>ch01 ~ ch03</code></td><td>에이전트 루프 · MCP &amp; Hooks · 3단계 Skills</td><td><b>75분</b></td></tr>
          <tr><td><b>Part 2</b></td><td><code>ch04 ~ ch05</code></td><td>7항목 프롬프트 · 컨텍스트 예산 · Agentic RAG &amp; Memory</td><td><b>45분</b></td></tr>
          <tr><td><b>Part 3</b></td><td><code>ch06 ~ ch08</code></td><td>서브에이전트 · 하네스 가드레일 · Ralph Loop &amp; <code>/goal</code></td><td><b>65분</b></td></tr>
          <tr><td><b>Part 4A</b></td><td><code>ch09 ~ ch10</code></td><td>3-Agent 블라인드 합의 · 5단계 아우터 루프</td><td><b>45분</b></td></tr>
          <tr><td><b>Part 4B</b></td><td><code>ch11 ~ ch12</code></td><td>LiteLLM + Langfuse Save as Prompt · Eval · Stage 1~4</td><td><b>40분</b></td></tr>
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

  // 3. Any-Platform 아키텍처 (Claude · ChatGPT · Gemini)
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
        ['Gemini / Antigravity', 'GEMINI.md · .gemini/', 'adapter_gemini.py', '*_gemini.json / *_gemini.py', '#DCE6FF', '#1E4FD0'],
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
      w.body.innerHTML = `<div class="term"><span class="p">$</span>AGENT_PLATFORM=claude python3 ch06/quote-cli/quote_agent.py --platform claude
<span class="o">-> claude (키 미설정 시 deterministic offline 시뮬레이터로 자동 폴백)</span>
<span class="p">$</span>AGENT_PLATFORM=chatgpt python3 ch10/todo-loop/loop.py --platform chatgpt --check
<span class="p">$</span>AGENT_PLATFORM=gemini python3 ch11/support-assistant/run_evals.py --platform gemini
<span class="ok">[OK] claude / chatgpt / gemini 3종 모두 API 키 없이 동일 테스트 스위트 통과</span></div>`;
      A(w.el, 'up', 0.34, { dur: 0.45 });
    },
  });

  // 4. 저장소 & GitHub Pages 구조
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

      const w1 = win(el, { x: 100, y: 225, w: 840, h: 735, dark: true, title: '/apps/learn_hermes_engineering (Tree)' });
      w1.body.innerHTML = `<pre class="tree" style="background:transparent;border:0;padding:0;font-size:21px"><code>learn_hermes_engineering/
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

  // 5. ch00 실습 + 모범 답안
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
        kicker: 'CH00 PROLOGUE · HANDS-ON LAB',
        heading: '프롤로그 실습: 4계층 스택 진단 & <span class="hl">플랫폼 감지</span>',
        duration: '15분',
        missionTitle: '컨테이너 런타임, SQLite FTS5, 3대 플랫폼 어댑터 상태 점검',
        steps: [
          '<code>ch00-prologue/stack_check.py</code>를 일반 모드와 <code>--json</code> 모드로 실행해 12대 스택 준비 상태를 확인한다.',
          '<code>AGENT_PLATFORM</code> 환경 변수를 <code>claude</code>, <code>chatgpt</code>, <code>gemini</code>로 바꿔 어댑터 로드를 검증한다.',
          '<code>tests/test_repo_root.py</code>를 실행해 <code>AGENTS.md</code> 100줄 제한 및 레거시 부재를 확인한다.',
        ],
        runCmd: 'python3 ch00-prologue/stack_check.py --json\npython3 -m unittest discover -s platforms/tests -p "test_*.py" -v',
        answerLabel: 'ch00 모범 답안 열기 (Tree + 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>stack_check.py</code>는 Python 3.13+, SQLite FTS5, Git, Node 런타임 및 4계층 디렉터리 존재 여부를 점검하고 <code>overall_ready: true</code>를 반환합니다.',
        tree: `learn_hermes_engineering/
├── AGENTS.md (<= 100줄) · CLAUDE.md · CHATGPT.md · GEMINI.md
├── platforms/
│   ├── base.py (get_adapter)
│   ├── adapter_claude.py
│   ├── adapter_chatgpt.py
│   └── adapter_gemini.py
└── ch00-prologue/
    ├── stack_check.py
    └── tests/test_stack_check.py`,
        codeCaption: 'stack_check.py --json 핵심 출력 예시',
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
