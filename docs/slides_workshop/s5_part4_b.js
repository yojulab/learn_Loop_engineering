(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 4B Divider
  DECK.slide({
    id: 'p4b-div',
    part: 'p4b',
    chap: 'Part 4B 시작',
    theme: 'paper',
    title: 'Part 4B · Eval, LLMOps & 실전 로드맵 (ch10 ~ ch11)',
    notes: '마지막 블록은 LiteLLM 프록시 + Langfuse Save as Prompt + 3종 Eval(ch10)과 Stage 1~4 도입 전략(ch11)으로 마무리합니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:100px;top:270px;width:1040px';
      chip(box, 'PART 4B', { bg: 'var(--red-l)', fg: 'var(--red)' });
      h('div', 'h1', box, '관측과 평가(<span class="hr">Eval/LLMOps</span>),<br>그리고 팀 도입 4단계').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch10 LiteLLM 무코드 프록시 &amp; Langfuse 프롬프트 승격 · ch11 치트시트 &amp; Stage 1~4').style.cssText = 'margin-top:28px;color:var(--fg2)';
      A(box, 'up', 0, { dur: 0.5 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_10_in.jpg" alt="Part 4B 도입 카툰: 어제는 됐는데 오늘 이상해 → LLMOps" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
    },
  });

  // ch10 이론 (1/2) — LiteLLM 무코드 관측 & Langfuse
  DECK.slide({
    id: 'ch10-litellm',
    part: 'p4b',
    chap: 'ch10 LLMOps & LiteLLM',
    theme: 'night',
    dots: true,
    title: 'ch10 (1/2): LiteLLM 프록시 무코드 관측 → Langfuse 프롬프트 업로드',
    notes: '애플리케이션 코드를 수정하지 않고 LiteLLM Proxy를 경유시켜 Claude·ChatGPT·Gemini 호출 로그를 Langfuse Trace로 자동 수집합니다.',
    build(el, A) {
      const T = title(el, 'CH10 · ZERO-CODE OBSERVABILITY', '<span class="hl">LiteLLM 프록시</span> 무코드 관측으로 LLM 호출 → <span class="hb">Langfuse</span> 수집', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const w1 = win(el, { x: 100, y: 225, w: 920, h: 720, dark: true, title: 'ch10-eval-and-llmops/litellm_proxy/litellm_config.yaml' });
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

  // ch10 이론 (2/2) — Save as Prompt & fetch_prompt & 3종 Eval
  DECK.slide({
    id: 'ch10-evals',
    part: 'p4b',
    chap: 'ch10 Save as Prompt & Evals',
    theme: 'white',
    title: 'ch10 (2/2): Trace → "Save as Prompt" → fetch_prompt → 3종 Eval',
    notes: 'Traces 탭의 입력 페이로드를 Save as Prompt로 프롬프트 자산에 등록하고, 앱에서는 fetch_prompt.py로 production 라벨 버전을 가져와 3종 Eval로 회귀 검증합니다.',
    build(el, A) {
      const T = title(el, 'CH10 · PROMPT LIFECYCLE & EVALS', 'Trace <span class="hb">"Save as Prompt"</span> 승격 → <code>fetch_prompt</code> → 3종 Eval', { y: 64 });
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

  // ch10 실습 + 모범 답안
  DECK.slide({
    id: 'ch10-lab',
    part: 'p4b',
    chap: 'ch10 실습 & 답안',
    theme: 'paper',
    title: 'ch10 실습: Trace 프롬프트 승격, Fetch & 3종 Eval 실행',
    notes: 'trace_to_prompt.py -> fetch_prompt.py -> run_evals.py 순서로 LLMOps 사이클 전체를 컨테이너 안에서 재현합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch10',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더에서 Trace->Prompt 승격(Save as Prompt), 프롬프트 Fetch, 3종 Eval 회귀 비교를 실행해 출력해줘.

1) 프롬프트 1 (Save as Prompt & Fetch): python3 trace_to_prompt.py --demo --json 과 python3 fetch_prompt.py --demo --json 을 실행해 {{var}} 템플릿 승격과 컴파일 결과를 보여줘.
2) 프롬프트 2 (3종 Eval 회귀 비교): python3 regression_compare.py 를 실행해 production(v1) vs candidate(v2) 점수와 통과율을 비교해줘.
3) 프롬프트 3 (무코드 프록시 & 통합 테스트): python3 litellm_proxy/zero_code_proxy_demo.py 와 python3 -m unittest discover -s tests -p "test_*.py" -v 결과를 출력해줘.`,
        kicker: 'CH10 · HANDS-ON LAB',
        heading: '제10장 실습: <span class="hl">Save as Prompt</span> &amp; 3종 Eval 출력',
        duration: '',
        missionTitle: '챕터 루트에 프록시·Eval 구성 후 AI CLI 프롬프트로 회귀 평가 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서, <code>litellm_proxy/</code>, <code>langfuse_ops.py</code>, <code>trace_to_prompt.py</code>, <code>evaluator.py</code>를 배치.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br>챕터 루트에서 <code>claude</code> · <code>agy</code> · <code>codex</code>로 접속해 LLMOps 평가 규칙을 로드.',
          '<code>사용자 입력 프롬프트로 승격·회귀 평가 실행</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 프롬프트 컴파일 및 버전별 <code>avg_score</code>·<code>pass_rate</code>를 확인.',
        ],
        promptExamples: [
          '1) "trace_to_prompt.py --demo --json과 fetch_prompt.py --demo --json으로 승격·컴파일을 확인해줘."',
          '2) "python3 regression_compare.py를 실행해 production vs candidate 3종 Eval 점수를 비교해줘."',
          '3) "litellm_proxy/zero_code_proxy_demo.py와 tests/test_support_assistant.py를 실행해 검증해줘."',
        ],
        runCmd: 'python3 trace_to_prompt.py --demo --json\npython3 fetch_prompt.py --demo --json\npython3 regression_compare.py\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI가 프롬프트 승격·컴파일과 <code>production</code> vs <code>candidate</code> 3종 Eval 회귀 비교 결과를 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/eval-llmops.md · .gemini/settings.json
├── litellm_proxy/ (litellm_config.yaml, zero_code_proxy_demo.py, cli_openai_bridge.py)
├── langfuse_ops.py · cli_litellm_eval.py · seed_langfuse_dashboard.py
├── trace_to_prompt.py · fetch_prompt.py · prompting.py
├── evaluator.py · regression_compare.py
└── tests/test_support_assistant.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (승격 + 회귀 비교)',
        answerCode: `// trace_to_prompt.py -> production 승격 완료 ({{ticket_id}}, {{product}})
// regression_compare.py:
{
  "production": {"version": 1.0, "avg_score": 0.483, "pass_rate": 0.333},
  "candidate":  {"version": 2.0, "avg_score": 0.872, "pass_rate": 1.0}
}`,
      });
    },
  });

  // ch10 심화 (p.35): 실무에서 활용하는 3가지 평가(Eval) 기법과 알맞은 예시
  DECK.slide({
    id: 'ch10-eval-methods',
    part: 'p4b',
    chap: 'ch10 실무 3대 Eval 기법',
    theme: 'white',
    title: 'ch10 심화: 실무에서 활용하는 3가지 평가(Eval) 기법과 예시',
    notes: 'p.34 ch10 실습 직후, 실무 LLMOps 파이프라인에서 조합하는 3가지 평가(코드 기반 결정론적 평가, LLM-as-a-Judge, 사람 평가 & 운영 피드백)와 실제 예시를 정리합니다.',
    build(el, A) {
      const T = title(
        el,
        'CH10 · PRACTICAL 3-TIER EVALUATION METHODS',
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
$ python3 ch10-eval-and-llmops/regression_compare.py`,
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

  // ch11 이론
  DECK.slide({
    id: 'ch11-theory',
    part: 'p4b',
    chap: 'ch11 에필로그 & 로드맵',
    theme: 'white',
    title: 'ch11: 11대 스택 한눈에 보기 & 팀 도입 4단계(Stage 1~4)',
    notes: '모든 스택을 첫날부터 한꺼번에 도입하지 말고 Stage 1부터 점진적으로 성숙도를 높여야 합니다.',
    build(el, A) {
      const T = title(el, 'CH11 · EPILOGUE & ADOPTION ROADMAP', '한 번에 다 도입하지 마라 — <span class="hl">Stage 1~4</span> 점진적 도입 전략', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const stages = [
        ['Stage 1 · 개인 루프', 'ch01 · ch04', '단일 에이전트 CLI + 7항목 프롬프트 + AGENTS.md 규칙서', '#D5F2E6', '#0B8A5F'],
        ['Stage 2 · 도구와 안전', 'ch02 · ch03 · ch06', 'MCP 연결 + PreToolUse 가드레일 + 팀 Skills + 아키텍처 린터', '#DCE6FF', '#1E4FD0'],
        ['Stage 3 · 위임과 자율 루프', 'ch05 · ch07', '서브에이전트 역할 분리 + 동적 병렬 워크플로 + Ralph Loop(/goal)', '#E6E0FF', '#4D2FD0'],
        ['Stage 4 · 합의와 LLMOps', 'ch08 · ch09 · ch10', 'Maker!=Checker 블라인드 합의 + 아우터 루프 + LiteLLM/Langfuse Eval', '#FDEFD3', '#9A5B00'],
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

  // ch11 최종 실습 + 모범 답안
  DECK.slide({
    id: 'ch11-lab',
    part: 'p4b',
    chap: 'ch11 최종 실습 & 답안',
    theme: 'paper',
    title: 'ch11 최종 실습: Stage 1~4 준비도 진단 & 전 단원 통합 검증',
    notes: '마지막 실습에서는 우리 팀의 성숙도 Stage를 진단하고 verify_chapters.py --all 로 전 단원 100% 통과를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch11',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더에서 저장소의 Stage 1~4 도입 성숙도를 진단하고 전체 통합 검증 게이트 실행 결과를 출력해줘.

1) 프롬프트 1 (Stage 1~4 성숙도 진단): python3 stage_readiness_check.py --format json 을 실행해 completed_stages: 4/4 달성 여부를 출력해줘.
2) 프롬프트 2 (진단기 단위 테스트): python3 -m unittest discover -s tests -p "test_*.py" -v 로 Stage 누락/완비 시나리오를 검증해줘.
3) 프롬프트 3 (전 단원 통합 게이트): python3 scripts/verify_chapters.py --all 을 실행해 전 단원 통합 게이트 PASS 요약을 출력해줘.`,
        kicker: 'CH11 · FINAL CAPSTONE LAB',
        heading: '제11장 실습: <span class="hl">Stage 1~4 성숙도</span> 진단 &amp; 통합 게이트',
        duration: '',
        missionTitle: '챕터 루트에 Stage 1~4 진단기 구성 후 AI CLI로 전체 게이트 결과 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서, 4계층 치트시트(<code>README.md</code>), <code>stage_readiness_check.py</code>를 배치.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br>챕터 루트에서 <code>claude</code> · <code>agy</code> · <code>codex</code>로 접속해 도입 체크리스트 지침을 로드.',
          '<code>사용자 입력 프롬프트로 최종 게이트 검증</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 <code>completed_stages: 4/4</code> 및 통합 게이트 <code>PASS</code>를 확인.',
        ],
        promptExamples: [
          '1) "python3 stage_readiness_check.py --format json으로 Stage 1~4 성숙도(4/4)를 진단해줘."',
          '2) "tests/test_stage_readiness.py 단위 테스트를 실행해 Stage별 판정 로직을 검증해줘."',
          '3) "verify_chapters.py --all을 실행해 전 단원 통합 게이트 PASS 리포트를 출력해줘."',
        ],
        runCmd: 'python3 stage_readiness_check.py --format json\npython3 scripts/verify_chapters.py --all',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI가 <code>stage_readiness_check.py</code>와 <code>verify_chapters.py --all</code>을 순차 실행해 전 단원 100% PASS 리포트를 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/readiness.md · .gemini/settings.json
├── README.md                  # 4계층 아키텍처 치트시트 & 프롬프트 예시 3선
├── stage_readiness_check.py   # Stage 1~4 성숙도 진단 CLI
└── tests/test_stage_readiness.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (Stage 1~4 + 통합 게이트 PASS)',
        answerCode: `{
  "stages": {
    "stage_1_foundation": true,
    "stage_2_role_separation": true,
    "stage_3_outer_loop": true,
    "stage_4_llmops": true
  },
  "completed_stages": 4,
  "total_stages": 4
}
=== verify_chapters (all) [PASS] (56/56) ===`,
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
    title: '워크숍 완주! 신뢰할 수 있는 에이전트 설계 마무리',
    notes: '수고하셨습니다! 각 단원의 실습 미션과 모범 답안을 팀 프로젝트에 바로 적용해 보세요.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:100px;top:300px;width:1040px';
      chip(box, 'COMPLETED · CARTOON WORKSHOP', { bg: 'rgba(75,227,166,.18)', fg: '#4BE3A6' });
      h('div', 'h1', box, '이제 <span class="hl">신뢰할 수 있는 에이전트</span>를<br>직접 설계할 준비가 끝났습니다').style.cssText = 'margin-top:28px';
      h('div', 'b1', box, '우리 팀에 딱 맞는 최소 스택부터 시작해 4계층 검증 루프로 확장해 보세요.').style.cssText = 'margin-top:24px;color:#AEB8D3';
      A(box, 'up', 0, { dur: 0.55 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_11_out.jpg" alt="에필로그 마무리 카툰: 최소 도입 로드맵 & 우리 팀에 딱 맞는 스택부터!" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
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
        userPrompt: `[3세대 에이전트 퍼스트 체험 실습 — 신규 프로젝트 폴더에서 AI CLI에 입력]
사용자 목표를 자율적으로 판단·실행하는 3세대 에이전트 퍼스트 도구를 활용하여, 다음 5대 핵심 아키텍처 원칙에 따라 다중 프로젝트 관리 루프에이전트(learn_LLM_Engineering) 구조를 구축하고 실행 결과를 출력해줘.

1. 호스트-컨테이너 분리:
   - 호스트 환경에서 복수 Docker 컨테이너를 통합 제어하는 어댑터 패턴 기반의 단일 에이전틱 오케스트레이션 상태 머신(run.py 및 orchestrator/) 구축.

2. 파일 매개 협업 (대화 컨텍스트 부패 차단):
   - 에이전트 간 대화 내역 직접 전달을 전면 배제하고, projects/<id>/docs/ 내 7종 표준 파일(CLIENT_BRIEF.md, PRD.md, PLAN.md, TASKS.md, IMPL.md, REVIEW.md, GIT_STATE.md, AUDIT.md)을 매개로 역할별 최소 컨텍스트만 주입(python3 run.py --project <id> --action context --role <role>).

3. Maker × Checker 1:1 분리 (자가 평가 편향 차단):
   - 작성자(Maker: specifier, planner, generator, git_manager)와 검증자(Checker: auditor, evaluator)를 1:1로 엄격 격리하여 자가 평가 편향을 원천 차단하고 블라인드 합의 및 품질 게이트 적용.

4. 5단계 운영 루프 & 계층별 선택적 롤백 (Selective Rollback):
   - DISCOVER(발견) -> PLAN(계획) -> EXECUTE(실행) -> VERIFY(검증) -> ITERATE(반복) 5단계 운영.
   - 검증 실패 시 실패 원인 계층별 롤백: 구현/테스트 오류 -> EXECUTE(07_IMPL_CODE), 계획/범위 모호성 -> PLAN(05_PLAN_TASKS), 요구사항 결함 -> DISCOVER(01_INTAKE_SPEC).

5. 통합 제어 표준화 & 결과 출력:
   - run_port.sh, project.yaml 표준화 후 생성된 디렉터리 구조와 상태 전이 시뮬레이션, 검증 명령(stage_readiness_check.py --format json, scripts/verify_chapters.py --all) 통과 결과를 출력할 것.`,
        kicker: 'CAPSTONE · AGENT-FIRST HANDS-ON (자율 체험)',
        heading: '체험 실습: 3세대 에이전트 퍼스트 <span class="hl">다중 프로젝트 관리 루프에이전트</span>',
        duration: '',
        missionTitle: '신규 프로젝트 폴더에서 3세대 AI CLI 접속 → 사용자 프롬프트로 루프에이전트 구축',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>신규 작업 폴더에서 Claude Code, ChatGPT/Codex, Gemini/Antigravity 등 3세대 AI CLI를 기동.',
          '<code>5대 핵심 아키텍처 원칙 프롬프트 입력</code><br>호스트-컨테이너 분리, 7종 파일 매개 협업, Maker×Checker 1:1 격리, 선택적 롤백, <code>project.yaml</code> 표준화를 지시.',
          '<code>구축된 구조 및 검증 결과 출력 확인</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 상태 머신·문서 허브와 검증 게이트 통과 결과를 확인.',
        ],
        promptExamples: [
          '1) "5대 원칙(호스트-컨테이너 분리, 7종 파일 협업, Maker×Checker 1:1 격리)으로 run.py와 orchestrator/를 구축해줘."',
          '2) "검증 실패 원인별로 EXECUTE(07)·PLAN(05)·DISCOVER(01)로 되돌리는 선택적 롤백 상태 머신을 시뮬레이션해줘."',
          '3) "stage_readiness_check.py --format json과 verify_chapters.py --all을 실행해 구축 결과를 검증해줘."',
        ],
        runCmd: 'python3 stage_readiness_check.py --format json\npython3 scripts/verify_chapters.py --all',
        answerLabel: '루프에이전트 아키텍처 & AI CLI 결과 확인 (클릭하여 열기)',
        answerType: 'Tree + Architecture',
        answerSummary: '3세대 에이전트 퍼스트 도구는 모호한 사용자 목표를 받아 스스로 판단하며, 호스트-컨테이너 분리·파일 매개 협업·Maker×Checker 분리·선택적 롤백 구조를 완결해 출력합니다.',
        tree: `learn_LLM_Engineering/
├── AGENTS.md · CLAUDE.md · GEMINI.md · .claude/ · .gemini/
├── project.yaml · run.py · run_port.sh
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
