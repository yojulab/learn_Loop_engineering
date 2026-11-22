(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 1 Divider
  DECK.slide({
    id: 'p1-div',
    part: 'p1',
    chap: 'Part 1 시작',
    theme: 'blue',
    title: 'Part 1 · 행동과 확장 (ch01 ~ ch03)',
    notes: 'Part 1은 에이전트 루프(ch01), MCP와 Hooks 가드레일(ch02), 온디맨드 3단계 Skills(ch03)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:100px;top:270px;width:1040px';
      chip(box, 'PART 1', { bg: 'rgba(255,255,255,.2)', fg: '#fff' });
      h('div', 'h1', box, '행동, 도구 연결, 그리고<br>팀 워크플로의 표준화').style.cssText = 'margin-top:24px;color:#fff';
      h('div', 'b1', box, 'ch01 에이전트 루프 · ch02 MCP &amp; Hooks · ch03 3단계 Skills').style.cssText = 'margin-top:28px;color:#DCE6FF';
      A(box, 'up', 0, { dur: 0.5 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_01_in.jpg" alt="Part 1 도입 카툰: 바이브 코딩 1~3세대 & 목표-도구-확인 루프" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
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
        userPrompt: `[에이전트 코딩 루프 & Quote CLI 모범 답안 재현 프롬프트]
명언 데이터와 태그 필터링, 결정론적 시드 기반 랜덤 추출을 지원하는 Quote CLI 및 단위 테스트를 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - README.md
   - quote-cli/quotes.json (id, text, author, tags 배열을 포함한 최소 5건 이상의 엔지니어링 명언 데이터, engineering 태그 포함)
   - quote-cli/quote_cli.py
   - quote-cli/interactive_demo.py (REPL 대화형 루프 데모)
   - quote-cli/tests/test_quote_cli.py

2. 핵심 구현 명세 (표준 라이브러리 argparse, json, random, pathlib만 사용)
   - load_quotes(path): quotes.json을 파싱하며 list가 아니면 ValueError 발생
   - filter_by_tag(quotes, tag): 대소문자 무시 정확 일치(t.lower() == tag.strip().lower()) 필터링
   - get_random_quote(quotes, rng=None): 빈 목록이면 ValueError, rng(random.Random(seed)) 전달 시 결정론적 1건 선택
   - format_quotes(quotes, as_json=False): JSON 문자열 또는 '[id] "text" — author (tags: ...)' 텍스트 반환
   - CLI 옵션: --all, --tag, --json, --seed, --data

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 quote-cli/quote_cli.py --tag engineering --json
   - python3 quote-cli/quote_cli.py --seed 42 --json
   - python3 -m unittest discover -s quote-cli/tests -p "test_*.py" -v`,
        kicker: 'CH01 · HANDS-ON LAB',
        heading: '제1장 실습: <span class="hb">Quote CLI</span> 필터 &amp; 단위 테스트',
        duration: '',
        missionTitle: '태그·저자 검색 및 JSON 출력을 지원하는 Quote CLI 검증',
        steps: [
          '<code>quote-cli/quote_cli.py --tag engineering --json</code><br>태그 필터링과 JSON 구조화 출력 결과를 확인.',
          '<code>--author "Loop Handbook"</code> / <code>--seed 42</code><br>저자 검색과 결정론적 랜덤 추출 동작을 검증.',
          '<code>test_quote_cli.py</code><br>단위 테스트 스위트를 실행해 전 케이스 통과를 확인.',
        ],
        runCmd: 'python3 quote-cli/quote_cli.py --tag engineering --json\npython3 -m unittest discover -s quote-cli/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + 구현 코드)',
        answerType: 'Tree + Python',
        answerSummary: '<code>quote_cli.py</code>는 표준 라이브러리(<code>argparse</code>, <code>json</code>, <code>random</code>)만으로 CLI·JSON·시드 랜덤을 지원합니다.',
        tree: `project/
├── README.md
└── quote-cli/
    ├── quotes.json
    ├── quote_cli.py
    ├── interactive_demo.py
    └── tests/test_quote_cli.py`,
        codeCaption: 'quote_cli.py 핵심 필터 & 시드 랜덤 로직',
        answerCode: `def filter_quotes(quotes, tag=None, author=None):
    items = quotes
    if tag:
        items = [q for q in items if tag.lower() in [t.lower() for t in q.get("tags", [])]]
    if author:
        items = [q for q in items if author.lower() in q.get("author", "").lower()]
    return items

# 실행 예: python3 quote-cli/quote_cli.py --all --json`,
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
        userPrompt: `[MCP & PreToolUse 훅 가드레일 모범 답안 재현 프롬프트]
FastMCP 표준 프로토콜 기반 Quote MCP 서버와 위험 Bash 명령 차단 훅, 멀티 플랫폼 설정 및 단위 테스트를 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - quote-mcp/main.py
   - quote-mcp/mcp_config_claude.json , mcp_config_chatgpt.json , mcp_config_gemini.json
   - quote-mcp/hooks/block_dangerous_bash.py
   - quote-mcp/hooks/audit_logger.py
   - quote-mcp/hooks/platform_hook_bridge.py
   - quote-mcp/tests/test_quote_mcp_and_hooks.py

2. 핵심 구현 명세
   - main.py: 외부 mcp.server.fastmcp 미설치 시 동일 데코레이터 계약을 제공하는 LocalFastMCP 폴백 클래스 포함. @mcp.tool() get_random_quote / add_quote, @mcp.resource("quote://all"), @mcp.prompt() quote_post 등록. run("stdio") 실행 시 {"server": "quote-mcp", "transport": "stdio", "tools": [...], "resources": ["quote://all"], "prompts": ["quote_post"]} 메타데이터 출력.
   - hooks/block_dangerous_bash.py: evaluate_command(command)로 rm -rf, git push --force/-f, git reset --hard, DROP TABLE, find ... -delete, mkfs 정규식 탐지. --command 인자 또는 stdin JSON(platform_hook_bridge.normalize_hook_event() 호환)을 받아 차단 시 {"decision": "block", "reason": ...} 출력 후 sys.exit(2), 안전 명령은 exit 0.
   - hooks/audit_logger.py: 도구 실행 이벤트를 JSONL 감사 로그로 기록.

3. 검증 명령 (전부 통과 필수)
   - python3 quote-mcp/main.py
   - echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 quote-mcp/hooks/block_dangerous_bash.py  # exit=2 확인
   - python3 -m unittest discover -s quote-mcp/tests -p "test_*.py" -v`,
        kicker: 'CH02 · HANDS-ON LAB',
        heading: '제2장 실습: <span class="hl">MCP 서버</span> &amp; <span class="hb">PreToolUse</span> 차단 검증',
        duration: '',
        missionTitle: 'Quote MCP 도구 실행과 위험 Bash 차단 훅 동작 검증',
        steps: [
          '<code>quote-mcp/main.py</code><br>실행 후 MCP 서버 메타데이터와 도구·리소스 목록을 확인.',
          '<code>block_dangerous_bash.py</code><br><code>rm -rf</code>와 안전 명령을 전달해 exit code <code>2</code> vs <code>0</code>을 검증.',
          '<code>mcp_config_claude.json</code> · <code>chatgpt</code> · <code>gemini</code><br>3대 플랫폼 설정 스키마 차이를 비교.',
        ],
        runCmd: 'python3 quote-mcp/main.py\npython3 -m unittest discover -s quote-mcp/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + 훅·MCP 코드)',
        answerType: 'Tree + Config',
        answerSummary: '<code>block_dangerous_bash.py</code>는 exit code <code>2</code>를 반환해 Claude Code / 범용 브리지에서 도구 실행 자체를 사전 차단하며, <code>audit_logger.py</code>가 실행 이력을 남깁니다.',
        tree: `quote-mcp/
├── main.py                    # MCP JSON-RPC / self-test
├── mcp_config_claude.json     # Claude MCP 스키마
├── mcp_config_chatgpt.json    # ChatGPT MCP/Tool 스키마
├── mcp_config_gemini.json     # Gemini MCP 스키마
└── hooks/
    ├── block_dangerous_bash.py
    ├── audit_logger.py
    └── platform_hook_bridge.py`,
        codeCaption: '위험 명령 훅 검사 & MCP 메타데이터 결과',
        answerCode: `{"server": "quote-mcp", "transport": "stdio", "tools": ["add_quote", "get_random_quote"], "resources": ["quote://all"], "prompts": ["quote_post"]}

# PreToolUse 검사 흐름:
# stdin JSON -> platform_hook_bridge.normalize_hook_event()
# -> regex match(rm -rf / mkfs / force push) -> sys.exit(2) 차단`,
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
        userPrompt: `[3단계 Skills & GitHub 워크플로 모범 답안 재현 프롬프트]
3단계 Progressive Disclosure(1단계 Metadata -> 2단계 Instructions -> 3단계 Resources) 구조의 5종 GitHub 스킬 및 검증 테스트를 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - github-workflow-skills/ 하위에 5종 스킬 디렉터리 각각 구성:
     * git-commit/ : SKILL.md, reference.md, examples/, scripts/validate_commit.py
     * gh-issue/   : SKILL.md, reference.md, examples/, scripts/validate_issue.py
     * gh-pr/      : SKILL.md, reference.md, examples/, scripts/validate_pr.py
     * gh-review/  : SKILL.md, reference.md, examples/, scripts/validate_review.py
     * gh-address-review/ : SKILL.md, reference.md, examples/, scripts/validate_address_review.py
   - 3대 플랫폼 가이드: skills_claude.md , skills_chatgpt.md , skills_gemini.md
   - 단위 테스트: github-workflow-skills/tests/test_github_workflow_skills.py

2. 핵심 구현 명세
   - 각 SKILL.md 상단에 '---\\nname: <스킬명>\\ndescription: <활성화 조건 설명>\\n---' YAML Frontmatter를 반드시 배치(1단계 로딩 최소화).
   - 본문(2단계)에는 절차와 규칙을 간결하게(<5KB) 적고, 상세 체크리스트는 reference.md(3단계)로 분리.
   - validate_commit.py: --text 인자를 받아 Conventional Commits 패턴(^(feat|fix|docs|style|refactor|test|chore)(\\(.+\\))?: .+)을 검증해 유효 시 exit 0("[OK] valid Conventional Commit"), 위반 시 exit 1 반환. 나머지 4개 validate_*.py도 동일 패턴으로 구현.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 github-workflow-skills/git-commit/scripts/validate_commit.py --text "feat: add workflow skill"
   - python3 -m unittest discover -s github-workflow-skills/tests -p "test_*.py" -v`,
        kicker: 'CH03 · HANDS-ON LAB',
        heading: '제3장 실습: <span class="hl">5종 GitHub 스킬</span> 검증 스크립트 &amp; 테스트',
        duration: '',
        missionTitle: '3단계 Progressive Disclosure 스킬 구조 및 커밋/PR 검증 스크립트 실행',
        steps: [
          '<code>github-workflow-skills/git-commit/scripts/validate_commit.py --text "feat: add workflow skill"</code><br>Conventional Commits 메시지 검증 스크립트 동작을 확인.',
          '<code>skills_claude.md</code> · <code>skills_chatgpt.md</code> · <code>skills_gemini.md</code><br>3대 플랫폼용 스킬 적용 가이드를 비교.',
          '<code>tests/test_github_workflow_skills.py</code><br>5종 스킬 Frontmatter·스크립트 단위 테스트를 실행.',
        ],
        runCmd: 'python3 github-workflow-skills/git-commit/scripts/validate_commit.py --text "feat: add workflow skill"\npython3 -m unittest discover -s github-workflow-skills/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + SKILL.md 구조)',
        answerType: 'Tree + YAML',
        answerSummary: '모든 스킬은 <code>SKILL.md</code> 상단에 <code>name</code>과 <code>description</code>이 있는 YAML Frontmatter를 가지며, 각 하위 <code>scripts/validate_*.py</code>로 형식을 자동 검증합니다.',
        tree: `github-workflow-skills/
├── git-commit/ (SKILL.md, reference.md, examples/, scripts/validate_commit.py)
├── gh-issue/   (SKILL.md, reference.md, examples/, scripts/validate_issue.py)
├── gh-pr/      (SKILL.md, reference.md, examples/, scripts/validate_pr.py)
├── gh-review/  (SKILL.md, reference.md, examples/, scripts/validate_review.py)
├── gh-address-review/ (SKILL.md, reference.md, scripts/validate_address_review.py)
├── skills_claude.md · skills_chatgpt.md · skills_gemini.md
└── tests/test_github_workflow_skills.py`,
        codeCaption: 'validate_commit.py & 스킬 테스트 기대 결과',
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
