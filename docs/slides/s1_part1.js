(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 1 Divider
  DECK.slide({
    id: 'p1-div',
    part: 'p1',
    chap: 'Part 1 시작',
    theme: 'blue',
    title: 'Part 1 · 행동과 확장 (ch01 ~ ch03, 75분)',
    notes: 'Part 1은 에이전트 루프(ch01), MCP와 Hooks 가드레일(ch02), 온디맨드 3단계 Skills(ch03)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 1 · 75분', { bg: 'rgba(255,255,255,.2)', fg: '#fff' });
      h('div', 'h1', box, '행동, 도구 연결, 그리고<br>팀 워크플로의 표준화').style.cssText = 'margin-top:24px;color:#fff';
      h('div', 'b1', box, 'ch01 에이전트 루프 · ch02 MCP &amp; Hooks · ch03 3단계 Skills').style.cssText = 'margin-top:28px;color:#DCE6FF';
      A(box, 'up', 0, { dur: 0.5 });
    },
  });

  // ch01 이론
  DECK.slide({
    id: 'ch01-theory',
    part: 'p1',
    chap: 'ch01 에이전트 루프',
    theme: 'paper',
    title: 'ch01: 바이브 코딩 vs 에이전틱 코딩 & 5단계 루프',
    notes: '도서 호환 경로 ch01/quote-cli/와 정식 경로 ch01-agentic-coding/quote-cli/가 심볼릭 링크로 연결되어 있습니다.',
    build(el, A) {
      const T = title(el, 'CH01 · AGENTIC CODING LOOP', '바이브 코딩과 <span class="hb">에이전틱 코딩</span>의 결정적 차이', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 830, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">바이브 코딩 vs 에이전틱 코딩</div>
      <div class="col" style="gap:18px;margin-top:24px">
        <div style="padding:20px;border-radius:16px;background:var(--red-l)">
          <div class="cap" style="color:var(--red)">Vibe Coding (단발 프롬프트)</div>
          <div class="b3" style="color:var(--ink);margin-top:6px">코드 복사-붙여넣기 반복 → 테스트·환경 검증 누락 → 기술 부채 급증</div>
        </div>
        <div style="padding:20px;border-radius:16px;background:var(--green-l)">
          <div class="cap" style="color:var(--green-d)">Agentic Coding (폐쇄 루프 검증)</div>
          <div class="b3" style="color:var(--ink);margin-top:6px">요구사항 분해 → 도구로 파일 수정 → 테스트 실행 → 실패 시 스스로 수정</div>
        </div>
      </div>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 970, y: 230, w: 850, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">Quote CLI 4대 실습 기능</div>
      <ul class="lab-steps" style="margin-top:20px">
        <li><code>--all</code> / <code>--tag &lt;태그&gt;</code><br><code>quotes.json</code> 기반 전체·태그 필터링 결과를 출력.</li>
        <li><code>--author &lt;저자&gt;</code> / <code>--json</code><br>저자별 필터링과 구조화 JSON 출력 포맷을 확인.</li>
        <li><code>--seed &lt;숫자&gt;</code><br>결정론적 시드 기반 랜덤 명언을 추출.</li>
        <li><code>interactive_demo.py</code><br>REPL 대화형 루프 데모를 실행해 입력 흐름을 점검.</li>
      </ul>
      <div class="answer-hint" style="margin-top:28px">호환 경로: <code>ch01/quote-cli/</code> → <code>ch01-agentic-coding/quote-cli/</code> (동일 코드)</div>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch01 실습 + 모범 답안
  DECK.slide({
    id: 'ch01-lab',
    part: 'p1',
    chap: 'ch01 실습 & 답안',
    theme: 'white',
    title: 'ch01 실습: Quote CLI 필터·랜덤 모드 및 테스트 실행',
    notes: 'Quote CLI를 실행하고 unittest 통과 여부를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch01',
        userPrompt: `[실습 결과 실행 프롬프트 — quote-cli/ 폴더에서 AI CLI에 입력]
현재 quote-cli 프로젝트 폴더에서 에이전트 루프(수집 -> 실행 -> 검증)를 거쳐 아래 실습 결과를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 quotes.json, quote_cli.py, tests/test_quote_cli.py를 먼저 작성)
   - python3 quote-cli/quote_cli.py --tag engineering --json
   - python3 quote-cli/quote_cli.py --seed 42 --json
   - python3 -m unittest discover -s quote-cli/tests -p "test_*.py" -v

2. 출력 요구사항
   - engineering 태그 필터링 JSON 결과, 시드 42 결정론적 출력, 단위 테스트 통과 건수를 함께 출력할 것.`,
        kicker: 'CH01 · HANDS-ON LAB (20분)',
        heading: '제1장 실습: <span class="hl">Quote CLI</span> 루프 작성 &amp; 결과 출력',
        duration: '20분',
        missionTitle: 'quote-cli/ 폴더에 명언 CLI 작성 후 AI CLI 프롬프트로 실행·검증 결과 출력',
        steps: [
          '<code>quote-cli/quotes.json</code> · <code>quote_cli.py</code><br>명언 데이터와 <code>--tag</code>·<code>--seed</code>·<code>--json</code> 지원 CLI를 작성.',
          '<code>quote-cli/interactive_demo.py</code> · <code>tests/</code><br>대화형 REPL 데모와 표준 <code>unittest</code> 검증 스위트를 구성.',
          '<code>quote-cli/ 에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 태그 필터 JSON과 테스트 통과 결과를 출력.',
        ],
        runCmd: 'python3 quote-cli/quote_cli.py --tag engineering --json\npython3 -m unittest discover -s quote-cli/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>quote-cli/</code> 폴더에서 AI CLI가 코드를 읽고 실행·검증 루프를 돌아 태그 필터 JSON과 테스트 결과를 반환합니다.',
        tree: `quote-cli/
├── quotes.json               # 명언 데이터 (engineering 태그 포함)
├── quote_cli.py              # --all / --tag / --seed / --json
├── interactive_demo.py       # REPL 대화형 루프 데모
└── tests/test_quote_cli.py   # 단위 테스트`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (quote_cli.py --tag engineering --json)',
        answerCode: `[
  {
    "id": 1,
    "text": "Tests are the compass of agentic coding.",
    "author": "Loop Handbook",
    "tags": ["engineering", "testing"]
  }
]
# Ran 6 tests in 0.01s — OK`,
      });
    },
  });

  // ch02 이론
  DECK.slide({
    id: 'ch02-theory',
    part: 'p1',
    chap: 'ch02 MCP & Hooks',
    theme: 'ink',
    dots: true,
    title: 'ch02: MCP 도구 표준화 & PreToolUse/PostToolUse 훅 가드레일',
    notes: '도구 연결(MCP)만으로는 rm -rf 같은 위험 명령을 막기 어렵습니다. 결정론적 Python 훅과 멀티 플랫폼 설정 파일을 함께 다룹니다.',
    build(el, A) {
      const T = title(el, 'CH02 · MCP & HOOKS', '<span class="hl">MCP</span> 도구 프로토콜 + 결정론적 <span class="hl">Hooks</span> 가드레일', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const w1 = win(el, { x: 100, y: 225, w: 840, h: 720, dark: true, title: 'ch02/quote-mcp/hooks/block_dangerous_bash.py' });
      w1.body.innerHTML = `<div class="term"><span class="o"># PreToolUse 훅: 위험 명령어 차단 (exit code 2)</span>
DANGEROUS_PATTERNS = [r"\\brm\\s+-rf\\b", r":\\(\\)\\{:\\|:&\\};:", r"git\\s+push\\s+--force"]

<span class="p">$</span>echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | \\
  python3 ch02/quote-mcp/hooks/block_dangerous_bash.py
<span class="er">[BLOCKED exit=2] 위험한 셸 명령이 감지되어 실행을 차단했습니다.</span>
<span class="p">$</span>echo '{"tool_name":"Bash","tool_input":{"command":"pytest -q"}}' | \\
  python3 ch02/quote-mcp/hooks/block_dangerous_bash.py
<span class="ok">[ALLOW exit=0]</span></div>`;
      A(w1.el, 'up', 0.12, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 225, w: 840, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">플랫폼별 MCP·훅 브리지 + 제2장 오타 호환</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><code>mcp_config_claude.json</code> · <code>chatgpt</code> · <code>gemini</code><br>3대 플랫폼 전용 MCP/Tool 설정 파일을 분리 제공.</li>
        <li><code>hooks/platform_hook_bridge.py</code><br>플랫폼별 훅 페이로드를 표준 내부 포맷으로 정규화.</li>
        <li><code>audit_logger.py</code><br>PostToolUse 단계에서 도구 실행 감사 로그를 기록.</li>
        <li><code>ch04/quote-cli</code> → <code>ch02-mcp-and-hooks/quote-mcp</code><br>도서 제2장 오타 경로 호환용 심볼릭 링크를 유지.</li>
      </ul>`;
      A(c2, 'up', 0.22, { dur: 0.45 });
    },
  });

  // ch02 실습 + 모범 답안
  DECK.slide({
    id: 'ch02-lab',
    part: 'p1',
    chap: 'ch02 실습 & 답안',
    theme: 'paper',
    title: 'ch02 실습: MCP 도구 호출 & 위험 명령 차단 훅 테스트',
    notes: 'JSON-RPC MCP 서버 self-test와 PreToolUse 차단 시뮬레이션을 함께 실습합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch02',
        userPrompt: `[실습 결과 실행 프롬프트 — quote-mcp/ 폴더에서 AI CLI에 입력]
현재 quote-mcp 프로젝트 폴더에서 MCP 서버와 PreToolUse 가드레일 훅을 점검하고 실습 결과를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 main.py, hooks/block_dangerous_bash.py, .claude/settings.json을 먼저 구성)
   - python3 quote-mcp/main.py
   - echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 quote-mcp/hooks/block_dangerous_bash.py
   - python3 -m unittest discover -s quote-mcp/tests -p "test_*.py" -v

2. 출력 요구사항
   - MCP 서버 메타데이터(Tools/Resources/Prompts) JSON, 위험 명령 차단 JSON(exit 2 확인), 단위 테스트 통과 결과를 출력할 것.`,
        kicker: 'CH02 · HANDS-ON LAB (25분)',
        heading: '제2장 실습: <span class="hl">MCP 서버</span> &amp; <span class="hb">PreToolUse</span> 훅 검증',
        duration: '25분',
        missionTitle: 'quote-mcp/ 폴더에 MCP 서버·차단 훅 구성 후 AI CLI로 차단/통과 결과 출력',
        steps: [
          '<code>quote-mcp/main.py</code> · <code>.mcp.json</code><br>Tools·Resources·Prompts를 노출하는 MCP 서버와 설정을 작성.',
          '<code>hooks/block_dangerous_bash.py</code> · <code>.claude/settings.json</code><br>위험 Bash 명령을 exit code <code>2</code>로 차단하는 훅과 감사 로그를 연결.',
          '<code>quote-mcp/ 에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 MCP 메타데이터와 <code>rm -rf</code> 차단 JSON을 출력.',
        ],
        runCmd: 'python3 quote-mcp/main.py\npython3 -m unittest discover -s quote-mcp/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>quote-mcp/</code>에서 AI CLI가 MCP 메타데이터와 <code>PreToolUse</code> 위험 명령 차단(<code>exit 2</code>) 동작을 직접 검증해 출력합니다.',
        tree: `quote-mcp/
├── main.py                        # MCP 서버 (Tools/Resources/Prompts)
├── .mcp.json · mcp_config_*.json  # 3대 플랫폼 MCP 설정
├── .claude/settings.json          # PreToolUse / PostToolUse 훅 등록
└── hooks/
    ├── block_dangerous_bash.py    # exit 2 위험 명령 차단기
    ├── audit_logger.py            # 감사 로그 기록기
    └── platform_hook_bridge.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (MCP + PreToolUse 차단)',
        answerCode: `{"server": "quote-mcp", "transport": "stdio", "tools": ["add_quote", "get_random_quote"], "resources": ["quote://all"], "prompts": ["quote_post"]}

# 위험 명령 입력 시 block_dangerous_bash.py 응답 (exit code: 2):
{"decision": "block", "reason": "Dangerous command pattern detected: rm -rf"}`,
      });
    },
  });

  // ch03 이론
  DECK.slide({
    id: 'ch03-theory',
    part: 'p1',
    chap: 'ch03 3단계 Skills',
    theme: 'white',
    title: 'ch03: 상시 지침 vs 온디맨드 Skills (3단계 Progressive Disclosure)',
    notes: '스킬은 평소에는 YAML Frontmatter(이름+설명)만 컨텍스트에 올리고, 트리거될 때만 SKILL.md와 reference.md/scripts를 로드합니다.',
    build(el, A) {
      const T = title(el, 'CH03 · ON-DEMAND SKILLS', '컨텍스트를 아끼는 <span class="hl">3단계 확장형 Skills</span> 아키텍처', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const stages = [
        ['1단계 · Metadata (~100 tokens)', 'YAML Frontmatter (name, description)', '항상 컨텍스트에 상주하여 언제 이 스킬을 켤지 판단', '#D5F2E6', '#0B8A5F'],
        ['2단계 · Instructions (< 5KB)', 'SKILL.md 본문 절차 & 규칙', '트리거 조건이 맞을 때만 본문 지침을 온디맨드 로딩', '#DCE6FF', '#1E4FD0'],
        ['3단계 · Resources (필요 시)', 'reference.md · scripts/ · examples/', '긴 체크리스트·검증 스크립트는 실행 직전에만 참조', '#E6E0FF', '#4D2FD0'],
      ];
      stages.forEach(([st, file, desc, bg, fg], i) => {
        const c = card(el, { x: 100 + i * 585, y: 230, w: 550, h: 320, pad: 30 });
        c.innerHTML = `<span class="chip" style="background:${bg};color:${fg}">${st}</span>
          <div class="h4" style="margin-top:18px">${file}</div>
          <div class="b3" style="margin-top:14px">${desc}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });

      const c4 = card(el, { x: 100, y: 590, w: 1720, h: 375, pad: 32 });
      c4.innerHTML = `<div class="h4">5종 GitHub 워크플로 스킬 + 플랫폼 포팅 가이드(<code>skills_claude/chatgpt/gemini.md</code>)</div>
      <div class="row" style="gap:16px;flex-wrap:wrap;margin-top:20px">
        <span class="chip lg">1. git-commit</span>
        <span class="chip lg">2. gh-issue</span>
        <span class="chip lg">3. gh-pr</span>
        <span class="chip lg">4. gh-review</span>
        <span class="chip lg">5. gh-address-review</span>
      </div>
      <div class="b2" style="margin-top:24px">각 스킬 디렉터리의 <code>SKILL.md</code> · <code>reference.md</code> · <code>scripts/validate_*.py</code>를 공통 자산으로 유지하고 3대 플랫폼 가이드와 연동합니다.</div>`;
      A(c4, 'up', 0.34, { dur: 0.45 });
    },
  });

  // ch03 실습 + 모범 답안
  DECK.slide({
    id: 'ch03-lab',
    part: 'p1',
    chap: 'ch03 실습 & 답안',
    theme: 'paper',
    title: 'ch03 실습: Skills 5종 검증 스크립트 & 단위 테스트',
    notes: '5종 스킬의 validate_*.py 스크립트와 test_github_workflow_skills.py를 실행해 3단계 구조를 검증합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch03',
        userPrompt: `[실습 결과 실행 프롬프트 — github-workflow-skills/ 폴더에서 AI CLI에 입력]
현재 github-workflow-skills 폴더의 3단계 Progressive Disclosure 스킬을 적용해 검증하고 실습 결과를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 5종 스킬 SKILL.md, reference.md, scripts/validate_*.py를 먼저 구성)
   - git-commit/SKILL.md 규칙에 맞춰 Conventional Commit 메시지 1건 생성 후 validate_commit.py --text 로 검증
   - python3 -m unittest discover -s github-workflow-skills/tests -p "test_*.py" -v

2. 출력 요구사항
   - 생성된 커밋 메시지, [OK] valid Conventional Commit 검증 출력, 5종 스킬 단위 테스트 통과 결과를 출력할 것.`,
        kicker: 'CH03 · HANDS-ON LAB (30분)',
        heading: '제3장 실습: <span class="hl">5종 GitHub 스킬</span> 작성 &amp; 트리거 출력',
        duration: '30분',
        missionTitle: 'github-workflow-skills/ 폴더에 3단계 스킬 작성 후 AI CLI로 스킬 적용 결과 출력',
        steps: [
          '<code>SKILL.md</code> (YAML Frontmatter + 절차)<br>1단계 최소 메타데이터와 2단계 핵심 워크플로를 5종 스킬 폴더에 작성.',
          '<code>reference.md</code> · <code>examples/</code> · <code>scripts/validate_*.py</code><br>3단계 세부 기준과 결정론적 형식 검증 스크립트를 배치.',
          '<code>github-workflow-skills/ 에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 스킬 기반 산출물과 <code>validate_commit.py</code> 통과 결과를 출력.',
        ],
        runCmd: 'python3 github-workflow-skills/git-commit/scripts/validate_commit.py --text "feat: add workflow skill"\npython3 -m unittest discover -s github-workflow-skills/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + YAML',
        answerSummary: '<code>github-workflow-skills/</code>에서 AI CLI가 <code>SKILL.md</code>를 온디맨드로 로드해 규칙에 맞는 산출물을 만들고 검증 스크립트까지 통과시킵니다.',
        tree: `github-workflow-skills/
├── git-commit/ (SKILL.md, reference.md, examples/, scripts/validate_commit.py)
├── gh-issue/   (SKILL.md, reference.md, examples/, scripts/validate_issue.py)
├── gh-pr/      (SKILL.md, reference.md, examples/, scripts/validate_pr.py)
├── gh-review/  (SKILL.md, reference.md, examples/, scripts/validate_review.py)
├── gh-address-review/ (SKILL.md, reference.md, scripts/validate_address_review.py)
└── tests/test_github_workflow_skills.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (스킬 적용 + 검증)',
        answerCode: `---
name: git-commit
description: 변경 사항을 Conventional Commits 규칙으로 정리합니다.
---
[OK] valid Conventional Commit: feat: add workflow skill
[OK] 5/5 skills validated via test_github_workflow_skills.py`,
      });
    },
  });
})();
