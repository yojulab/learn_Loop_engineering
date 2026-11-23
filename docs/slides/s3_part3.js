(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 3 Divider
  DECK.slide({
    id: 'p3-div',
    part: 'p3',
    chap: 'Part 3 시작',
    theme: 'green',
    title: 'Part 3 · 위임과 품질 (ch06 ~ ch08, 65분)',
    notes: 'Part 3은 서브에이전트와 워크플로(ch06), 하네스 엔지니어링(ch07), 이너 루프 & Ralph Loop /goal(ch08)을 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 3 · 65분', { bg: 'rgba(15,27,61,.18)', fg: '#0F1B3D' });
      h('div', 'h1', box, '역할 위임, 가드레일,<br>그리고 자율 이너 루프').style.cssText = 'margin-top:24px;color:#fff';
      h('div', 'b1', box, 'ch06 서브에이전트 · ch07 하네스 린터 · ch08 FTS5 + Ralph Loop').style.cssText = 'margin-top:28px;color:#E2FAF0';
      A(box, 'up', 0, { dur: 0.5 });
    },
  });

  // ch06 이론
  DECK.slide({
    id: 'ch06-theory',
    part: 'p3',
    chap: 'ch06 서브에이전트',
    theme: 'paper',
    title: 'ch06: 전문 서브에이전트 위임 & 동적 워크플로',
    notes: '하나의 에이전트에게 모든 일을 몰아주면 컨텍스트가 오염됩니다. 역할·도구·모델을 분리한 5종 서브에이전트와 Python 워크플로 오케스트레이션을 봅니다.',
    build(el, A) {
      const T = title(el, 'CH06 · SUBAGENTS & WORKFLOW', '컨텍스트 격리 기반 <span class="hl">서브에이전트</span> &amp; 동적 파이프라인', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 840, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">5종 전문 서브에이전트 (<code>.claude/agents/</code>)</div>
      <ul class="lab-steps" style="margin-top:16px">
        <li><code>api-reviewer.md</code> · <code>code-quality.md</code><br>API 계약·품질 기준을 읽기 전용으로 감사.</li>
        <li><code>security-scanner.md</code> · <code>test-runner.md</code><br>보안 취약점 스캔 및 테스트 스위트 검증 수행.</li>
        <li><code>doc-writer.md</code><br>변경된 코드와 README·API 문서를 동기화.</li>
      </ul>
      <div class="answer-hint" style="margin-top:20px">멀티 플랫폼 포팅: <code>agents_chatgpt.json</code> &amp; <code>agents_gemini.json</code> 동시 제공</div>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const w2 = win(el, { x: 980, y: 230, w: 840, h: 720, dark: true, title: 'ch06-subagents-workflow/dynamic_workflow.py' });
      w2.body.innerHTML = `<pre class="code-block" style="background:transparent;border:0;padding:0;font-size:21px"><code># --platform claude | chatgpt | gemini 지원
python3 ch06-subagents-workflow/dynamic_workflow.py \
  --task-type release_check \
  --platform gemini --json

# 검색 확장 Quote CLI:
python3 ch06/quote-cli/quote_cli.py --search "harness" --json</code></pre>`;
      A(w2.el, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch06 실습 + 모범 답안
  DECK.slide({
    id: 'ch06-lab',
    part: 'p3',
    chap: 'ch06 실습 & 답안',
    theme: 'white',
    title: 'ch06 실습: 플랫폼별 서브에이전트 동적 워크플로 실행',
    notes: 'quote_agent.py와 dynamic_workflow.py를 claude/chatgpt/gemini 모드로 각각 실행해 봅니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch06',
        userPrompt: `[실습 결과 실행 프롬프트 — quote-cli/ 서브에이전트 프로젝트 폴더에서 AI CLI에 입력]
현재 폴더의 5종 커스텀 서브에이전트와 동적 워크플로로 확장된 quote_cli.py 검색 기능을 교차 검증하고 결과를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 .claude/agents/*.md 5종, dynamic_workflow.py, quote-cli/quote_cli.py를 먼저 구성)
   - python3 dynamic_workflow.py --platform gemini --json
   - python3 quote-cli/quote_cli.py --search "harness" --json
   - python3 -m unittest discover -s tests -p "test_*.py" -v

2. 출력 요구사항
   - 동적 선택·병렬 실행된 서브에이전트 요약, --search "harness" JSON 결과, 테스트 통과 여부를 출력할 것.`,
        kicker: 'CH06 · HANDS-ON LAB (20분)',
        heading: '제6장 실습: <span class="hl">서브에이전트</span> 병렬 위임 &amp; 교차 검증',
        duration: '20분',
        missionTitle: '.claude/agents/ 5종 정의·워크플로 작성 후 AI CLI로 병렬 위임 결과 출력',
        steps: [
          '<code>.claude/agents/*.md</code> · <code>agents_*.json</code><br>읽기 전용 리뷰어와 실행형 테스터 등 5종 서브에이전트 역할을 정의.',
          '<code>dynamic_workflow.py</code> · <code>quote-cli/quote_cli.py</code><br><code>ThreadPoolExecutor</code> 병렬 위임기와 <code>--search</code>·<code>--author</code> 확장을 구현.',
          '<code>프로젝트 폴더에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 서브에이전트 병렬 실행 결과와 검색 JSON을 출력.',
        ],
        runCmd: 'python3 dynamic_workflow.py --platform gemini --json\npython3 quote-cli/quote_cli.py --search "harness" --json',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: 'AI CLI가 <code>.claude/agents/</code>에 정의된 서브에이전트를 활용해 격리된 병렬 리뷰·검색 테스트 결과를 하나로 병합 출력합니다.',
        tree: `project/
├── .claude/agents/ (api-reviewer, code-quality, doc-writer, security-scanner, test-runner)
├── agents_chatgpt.json · agents_gemini.json
├── dynamic_workflow.py       # 동적 선택 + ThreadPoolExecutor 병렬 실행
├── quote-cli/quote_cli.py    # --search, --author, --tag 확장
└── tests/test_dynamic_workflow.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (dynamic_workflow.py --json)',
        answerCode: `{
  "platform": "gemini",
  "selected_agents": ["api-reviewer", "security-scanner", "test-runner"],
  "parallel_status": "ALL_PASSED",
  "search_hits": [{"id": 3, "tags": ["harness", "engineering"]}]
}`,
      });
    },
  });

  // ch07 이론
  DECK.slide({
    id: 'ch07-theory',
    part: 'p3',
    chap: 'ch07 하네스 엔지니어링',
    theme: 'ink',
    dots: true,
    title: 'ch07: 하네스 엔지니어링 — 목차형 100줄 AGENTS.md & 결정론적 린터',
    notes: '말로 주의를 주는 대신(비결정적), 코드와 린터로 규칙을 강제(결정적)하는 것이 하네스 엔지니어링의 핵심입니다.',
    build(el, A) {
      const T = title(el, 'CH07 · HARNESS ENGINEERING', '말이 아닌 <span class="hl">코드와 구조</span>로 강제하는 하네스 3종 세트', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const items = [
        ['1. 목차형 100줄 AGENTS.md', '거대한 매뉴얼 대신 핵심 규칙과 상세 문서 포인터만 100줄 이내로 유지해 컨텍스트 점유 최소화'],
        ['2. arch_linter.py (아키텍처 린터)', '도메인 계층 간 금지된 역참조 import나 크기 상한 위반을 AST 기반으로 즉시 탐지 (exit=1)'],
        ['3. guardrails.py & doc_gardening.py', '시크릿/금지 패턴 스캔 및 코드와 문서 링크 간 불일치(Doc Drift)를 주기적으로 자동 정리'],
      ];
      items.forEach(([hd, bd], i) => {
        const c = card(el, { x: 100, y: 230 + i * 240, w: 1720, h: 210, pad: 30 });
        c.innerHTML = `<div class="h3">${hd}</div><div class="b2" style="margin-top:14px">${bd}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });
    },
  });

  // ch07 실습 + 모범 답안
  DECK.slide({
    id: 'ch07-lab',
    part: 'p3',
    chap: 'ch07 실습 & 답안',
    theme: 'paper',
    title: 'ch07 실습: 아키텍처 린터·가드레일·문서 정원가꾸기 실행',
    notes: 'arch_linter.py, guardrails.py, doc_gardening.py를 실행하고 AGENTS.md 100줄 규정을 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch07',
        userPrompt: `[실습 결과 실행 프롬프트 — harness-templates/ 폴더에서 AI CLI에 입력]
현재 harness-templates 폴더의 아키텍처 린터와 가드레일·문서 감사 도구를 실행해 검증 리포트를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 AGENTS.md, arch_linter.py, guardrails.py, doc_gardening.py를 먼저 구성)
   - python3 harness-templates/arch_linter.py --root harness-templates/samples/valid_app --json
   - python3 harness-templates/arch_linter.py --root harness-templates/samples/invalid_app --json (위반 탐지 확인)
   - python3 harness-templates/guardrails.py --cmd "ls -la" --json
   - python3 -m unittest discover -s harness-templates/tests -p "test_*.py" -v

2. 출력 요구사항
   - valid_app(passed: true) vs invalid_app(UI -> Repo 위반 탐지) 비교와 가드레일/테스트 통과 결과를 출력할 것.`,
        kicker: 'CH07 · HANDS-ON LAB (20분)',
        heading: '제7장 실습: <span class="hl">AST 린터</span> &amp; 하네스 가드레일 검증',
        duration: '20분',
        missionTitle: 'harness-templates/ 폴더에 린터·가드레일 작성 후 AI CLI로 위반 탐지 결과 출력',
        steps: [
          '<code>AGENTS.md</code> (100줄 이하 목차형)<br>상시 로딩 가능한 계층 의존성 규칙과 금지 패턴 지침을 작성.',
          '<code>arch_linter.py</code> · <code>guardrails.py</code> · <code>doc_gardening.py</code><br>AST 레이어 검사기, 파괴 명령 차단기(<code>--json</code>), 문서 드리프트 탐지기를 구현.',
          '<code>harness-templates/ 에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 정상 vs 위반 샘플 진단 JSON을 출력.',
        ],
        runCmd: 'python3 harness-templates/arch_linter.py --root harness-templates/samples/valid_app --json\npython3 harness-templates/guardrails.py --cmd "ls -la" --json\npython3 -m unittest discover -s harness-templates/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>harness-templates/</code>에서 AI CLI가 AST 린터와 가드레일을 실행해 <code>valid_app</code> 통과 및 <code>invalid_app</code> 계층 위반을 즉시 출력합니다.',
        tree: `harness-templates/
├── AGENTS.md                  # <= 100줄 목차형 표준
├── arch_linter.py             # AST 레이어 의존성 검증
├── guardrails.py              # 파괴 명령/시크릿 차단 (--json)
├── doc_gardening.py           # 문서-코드 드리프트 탐지
├── samples/ (valid_app, invalid_app)
└── tests/test_harness_templates.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (valid vs invalid 진단)',
        answerCode: `// valid_app:
{"passed": true, "violations": []}
// invalid_app:
{"passed": false, "violations": ["ui/screen.py -> repo.user_repo (UI cannot import Repo directly)"]}
// guardrails.py --cmd "ls -la" --json:
{"safe": true, "violations": []}`,
      });
    },
  });

  // ch08 이론
  DECK.slide({
    id: 'ch08-theory',
    part: 'p3',
    chap: 'ch08 이너 & Ralph 루프',
    theme: 'white',
    title: 'ch08: 이너 루프, Ralph Loop(컨텍스트 초기화) & /goal 평가자',
    notes: '컨텍스트가 무거워져 모델이 같은 실수를 반복하면, 파일(TASKS/PROGRESS)만 남기고 세션을 새로 시작하는 Ralph Loop가 효과적입니다.',
    build(el, A) {
      const T = title(el, 'CH08 · INNER & RALPH LOOP', 'SQLite <span class="hb">FTS5 RSS Wiki</span>와 <span class="hl">Ralph Loop</span> 장시간 자율 실행', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 840, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">RSS Wiki 앱 (<code>ch08/rss-wiki/</code>)</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><code>db.py</code><br>SQLite <code>FTS5</code> 가상 테이블 기반 전문 검색 인덱스를 구축.</li>
        <li><code>collector.py</code><br>로컬 샘플 피드를 파싱하고 중복을 제거해 저장.</li>
        <li><code>app.py</code><br>Python 내장 <code>http.server</code> 웹 UI와 JSON 검색 API를 제공.</li>
      </ul>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 230, w: 840, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">Ralph Loop &amp; <code>/goal</code> 3종 셸 스크립트</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><b>컨텍스트 초기화 원칙</b><br>반복마다 세션을 비우고 파일 상태만 다시 읽어 컨텍스트 부패를 차단.</li>
        <li><b>무한 루프 가드</b><br><code>MAX_ITERS</code> 상한, 종료 코드 확인, 연속 동일 에러 시 즉시 중단.</li>
        <li><code>ralph_loop.sh</code> · <code>worker_claude/chatgpt/gemini.sh</code><br>3대 플랫폼용 워커 셸 스크립트와 <code>goal_evaluator.py</code>를 함께 제공.</li>
      </ul>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch08 실습 + 모범 답안
  DECK.slide({
    id: 'ch08-lab',
    part: 'p3',
    chap: 'ch08 실습 & 답안',
    theme: 'paper',
    title: 'ch08 실습: FTS5 검색 DB & goal_evaluator 성공 판정',
    notes: 'RSS Wiki의 FTS5 검색과 /goal 평가기의 종료 조건 판정을 실습합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch08',
        userPrompt: `[실습 결과 실행 프롬프트 — rss-wiki/ 폴더에서 AI CLI에 입력]
현재 rss-wiki 프로젝트 폴더에서 PROMPT.md 목표 기준에 따라 수집·FTS5 색인·목표 달성 판정 결과를 출력해줘.

1. 실행 및 검증할 항목 (미작성 시 db.py, collector.py, app.py, goal_evaluator.py, ralph_loop.sh를 먼저 구성)
   - python3 rss-wiki/goal_evaluator.py
   - python3 -m unittest discover -s rss-wiki/tests -p "test_*.py" -v

2. 출력 요구사항
   - goal_evaluator.py의 5대 조건 점검 JSON(status: "MET", passed_count: 5/5)과 FTS5 테스트 통과 결과를 출력할 것.`,
        kicker: 'CH08 · HANDS-ON LAB (25분)',
        heading: '제8장 실습: <span class="hl">FTS5 RSS Wiki</span> &amp; /goal 판정 출력',
        duration: '25분',
        missionTitle: 'rss-wiki/ 폴더에 SQLite FTS5·목표 판정기 작성 후 AI CLI로 MET 결과 출력',
        steps: [
          '<code>rss-wiki/db.py</code> · <code>collector.py</code> · <code>app.py</code><br>SQLite FTS5 전문 검색 DB, XML 수집기, 웹 뷰를 작성.',
          '<code>PROMPT.md</code> · <code>goal_evaluator.py</code> · <code>ralph_loop.sh</code><br>종료 조건 검증기(5대 체크리스트)와 3대 플랫폼 워커 루프를 구성.',
          '<code>rss-wiki/ 에서 AI CLI 실행</code><br>단축키 A 프롬프트를 입력해 <code>status: "MET"</code> (5/5) 판정 JSON을 출력.',
        ],
        runCmd: 'python3 rss-wiki/goal_evaluator.py\npython3 -m unittest discover -s rss-wiki/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>rss-wiki/</code>에서 AI CLI가 <code>goal_evaluator.py</code>와 FTS5 테스트를 실행해 <code>status: "MET"</code> 객관적 달성 판정을 출력합니다.',
        tree: `rss-wiki/
├── PROMPT.md                 # 이너 루프 목표 명세
├── db.py (FTS5) · collector.py · app.py
├── goal_evaluator.py         # 5대 조건 독립 판정기 (JSON)
├── ralph_loop.sh · worker_*.sh
└── tests/test_rss_wiki.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (goal_evaluator.py)',
        answerCode: `{
  "status": "MET",
  "passed_count": 5,
  "total_count": 5,
  "checks": [
    {"name": "db_module", "passed": true},
    {"name": "tests_present", "passed": true}
  ]
}`,
      });
    },
  });
})();
