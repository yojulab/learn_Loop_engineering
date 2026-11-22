(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 4B Divider
  DECK.slide({
    id: 'p4b-div',
    part: 'p4b',
    chap: 'Part 4B 시작',
    theme: 'paper',
    title: 'Part 4B · Eval, LLMOps & 실전 로드맵 (ch11 ~ ch12, 40분)',
    notes: '마지막 블록은 LiteLLM 프록시 + Langfuse Save as Prompt + 3종 Eval(ch11)과 Stage 1~4 도입 전략(ch12)으로 마무리합니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 4B · 40분', { bg: 'var(--red-l)', fg: 'var(--red)' });
      h('div', 'h1', box, '관측과 평가(<span class="hr">Eval/LLMOps</span>),<br>그리고 팀 도입 4단계').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch11 LiteLLM 무코드 프록시 &amp; Langfuse 프롬프트 승격 · ch12 치트시트 &amp; Stage 1~4').style.cssText = 'margin-top:28px;color:var(--fg2)';
      A(box, 'up', 0, { dur: 0.5 });
    },
  });

  // ch11 이론 (1/2) — LiteLLM 무코드 관측 & Langfuse
  DECK.slide({
    id: 'ch11-litellm',
    part: 'p4b',
    chap: 'ch11 LLMOps & LiteLLM',
    theme: 'night',
    dots: true,
    title: 'ch11 (1/2): LiteLLM 프록시 무코드 관측 → Langfuse 프롬프트 업로드',
    notes: '애플리케이션 코드를 수정하지 않고 LiteLLM Proxy를 경유시켜 Claude·ChatGPT·Gemini 호출 로그를 Langfuse Trace로 자동 수집합니다.',
    build(el, A) {
      const T = title(el, 'CH11 · ZERO-CODE OBSERVABILITY', '<span class="hl">LiteLLM 프록시</span> 무코드 관측으로 LLM 호출 → <span class="hb">Langfuse</span> 수집', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const w1 = win(el, { x: 100, y: 225, w: 920, h: 720, dark: true, title: 'ch11/support-assistant/litellm_proxy/litellm_config.yaml' });
      w1.body.innerHTML = `<pre class="code-block" style="background:transparent;border:0;padding:0;font-size:21px"><code>model_list:
  - model_name: gpt-4o-mini
    litellm_params: { model: openai/gpt-4o-mini, api_key: os.environ/OPENAI_API_KEY }
  - model_name: claude-3-5-sonnet
    litellm_params: { model: anthropic/claude-3-5-sonnet-20241022 }
  - model_name: gemini-2.5-flash
    litellm_params: { model: gemini/gemini-2.5-flash }

litellm_settings:
  success_callback: ["langfuse"]   # 앱 코드 수정 없는 무코드 관측!
  failure_callback: ["langfuse"]</code></pre>`;
      A(w1.el, 'up', 0.12, { dur: 0.45 });

      const c2 = card(el, { x: 1050, y: 225, w: 770, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">왜 LiteLLM 프록시인가?</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><code>OPENAI_BASE_URL=http://localhost:4000</code><br>앱 코드 수정 없이 엔드포인트만 변경해 무코드 관측을 연결.</li>
        <li><b>Any-Platform 단일 게이트웨이</b><br>Claude · ChatGPT · Gemini 호출 로그를 하나의 Trace 스트림으로 통합 수집.</li>
        <li><code>seed_prompts.py</code> · <code>trace_to_prompt.py</code><br>직접 업서트와 Trace 기반 프롬프트 승격 두 경로를 모두 지원.</li>
      </ul>`;
      A(c2, 'up', 0.22, { dur: 0.45 });
    },
  });

  // ch11 이론 (2/2) — Save as Prompt & fetch_prompt & 3종 Eval
  DECK.slide({
    id: 'ch11-evals',
    part: 'p4b',
    chap: 'ch11 Save as Prompt & Evals',
    theme: 'white',
    title: 'ch11 (2/2): Trace → "Save as Prompt" → fetch_prompt → 3종 Eval',
    notes: 'Traces 탭의 입력 페이로드를 Save as Prompt로 프롬프트 자산에 등록하고, 앱에서는 fetch_prompt.py로 production 라벨 버전을 가져와 3종 Eval로 회귀 검증합니다.',
    build(el, A) {
      const T = title(el, 'CH11 · PROMPT LIFECYCLE & EVALS', 'Trace <span class="hb">"Save as Prompt"</span> 승격 → <code>fetch_prompt</code> → 3종 Eval', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const flow = [
        ['Step 1 · Trace 추출', 'Traces 탭 입력 페이로드를 "Save as Prompt"로 승격 (<code>trace_to_prompt.py</code>로 로컬 재현)', '#DCE6FF', '#1E4FD0'],
        ['Step 2 · 버전 Fetch', '앱이 <code>fetch_prompt.py</code>로 <code>production</code> 라벨 프롬프트를 가져와 <code>{{var}}</code> 렌더링', '#D5F2E6', '#0B8A5F'],
        ['Step 3 · 3종 Eval 게이트', '코드 기반(형식/금지어) · LLM-as-Judge · 사람 평가 비교 후 배포(<code>regression_compare.py</code>)', '#FDE1E1', '#B42323'],
      ];
      flow.forEach(([hd, bd, bg, fg], i) => {
        const c = card(el, { x: 100 + i * 585, y: 230, w: 550, h: 350, pad: 30 });
        c.innerHTML = `<span class="chip" style="background:${bg};color:${fg}">${hd}</span>
          <div class="b2" style="margin-top:22px">${bd}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });

      const c4 = card(el, { x: 100, y: 620, w: 1720, h: 340, pad: 32 });
      c4.innerHTML = `<div class="h4">로컬 Langfuse Mock HTTP v2 서버 내장 (외부 키 없이 100% 재현)</div>
      <div class="b2" style="margin-top:14px"><code>tests/test_support_assistant.py</code> 실행 시 로컬 HTTP Mock 서버가 <code>/api/public/traces</code> 조회, 프롬프트 등록(<code>POST /api/public/v2/prompts</code>), 라벨 기반 Fetch(<code>GET ...?label=production</code>)를 모두 검증합니다.</div>`;
      A(c4, 'up', 0.34, { dur: 0.45 });
    },
  });

  // ch11 실습 + 모범 답안
  DECK.slide({
    id: 'ch11-lab',
    part: 'p4b',
    chap: 'ch11 실습 & 답안',
    theme: 'paper',
    title: 'ch11 실습: Trace 프롬프트 승격, Fetch & 3종 Eval 실행',
    notes: 'trace_to_prompt.py -> fetch_prompt.py -> run_evals.py 순서로 LLMOps 사이클 전체를 컨테이너 안에서 재현합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch11',
        userPrompt: `[ch11 LiteLLM 무코드 프록시 & Langfuse Save as Prompt 모범 답안 재현 프롬프트]
LiteLLM 무코드 관측 프록시, Trace->Prompt 승격(trace_to_prompt.py), 라벨 기반 프롬프트 조회(fetch_prompt.py), 3종 Eval 및 회귀 비교 모범 답안을 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조 및 심볼릭 링크
   - ch11-eval-and-llmops/support-assistant/litellm_proxy/ (litellm_config.yaml, zero_code_proxy_demo.py, client_claude.py, client_chatgpt.py, client_gemini.py)
   - ch11-eval-and-llmops/support-assistant/langfuse_ops.py (LangfuseOpsClient: HTTP v2 API 연동 및 오프라인 JSONL 폴백)
   - ch11-eval-and-llmops/support-assistant/trace_to_prompt.py , fetch_prompt.py , seed_prompts.py , prompting.py
   - ch11-eval-and-llmops/support-assistant/evaluator.py , regression_compare.py
   - ch11-eval-and-llmops/support-assistant/tests/test_support_assistant.py
   - 심볼릭 링크: ch11/support-assistant -> ../ch11-eval-and-llmops/support-assistant

2. 핵심 구현 명세
   - trace_to_prompt.py: extract_prompt_template_from_trace(trace_entry, variable_mapping) 및 promote_trace_as_prompt()로 Trace input의 샘플 값을 {{var}} 변수로 승격해 Prompt 자산 등록(--demo --json 지원).
   - fetch_prompt.py & prompting.py: fetch_and_compile_prompt(ops, prompt_name, ticket, label="production")로 production 라벨 프롬프트를 가져와 SupportTicket 변수로 컴파일(--demo --json 지원).
   - evaluator.py & regression_compare.py: evaluate_rule_based(), evaluate_reference_and_judge(), evaluate_safety_policy(), run_three_evals()와 compare_prompt_versions(dataset, "production", "candidate", ops) 회귀 비교.
   - tests/test_support_assistant.py: 외부 키 없이 로컬 Mock HTTP v2 서버로 Trace 조회·Prompt 등록·라벨 Fetch·3종 Eval을 모두 검증.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 ch11/support-assistant/trace_to_prompt.py --demo --json
   - python3 ch11/support-assistant/fetch_prompt.py --demo --json
   - python3 -m unittest discover -s ch11-eval-and-llmops/support-assistant/tests -p "test_*.py" -v`,
        kicker: 'CH11 · HANDS-ON LAB (25분)',
        heading: '제11장 실습: <span class="hb">Save as Prompt</span> + <code>fetch_prompt</code> + 3종 Eval',
        duration: '25분',
        missionTitle: 'LiteLLM 트레이스 기반 프롬프트 등록, Fetch 및 회귀 평가 완주',
        steps: [
          '<code>ch11/support-assistant/trace_to_prompt.py --demo --json</code><br>Trace 입력 페이로드에서 프롬프트를 추출해 Langfuse 자산으로 등록.',
          '<code>ch11/support-assistant/fetch_prompt.py --demo --json</code><br><code>production</code> 라벨 버전을 조회해 Mustache 변수 렌더링을 확인.',
          '<code>litellm_proxy/zero_code_proxy_demo.py</code> · <code>test_support_assistant.py</code><br>무코드 프록시 데모와 Mock HTTP v2 · 3종 Eval 통합 테스트를 실행.',
        ],
        runCmd: 'python3 ch11/support-assistant/trace_to_prompt.py --demo --json\npython3 ch11/support-assistant/fetch_prompt.py --demo --json\npython3 -m unittest discover -s ch11-eval-and-llmops/support-assistant/tests -p "test_*.py" -v',
        answerLabel: 'ch11 모범 답안 열기 (Tree + Mock API/Eval)',
        answerType: 'Tree + Python',
        answerSummary: '실제 Langfuse 서버가 없어도 로컬 Mock v2 API + JSONL 폴백으로 Trace 추출 → Prompt 승격 → Fetch → 3종 Eval 회귀 비교까지 끝까지 검증됩니다.',
        tree: `ch11-eval-and-llmops/support-assistant/  (# ch11/support-assistant)
├── litellm_proxy/ (litellm_config.yaml, zero_code_proxy_demo.py, client_*.py)
├── trace_to_prompt.py                 # Save as Prompt CLI/모듈
├── fetch_prompt.py                    # 라벨 기반 Prompt Fetch + {{var}}
├── seed_prompts.py · prompting.py · langfuse_ops.py
├── evaluator.py · regression_compare.py  # 3종 Eval & 회귀 비교
└── tests/test_support_assistant.py    # Mock HTTP v2 통합 테스트`,
        codeCaption: 'trace_to_prompt -> fetch_prompt -> run_evals 핵심 흐름',
        answerCode: `# 1) Trace payload -> Prompt (Save as Prompt)
promoted = extract_prompt_from_trace(trace_payload, name="support-reply", label="production")
# 2) Fetch & render Mustache variables
rendered = render_mustache(fetched["prompt"], {"customer_query": "환불 문의"})
# 3) Run 3-tier Evals -> pass_rate >= 0.85 PASS`,
      });
    },
  });

  // ch11 심화 (p.35): 실무에서 활용하는 3가지 평가(Eval) 기법과 알맞은 예시
  DECK.slide({
    id: 'ch11-eval-methods',
    part: 'p4b',
    chap: 'ch11 실무 3대 Eval 기법',
    theme: 'white',
    title: 'ch11 심화: 실무에서 활용하는 3가지 평가(Eval) 기법과 예시',
    notes: 'p.34 ch11 실습 직후, 실무 LLMOps 파이프라인에서 조합하는 3가지 평가(코드 기반 결정론적 평가, LLM-as-a-Judge, 사람 평가 & 운영 피드백)와 실제 예시를 정리합니다.',
    build(el, A) {
      const T = title(
        el,
        'CH11 · PRACTICAL 3-TIER EVALUATION METHODS',
        '실무에서 활용하는 <span class="hb">3가지 평가(Eval) 기법</span>과 실전 예시',
        { y: 56 },
      );
      A(T.t, 'up', 0, { dur: 0.4 });

      const methods = [
        [
          '01 · 코드 기반 결정론적 평가',
          'Code-based / Heuristic Eval',
          '매 커밋·CI마다 전수 실행 (비용 $0 · 수 ms).<br>JSON 스키마, 필수 섹션 포함, 금지어·PII 노출을 정규식·파서로 즉시 판정.',
          '#DCE6FF',
          '#1E4FD0',
          `# evaluator.py — 코드 기반 형식·금지어 검증 예시
def eval_code_rules(reply: str) -> bool:
    has_next_step = "다음 단계:" in reply
    no_forbidden = not re.search(r"(무조건\\s*환불|비밀번호\\s*요구)", reply)
    return has_next_step and no_forbidden and len(reply) >= 40`,
        ],
        [
          '02 · LLM-as-a-Judge 평가',
          'Model-based Rubric Scoring',
          '정답이 하나로 고정되지 않는 어조·친절도·근거 충실도(Faithfulness)를<br>0~3점 명시적 루브릭(Rubric)으로 채점 (근거 먼저 생성 후 점수 부여).',
          '#D5F2E6',
          '#0B8A5F',
          `# 0~3점 루브릭 Judge 프롬프트 & 출력 예시
[기준] 3점: 정책 근거 인용 + 다음 행동 안내 완비 / 0점: 환각·누락
{"reasoning": "환불 7일 규정 인용 및 주문번호 회신 안내 포함",
 "score": 3, "verdict": "PASS"}`,
        ],
        [
          '03 · 사람 평가 & 운영 피드백',
          'Human-in-the-Loop & Golden Dataset',
          '고위험 케이스·낮은 점수 Trace를 도메인 전문가(SME)가 검수해<br>교정 답변을 골든 데이터셋과 프롬프트(Save as Prompt)로 승격.',
          '#FDEFD3',
          '#9A5B00',
          `# Langfuse Trace -> Golden Dataset & 회귀 비교 예시
1) Langfuse에서 score < 0.7 Trace 필터링 & 전문가 교정 답변 작성
2) loop-triage-benchmark Dataset 추가 후 회귀 게이트 실행:
$ python3 ch11/support-assistant/regression_compare.py`,
        ],
      ];

      methods.forEach(([badge, sub, desc, bg, fg, codeEx], i) => {
        const c = card(el, { x: 100 + i * 585, y: 215, w: 550, h: 755, pad: 28 });
        c.style.cssText += ';display:flex;flex-direction:column';
        c.innerHTML = `<div style="height:250px;display:flex;flex-direction:column;align-items:flex-start">
            <span class="chip" style="background:${bg};color:${fg}">${badge}</span>
            <div class="h4" style="margin-top:16px">${sub}</div>
            <div class="b3" style="margin-top:12px;color:var(--fg2)">${desc}</div>
          </div>
          <div class="cap" style="color:var(--ink)">실전 코드 / 루브릭 예시</div>
          <pre class="code-block" style="margin-top:10px;font-size:17px;line-height:1.48;flex:1;margin-bottom:0"><code>${UI.esc(codeEx)}</code></pre>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });
    },
  });

  // ch12 이론
  DECK.slide({
    id: 'ch12-theory',
    part: 'p4b',
    chap: 'ch12 에필로그 & 로드맵',
    theme: 'white',
    title: 'ch12: 12대 스택 한눈에 보기 & 팀 도입 4단계(Stage 1~4)',
    notes: '모든 스택을 첫날부터 한꺼번에 도입하지 말고 Stage 1부터 점진적으로 성숙도를 높여야 합니다.',
    build(el, A) {
      const T = title(el, 'CH12 · EPILOGUE & ADOPTION ROADMAP', '한 번에 다 도입하지 마라 — <span class="hl">Stage 1~4</span> 점진적 도입 전략', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const stages = [
        ['Stage 1 · 개인 루프', 'ch01 · ch04', '단일 에이전트 CLI + 7항목 프롬프트 + AGENTS.md 규칙서', '#D5F2E6', '#0B8A5F'],
        ['Stage 2 · 도구와 안전', 'ch02 · ch03 · ch07', 'MCP 연결 + PreToolUse 가드레일 + 팀 Skills + 아키텍처 린터', '#DCE6FF', '#1E4FD0'],
        ['Stage 3 · 기억과 위임', 'ch05 · ch06 · ch08', 'Agentic RAG + TASKS/JOURNAL 메모리 + 서브에이전트 + Ralph Loop', '#E6E0FF', '#4D2FD0'],
        ['Stage 4 · 합의와 LLMOps', 'ch09 · ch10 · ch11', 'Maker!=Checker 블라인드 합의 + 아우터 루프 + LiteLLM/Langfuse Eval', '#FDEFD3', '#9A5B00'],
      ];
      stages.forEach(([s, ch, bd, bg, fg], i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const c = card(el, { x: 100 + col * 880, y: 230 + row * 370, w: 840, h: 330, pad: 32 });
        c.innerHTML = `<div class="row" style="justify-content:space-between"><span class="chip" style="background:${bg};color:${fg}">${s}</span><code style="font-size:20px">${ch}</code></div>
          <div class="b1" style="margin-top:24px">${bd}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });
    },
  });

  // ch12 최종 실습 + 모범 답안
  DECK.slide({
    id: 'ch12-lab',
    part: 'p4b',
    chap: 'ch12 최종 실습 & 답안',
    theme: 'paper',
    title: 'ch12 최종 실습: Stage 1~4 준비도 진단 & 전 단원 통합 검증',
    notes: '마지막 실습에서는 우리 팀의 성숙도 Stage를 진단하고 verify_chapters.py --all 로 전 단원 100% 통과를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch12',
        userPrompt: `[ch12 Stage 1~4 준비도 진단 & 통합 게이트 모범 답안 재현 프롬프트]
4계층 12대 스택 치트시트(README.md), Stage 1~4 성숙도 진단기(stage_readiness_check.py), 전 단원 통합 검증 게이트(verify_chapters.py --all) 모범 답안을 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - ch12-epilogue/README.md (4계층 12대 스택 한눈에 보기 치트시트 & Stage 1~4 점진적 도입 로드맵)
   - ch12-epilogue/stage_readiness_check.py
   - ch12-epilogue/tests/test_stage_readiness.py
   - scripts/verify_chapters.py (--all 옵션으로 루트·플랫폼·ch00~ch12·docs 웹 PPT 통합 검증)

2. 핵심 구현 명세 (stage_readiness_check.py)
   - inspect_stages(repo_root): 저장소의 stage_1_foundation(AGENTS.md/CLAUDE.md/verify_chapters.py), stage_2_role_separation(ch09 permissions.py/rubric.py), stage_3_outer_loop(ch10 loop.py/cost_logger.py), stage_4_llmops(ch11 evaluator.py/langfuse_ops.py) 존재 여부를 점검해 {"repo_root", "stages": {...}, "completed_stages": 4, "total_stages": 4}를 반환할 것.
   - CLI 옵션: --path, --format (text|json) 지원.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 ch12-epilogue/stage_readiness_check.py --format json
   - python3 -m unittest discover -s ch12-epilogue/tests -p "test_*.py" -v
   - python3 scripts/verify_chapters.py --all`,
        kicker: 'CH12 · FINAL CAPSTONE LAB (15분)',
        heading: '최종 실습: <span class="hl">Stage 1~4</span> 진단 &amp; 전 단원 통합 게이트',
        duration: '15분',
        missionTitle: '도입 성숙도 진단(stage_readiness_check.py) 및 전 단원 100% 검증 완주',
        steps: [
          '<code>ch12-epilogue/stage_readiness_check.py --format json</code><br>실행 후 현재 저장소의 Stage 1~4 도입 성숙도를 점검.',
          '<code>python3 scripts/verify_chapters.py --all</code><br>루트·플랫폼·ch00~ch12·웹 PPT 통합 검증 게이트를 실행.',
          '<code>git status</code> · <code>docs/index.html</code><br>워킹트리 클린 상태와 GitHub Pages 웹 PPT 렌더링을 최종 확인.',
        ],
        runCmd: 'python3 ch12-epilogue/stage_readiness_check.py --format json\npython3 scripts/verify_chapters.py --all',
        answerLabel: 'ch12 모범 답안 열기 (Tree + 최종 검증 결과)',
        answerType: 'Tree + Final Gate',
        answerSummary: 'Stage 1~4 체크리스트가 모두 충족되면 <code>verify_chapters.py --all</code>이 전 단원·플랫폼·웹 PPT 검사를 한 번에 PASS로 마칩니다.',
        tree: `learn_Loop_engineering/
├── docs/                  # GitHub Pages 5시간 웹 PPT + ARCHITECTURE.md
├── platforms/             # claude / chatgpt / gemini 어댑터
├── scripts/verify_chapters.py
├── ch00-prologue/ ~ ch11-eval-and-llmops/
└── ch12-epilogue/
    ├── README.md          # 4계층 치트시트
    ├── stage_readiness_check.py
    └── tests/test_stage_readiness.py`,
        codeCaption: '최종 통합 게이트 기대 출력',
        answerCode: `{
  "current_stage": 4,
  "stage_1_to_4_ready": true,
  "platforms_verified": ["claude", "chatgpt", "gemini"]
}
=== verify_chapters (all) [PASS] ... ===`,
      });
    },
  });

  // Closing (p.38)
  DECK.slide({
    id: 'closing',
    part: 'p4b',
    chap: '수료 & 마무리',
    theme: 'night',
    dots: true,
    noChrome: true,
    title: '5시간 과정 완주! 신뢰할 수 있는 에이전트 설계 마무리',
    notes: '수고하셨습니다! 각 단원의 실습 미션과 모범 답안을 팀 프로젝트에 바로 적용해 보세요.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:360px;width:1680px';
      chip(box, 'COMPLETED · 5-HOUR WORKSHOP', { bg: 'rgba(75,227,166,.18)', fg: '#4BE3A6' });
      h('div', 'h1', box, '이제 <span class="hl">신뢰할 수 있는 에이전트</span>를<br>직접 설계할 준비가 끝났습니다').style.cssText = 'margin-top:28px';
      A(box, 'up', 0, { dur: 0.55 });
    },
  });

  // p.39 (p.38 Closing 다음): 3세대 에이전트 퍼스트 체험 실습 — 다중 프로젝트 관리 루프에이전트
  DECK.slide({
    id: 'capstone-agent-first',
    part: 'p4b',
    chap: '3세대 에이전트 퍼스트 실습',
    theme: 'white',
    title: '체험 실습: 3세대 에이전트 퍼스트 다중 프로젝트 관리 루프에이전트',
    notes: '사용자 목표를 입력받아 스스로 판단·작업하는 3세대 에이전트 퍼스트 도구(Claude Code, Antigravity, ChatGPT Codex 등)를 활용하여 메타 하네스 루프에이전트(learn_LLM_Engineering) 구조를 자율 구축하는 체험 실습입니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'capstone',
        userPrompt: `[3세대 에이전트 퍼스트 체험 실습: 다중 프로젝트 관리 루프에이전트 구축 프롬프트]
사용자 목표를 자율적으로 판단·실행하는 3세대 에이전트 퍼스트 도구를 활용하여, 다음 5대 핵심 아키텍처 원칙에 따라 다중 프로젝트 관리 루프에이전트(learn_LLM_Engineering) 구조를 구축하고 검증해줘.

1. 호스트-컨테이너 분리:
   - 호스트 환경에서 복수 Docker 컨테이너를 통합 제어하는 어댑터 패턴 기반의 단일 에이전틱 오케스트레이션 상태 머신(run.py 및 orchestrator/) 구축.

2. 파일 매개 협업 (대화 컨텍스트 부패 차단):
   - 에이전트 간 대화 내역 직접 전달을 전면 배제하고, projects/<id>/docs/ 내 7종 표준 파일(CLIENT_BRIEF.md, PRD.md, PLAN.md, TASKS.md, IMPL.md, REVIEW.md, GIT_STATE.md, AUDIT.md)을 매개로 역할별 최소 컨텍스트만 주입(python3 run.py --project <id> --action context --role <role>).

3. Maker × Checker 1:1 분리 (자가 평가 편향 차단):
   - 작성자(Maker: specifier, planner, generator, git_manager)와 검증자(Checker: auditor, evaluator)를 1:1로 엄격 격리하여 자가 평가 편향을 원천 차단하고 블라인드 합의 및 품질 게이트 적용.

4. 5단계 운영 루프 & 계층별 선택적 롤백 (Selective Rollback):
   - DISCOVER(발견) -> PLAN(계획) -> EXECUTE(실행) -> VERIFY(검증) -> ITERATE(반복) 5단계 운영.
   - 검증 실패 시 전체 재시작 대신 실패 원인 계층별로 롤백: 구현/테스트 오류는 EXECUTE(07_IMPL_CODE), 계획/범위 모호성은 PLAN(05_PLAN_TASKS), 요구사항 결함은 DISCOVER(01_INTAKE_SPEC)로 선택적 되돌림.
   - 7대 완료·중단 조건(종료코드 0, 린트/테스트 통과, N회 연속 성공, 동일 오류 Stall 감지 차단, 비가역 작업 docs/HALT).

5. 통합 제어 표준화:
   - 컨테이너 제어 올인원 스크립트(run_port.sh) 및 프로젝트 레지스트리(project.yaml)를 표준화해 단일 명령으로 개발·배포·에이전트 실행 환경을 제어.

검증 명령 (전부 exit 0 통과 필수)
- python3 ch12-epilogue/stage_readiness_check.py --format json
- python3 scripts/verify_chapters.py --all`,
        kicker: 'CAPSTONE · AGENT-FIRST HANDS-ON (자율 체험)',
        heading: '체험 실습: 3세대 에이전트 퍼스트 <span class="hl">다중 프로젝트 관리 루프에이전트</span>',
        duration: '자율 실습',
        missionTitle: '사용자 목표 입력 → 스스로 판단·작업 수행하는 3세대 루프에이전트 체험',
        steps: [
          '<code>3세대 에이전트 퍼스트 CLI 기동</code><br>Claude Code, ChatGPT/Codex, Gemini/Antigravity 등 최신 에이전트 실행 환경 준비.',
          '<code>단축키 A로 해결 프롬프트 복사 & 투입</code><br>좌측 오버레이의 5대 핵심 아키텍처 원칙이 담긴 사용자 프롬프트를 에이전트에 입력.',
          '<code>learn_LLM_Engineering 구조 자동 형성 확인</code><br>호스트-컨테이너 분리, 7종 문서 허브, Maker×Checker 1:1 격리 워크스페이스 구축 결과를 검증.',
        ],
        runCmd: 'python3 ch12-epilogue/stage_readiness_check.py --format json\npython3 scripts/verify_chapters.py --all',
        answerLabel: '루프에이전트 아키텍처 & 구조 확인 (클릭하여 열기)',
        answerType: 'Tree + Architecture',
        answerSummary: '3세대 에이전트 퍼스트 도구는 모호한 사용자 목표를 받아 스스로 판단하며, 호스트-컨테이너 분리·파일 매개 협업·Maker×Checker 분리·선택적 롤백 구조를 완결합니다.',
        tree: `learn_LLM_Engineering/
├── AGENTS.md / project.yaml   # 프로젝트 레지스트리 & 하네스 규칙
├── run.py                     # 단일 에이전틱 오케스트레이션 상태 머신
├── run_port.sh                # 컨테이너 제어 올인원 스크립트
├── orchestrator/              # Maker x Checker, 선택적 롤백 제어기
├── fleet/                     # 전문 에이전트 플릿 매니페스트
└── projects/<project_id>/
    └── docs/                  # 7종 파일 매개 협업 허브
        ├── CLIENT_BRIEF.md · PRD.md · PLAN.md
        ├── TASKS.md (touch 지정) · IMPL.md
        ├── REVIEW.md (PASS/FAIL) · GIT_STATE.md
        └── decisions/ (*.planner.md, *.evaluator.md)`,
        codeCaption: '5단계 운영 루프 & 계층별 선택적 되돌림(Selective Rollback) 전이',
        answerCode: `# 검증 실패 시 원인 계층별 선택적 되돌림 규칙
if verify_result == "FAIL":
    if fail_cause == "implementation_or_test_error":
        next_step = "07_IMPL_CODE"      # EXECUTE 단계로 즉시 롤백
    elif fail_cause == "plan_ambiguity":
        next_step = "05_PLAN_TASKS"     # PLAN 단계로 롤백
    elif fail_cause == "requirement_defect":
        next_step = "01_INTAKE_SPEC"    # DISCOVER 단계로 롤백
elif verify_result == "PASS":
    next_step = "09_GIT_COMMIT_PUSH"    # 정상 릴리스 진행`,
      });
    },
  });
})();
