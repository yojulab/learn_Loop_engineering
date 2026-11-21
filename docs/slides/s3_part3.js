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
        userPrompt: `[해당 단계 구성 전무(백지) 전제 — ch06 모범 답안 재현 프롬프트]
ch06 관련 파일이 전혀 없는 백지 상태에서 5종 서브에이전트와 동적 워크플로 모범 답안을 처음부터 작성해줘.
1. 생성할 파일 구조 및 심볼릭 링크:
   - ch06-subagents-workflow/.claude/agents/ (api-reviewer.md, code-quality.md, doc-writer.md, security-scanner.md, test-runner.md 5종 역할·허용 도구 정의)
   - ch06-subagents-workflow/agents_chatgpt.json , agents_gemini.json
   - ch06-subagents-workflow/dynamic_workflow.py
   - ch06-subagents-workflow/quote-cli/quote_cli.py (기존 명언 CLI에 --search <키워드> 본문·저자·태그 통합 검색 확장)
   - ch06-subagents-workflow/tests/test_dynamic_workflow.py
   - 심볼릭 링크: ch06/quote-cli -> ../ch06-subagents-workflow/quote-cli
2. 핵심 구현 규격:
   - dynamic_workflow.py: --task-type, --platform (claude|chatgpt|gemini), --json 옵션을 받아 platforms.get_adapter(platform) 기반으로 병렬·파이프라인 서브에이전트 워크플로를 실행하고 status: "completed" JSON 반환
   - quote_cli.py --search "harness" --json 실행 시 매칭되는 명언 배열(예: id=3 "Constraints are guardrails that keep autonomous loops safe.") 출력
3. 검증 명령:
   - python3 ch06-subagents-workflow/dynamic_workflow.py --platform gemini --json
   - python3 ch06/quote-cli/quote_cli.py --search "harness" --json`,
        kicker: 'CH06 · HANDS-ON LAB (20분)',
        heading: '제6장 실습: <span class="hl">서브에이전트</span> 위임 &amp; 멀티 플랫폼 실행',
        duration: '20분',
        missionTitle: '5종 에이전트 역할 정의 검증 및 동적 워크플로 오케스트레이션',
        steps: [
          '<code>ch06-subagents-workflow/dynamic_workflow.py --platform gemini --json</code><br>플랫폼 옵션을 <code>claude|chatgpt|gemini</code>로 바꿔 실행 로그를 비교.',
          '<code>ch06/quote-cli/quote_cli.py --search "harness" --json</code><br>검색 확장 옵션(<code>--search</code>, <code>--author</code>, <code>--tag</code>) 동작을 테스트.',
          '<code>ch06-subagents-workflow/tests/</code> · <code>quote-cli/tests/</code><br>두 테스트 스위트를 실행해 전 케이스 통과를 확인.',
        ],
        runCmd: 'python3 ch06-subagents-workflow/dynamic_workflow.py --platform gemini --json\npython3 ch06/quote-cli/quote_cli.py --search "harness" --json',
        answerLabel: 'ch06 모범 답안 열기 (Tree + 워크플로 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>dynamic_workflow.py</code>는 <code>platforms.get_adapter(platform)</code>을 호출해 어떤 플랫폼에서도 동일한 병렬 워크플로를 재현하며, <code>ch06/quote-cli/quote_cli.py</code>는 <code>--search</code> 검색을 지원합니다.',
        tree: `ch06-subagents-workflow/
├── .claude/agents/ (api-reviewer, code-quality, doc-writer, security-scanner, test-runner)
├── agents_chatgpt.json · agents_gemini.json
├── dynamic_workflow.py
├── quote-cli/quote_cli.py   (# ch06/quote-cli symlink)
└── tests/test_dynamic_workflow.py`,
        codeCaption: 'quote_cli.py --search & dynamic_workflow.py 결과 요약',
        answerCode: `[{"id": 3, "text": "Constraints are guardrails that keep autonomous loops safe.", "author": "Harness Principles"}]
# dynamic_workflow.py --platform gemini --json -> status: "completed"`,
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
        userPrompt: `[해당 단계 구성 전무(백지) 전제 — ch07 모범 답안 재현 프롬프트]
ch07 관련 파일이 전혀 없는 초기 상태에서 AST 아키텍처 린터와 가드레일 3종 세트 모범 답안을 처음부터 구현해줘.
1. 생성할 파일 구조 및 심볼릭 링크:
   - ch07-harness-engineering/harness-templates/AGENTS_TEMPLATE.md (100줄 이하 목차형 표준)
   - ch07-harness-engineering/harness-templates/CLAUDE_TEMPLATE.md , GEMINI_TEMPLATE.md , CHATGPT_TEMPLATE.md
   - ch07-harness-engineering/harness-templates/arch_linter.py
   - ch07-harness-engineering/harness-templates/guardrails.py
   - ch07-harness-engineering/harness-templates/doc_gardening.py
   - ch07-harness-engineering/harness-templates/samples/valid_app/ , samples/invalid_app/
   - ch07-harness-engineering/harness-templates/tests/test_harness_templates.py
   - 심볼릭 링크: ch07/harness-templates -> ../ch07-harness-engineering/harness-templates
2. 핵심 구현 규격:
   - arch_linter.py: ast.parse()로 import 구문을 분석해 FORBIDDEN_IMPORTS = {"domain": {"infra", "ui"}, "core": {"ui"}} 계층 역참조 위반 및 파일 줄 수 상한을 탐지 (--root, --json 지원, valid_app은 위반 0건 exit 0, invalid_app은 위반 탐지)
   - guardrails.py(시크릿·위험 패턴 탐지) 및 doc_gardening.py(문서 내 깨진 파일 참조 Drift 탐지) 구현
3. 검증 명령:
   - python3 ch07/harness-templates/arch_linter.py --root ch07/harness-templates/samples/valid_app --json
   - python3 -m unittest discover -s ch07-harness-engineering/harness-templates/tests -p "test_*.py" -v`,
        kicker: 'CH07 · HANDS-ON LAB (20분)',
        heading: '제7장 실습: <span class="hl">하네스 린터</span> &amp; 문서 정원가꾸기',
        duration: '20분',
        missionTitle: '100줄 AGENTS.md 검증과 아키텍처·보안·문서 3종 하네스 실행',
        steps: [
          '<code>ch07/harness-templates/arch_linter.py --root ch07/harness-templates/samples/valid_app --json</code><br>정상 샘플과 <code>invalid_app</code>을 대상으로 계층 의존성 위반 탐지를 점검.',
          '<code>guardrails.py</code> · <code>doc_gardening.py</code><br>시크릿 노출 패턴과 깨진 문서 링크를 검사.',
          '<code>harness-templates/tests/</code><br>의도적 위반 탐지(Negative Test) 통과 여부를 확인.',
        ],
        runCmd: 'python3 ch07/harness-templates/arch_linter.py --root ch07/harness-templates/samples/valid_app --json\npython3 -m unittest discover -s ch07-harness-engineering/harness-templates/tests -p "test_*.py" -v',
        answerLabel: 'ch07 모범 답안 열기 (Tree + 린터 규칙)',
        answerType: 'Tree + AST',
        answerSummary: '<code>arch_linter.py</code>는 Python <code>ast.parse</code>로 import 그래프를 분석하므로 정규식보다 정확하게 계층 위반을 잡아냅니다.',
        tree: `ch07-harness-engineering/harness-templates/  (# ch07/harness-templates)
├── AGENTS_TEMPLATE.md         # <= 100줄 목차형 표준
├── CLAUDE_TEMPLATE.md / GEMINI_TEMPLATE.md / CHATGPT_TEMPLATE.md
├── arch_linter.py             # AST 레이어 의존성 검증
├── guardrails.py              # 시크릿·위험패턴 차단
├── doc_gardening.py           # 문서-코드 드리프트 탐지
└── tests/test_harness_templates.py`,
        codeCaption: 'arch_linter.py 핵심 AST 검증 패턴',
        answerCode: `# domain 레이어에서 infra 레이어를 직접 import 하면 위반!
FORBIDDEN_IMPORTS = {"domain": {"infra", "ui"}, "core": {"ui"}}
tree = ast.parse(path.read_text(encoding="utf-8"))
# 결과: [OK] 0 architecture violations / AGENTS.md lines=74 <= 100`,
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
        userPrompt: `[해당 단계 구성 전무(백지) 전제 — ch08 모범 답안 재현 프롬프트]
ch08 관련 디렉터리가 전혀 없는 백지 상태에서 SQLite FTS5 RSS Wiki와 Ralph Loop (/goal 평가기) 모범 답안을 처음부터 작성해줘.
1. 생성할 파일 구조 및 심볼릭 링크:
   - ch08-inner-ralph-loop/rss-wiki/db.py
   - ch08-inner-ralph-loop/rss-wiki/collector.py
   - ch08-inner-ralph-loop/rss-wiki/app.py
   - ch08-inner-ralph-loop/rss-wiki/goal_evaluator.py
   - ch08-inner-ralph-loop/rss-wiki/ralph_loop.sh
   - ch08-inner-ralph-loop/rss-wiki/worker_claude.sh , worker_chatgpt.sh , worker_gemini.sh
   - ch08-inner-ralph-loop/rss-wiki/tests/test_rss_wiki.py
   - 심볼릭 링크: ch08/rss-wiki -> ../ch08-inner-ralph-loop/rss-wiki
2. 핵심 구현 규격:
   - db.py: CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(title, summary, url UNINDEXED, tokenize='unicode61'); 기반 전문 검색 인덱싱 및 질의
   - collector.py: 로컬 샘플 RSS 피드 파싱 및 중복 제거 적재 / app.py: 내장 http.server 검색 API
   - goal_evaluator.py: 기사 수·FTS5 인덱스·테스트 통과 여부를 수치로 검증해 GOAL_MET 상태 출력
   - ralph_loop.sh: 반복마다 컨텍스트를 초기화하고 MAX_ITERS 및 연속 에러 서킷 브레이커로 무한 루프 차단
3. 검증 명령:
   - python3 ch08/rss-wiki/goal_evaluator.py
   - python3 -m unittest discover -s ch08-inner-ralph-loop/rss-wiki/tests -p "test_*.py" -v`,
        kicker: 'CH08 · HANDS-ON LAB (25분)',
        heading: '제8장 실습: <span class="hb">FTS5 Wiki</span> &amp; <span class="hl">Ralph Loop /goal</span> 평가',
        duration: '25분',
        missionTitle: 'SQLite FTS5 전문 검색과 Ralph Loop 목표 달성 판정기 검증',
        steps: [
          '<code>ch08/rss-wiki/db.py</code>, <code>collector.py</code><br>초기화 테스트를 실행해 FTS5 전문 검색 동작을 검증.',
          '<code>ch08/rss-wiki/goal_evaluator.py</code><br>실행 후 목표 달성(<code>GOAL_MET</code>) vs 미달 판정 출력을 확인.',
          '<code>worker_claude.sh</code> · <code>worker_chatgpt.sh</code> · <code>worker_gemini.sh</code><br>3대 플랫폼 워커 스크립트의 비대화형 CLI 플래그 차이를 비교.',
        ],
        runCmd: 'python3 ch08/rss-wiki/goal_evaluator.py\npython3 -m unittest discover -s ch08-inner-ralph-loop/rss-wiki/tests -p "test_*.py" -v',
        answerLabel: 'ch08 모범 답안 열기 (Tree + FTS5/Goal)',
        answerType: 'Tree + SQL/CLI',
        answerSummary: '<code>goal_evaluator.py</code>는 테스트 통과율과 에러 건수를 수치로 검증한 뒤 완료 시그널을 출력해 Ralph Loop를 안전하게 종료시킵니다.',
        tree: `ch08-inner-ralph-loop/rss-wiki/  (# ch08/rss-wiki)
├── db.py (SQLite FTS5) · collector.py · app.py
├── goal_evaluator.py · ralph_loop.sh
├── worker_claude.sh · worker_chatgpt.sh · worker_gemini.sh
└── tests/test_rss_wiki.py`,
        codeCaption: 'FTS5 가상 테이블 & Goal 판정 흐름',
        answerCode: `CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts
USING fts5(title, summary, url UNINDEXED, tokenize='unicode61');

# python3 ch08/rss-wiki/goal_evaluator.py -> goal 달성 여부 JSON/상태 출력`,
      });
    },
  });
})();
