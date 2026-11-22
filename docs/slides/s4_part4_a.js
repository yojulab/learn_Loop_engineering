(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 4A Divider
  DECK.slide({
    id: 'p4a-div',
    part: 'p4a',
    chap: 'Part 4A 시작',
    theme: 'night',
    dots: true,
    title: 'Part 4A · 합의와 아우터 루프 (ch09 ~ ch10, 45분)',
    notes: 'Part 4A는 3-Agent 블라인드 합의 오케스트레이션(ch09)과 5단계 아우터 루프(ch10)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 4A · 45분', { bg: 'rgba(245,165,36,.2)', fg: '#F5A524' });
      h('div', 'h1', box, '작성자와 검증자의 분리,<br>그리고 <span class="ha">아우터 루프</span> 통제').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch09 3-Agent 블라인드 합의 · ch10 5단계 루프 &amp; 7대 중단 조건').style.cssText = 'margin-top:28px;color:#AEB8D3';
      A(box, 'up', 0, { dur: 0.5 });
    },
  });

  // ch09 이론
  DECK.slide({
    id: 'ch09-theory',
    part: 'p4a',
    chap: 'ch09 3-Agent 오케스트레이션',
    theme: 'paper',
    title: 'ch09: Maker != Checker (Planner · Generator · Evaluator)',
    notes: '작성자(Maker)가 스스로 채점하면 긍정 편향에 빠집니다. 파일 매개 블라인드 합의와 0~3점 채점표(Rubric)로 편향을 제거합니다.',
    build(el, A) {
      const T = title(el, 'CH09 · 3-AGENT ORCHESTRATION', '자기 평가 편향을 없애는 <span class="hb">3-Agent</span> &amp; <span class="hl">블라인드 합의</span>', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const roles = [
        ['1. Planner (설계자)', 'TASKS.md · touch 범위 지정\ndecisions/*.planner.md 작성', '#E6E0FF', '#4D2FD0'],
        ['2. Generator (구현자)', 'touch 범위 코드만 수정\nIMPL.md 결과 기록 (채점 금지)', '#DCE6FF', '#1E4FD0'],
        ['3. Evaluator (평가자)', '*.planner.md 열람 금지(블라인드)\n0~3점 Rubric · PASS/FAIL 판정', '#D5F2E6', '#0B8A5F'],
      ];
      roles.forEach(([r, d, bg, fg], i) => {
        const c = card(el, { x: 100 + i * 585, y: 230, w: 550, h: 340, pad: 30 });
        c.innerHTML = `<span class="chip" style="background:${bg};color:${fg}">${r}</span>
          <div class="b2" style="margin-top:22px;white-space:pre-line">${d}</div>`;
        A(c, 'up', 0.1 + i * 0.08, { dur: 0.45 });
      });

      const c4 = card(el, { x: 100, y: 610, w: 1720, h: 340, pad: 32 });
      c4.innerHTML = `<div class="h3">블라인드 합의 &amp; 3회 불일치 인간 에스컬레이션 (HALT)</div>
      <div class="b2" style="margin-top:16px">Planner와 Evaluator가 서로의 근거를 보지 않고 각각 <code>선택: A</code> / <code>선택: B</code>를 파일 첫 줄에 기록합니다. 오케스트레이터(<code>run.py</code> / <code>orchestrator.py</code>)가 첫 줄만 비교해 일치 시 자동 확정, 3회 불일치 시 <code>docs/HALT</code>를 생성합니다.</div>`;
      A(c4, 'up', 0.34, { dur: 0.45 });
    },
  });

  // ch09 실습 + 모범 답안
  DECK.slide({
    id: 'ch09-lab',
    part: 'p4a',
    chap: 'ch09 실습 & 답안',
    theme: 'white',
    title: 'ch09 실습: 3-Agent 오케스트레이터 & 블라인드 합의 시뮬레이션',
    notes: 'orchestrator.py를 실행해 touch 스코프 검증, 블라인드 합의, 0~3점 채점표 판정을 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch09',
        userPrompt: `[3-Agent 블라인드 합의 & 루브릭 모범 답안 재현 프롬프트]
Maker!=Checker(Planner·Generator·Evaluator) 역할 분리, touch 스코프 검증, 첫 줄 블라인드 합의 및 0~3점 루브릭 채점 하네스를 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - harness/run.py
   - harness/src/harness/orchestrator.py , consensus.py , rubric.py , permissions.py
   - harness/src/harness/prompts/ 하위에 planner, generator, evaluator 마크다운 프롬프트
   - harness/tests/test_orchestration_harness.py

2. 핵심 구현 명세
   - permissions.py: Generator가 TASKS.md에 명시된 touch 허용 경로 외 파일을 수정하지 않도록 검증.
   - consensus.py: CHOICE_RE = r"^선택\\s*:\\s*([A-Z])\\b", parse_choice_line(), evaluate_consensus(docs_dir, topic, attempt, max_attempts=3, irreversible=False) 구현. Planner(.planner.md)와 Evaluator(.evaluator.md)가 상호 문서를 열람하지 않은 채 첫 줄만 비교해 일치 시 ConsensusOutcome(status="AGREED"), max_attempts(3회) 불일치 또는 irreversible=True 시 docs/HALT 파일 생성 후 status="HALTED" 반환.
   - rubric.py: BASE_CRITERIA = ("spec_fit", "module_boundary", "test_rigor", "ops_readiness") 각 0~3점 채점(max_score=12 또는 ui_polish 포함 시 15, total>=9 PASS) 후 score_evaluation() 반환.
   - run.py & orchestrator.py: --mode sim|dry-run --platform claude|chatgpt|gemini CLI 지원.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 harness/run.py --mode sim --platform chatgpt
   - python3 -m unittest discover -s harness/tests -p "test_*.py" -v`,
        kicker: 'CH09 · HANDS-ON LAB (20분)',
        heading: '제9장 실습: <span class="hb">3-Agent 합의</span> &amp; 채점표(Rubric) 검증',
        duration: '20분',
        missionTitle: 'Planner-Generator-Evaluator 분리 실행 및 블라인드 합의 확인',
        steps: [
          '<code>harness/run.py --mode sim --platform chatgpt</code><br>3-Agent 오케스트레이션 시뮬레이터를 <code>claude|chatgpt|gemini</code> 모드로 실행.',
          '<code>harness/src/harness/consensus.py</code><br>첫 줄(<code>선택: X</code>) 비교 로직과 3회 불일치 시 <code>HALT</code> 생성을 검증.',
          '<code>harness/tests/test_orchestration_harness.py</code><br>0~3점 채점표(Rubric) 컷오프 판정 테스트를 실행.',
        ],
        runCmd: 'python3 harness/run.py --mode sim --platform chatgpt\npython3 -m unittest discover -s harness/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + 합의·채점표)',
        answerType: 'Tree + Python',
        answerSummary: '오케스트레이터(<code>run.py</code>)는 Planner의 선택안과 Evaluator의 선택안 첫 줄(<code>선택: X</code>)만 파싱해 일치 시 PASS, 불일치 누적 시 HALT를 트리거합니다.',
        tree: `harness/
├── run.py              # --mode sim|dry-run --platform claude|chatgpt|gemini
├── src/harness/ (orchestrator.py, consensus.py, rubric.py, permissions.py, prompts/)
└── tests/test_orchestration_harness.py`,
        codeCaption: '블라인드 합의 & 0~3점 채점표 요약',
        answerCode: `{
  "consensus": {"planner": "A", "evaluator": "A", "agreed": true},
  "rubric_score": {"correctness": 3, "tests": 3, "scope": 3, "total": 9},
  "verdict": "PASS"
}`,
      });
    },
  });

  // ch10 이론
  DECK.slide({
    id: 'ch10-theory',
    part: 'p4a',
    chap: 'ch10 아우터 루프',
    theme: 'ink',
    dots: true,
    title: 'ch10: 아우터 루프 5단계, 선택적 되돌림 & 7대 완료·중단 조건',
    notes: '이해 부채(Comprehension Debt)를 남기지 않고 장시간 프로젝트를 완주하게 만드는 Outer Loop 구조를 배웁니다.',
    build(el, A) {
      const T = title(el, 'CH10 · OUTER LOOP ARCHITECTURE', '<span class="hl">5단계 운영 루프</span> · 선택적 되돌림 · <span class="ha">7대 완료/중단 조건</span>', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 840, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">5단계 &amp; 선택적 되돌림 (Selective Rollback)</div>
      <div class="b2" style="margin-top:16px"><b>DISCOVER → PLAN → EXECUTE → VERIFY → ITERATE</b></div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><b>구현/테스트 오류</b><br>처음부터 재시작하지 않고 즉시 <code>EXECUTE</code> 단계로 되돌림.</li>
        <li><b>범위/설계 모호성</b><br><code>PLAN</code> 단계로 돌아가 작업 분해와 <code>touch</code>를 보완.</li>
        <li><b>전제/요구사항 오류</b><br><code>DISCOVER</code> 단계로 되돌아가 의뢰 사양을 재확인.</li>
      </ul>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 230, w: 840, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">완료 3기준 + 중단 4기준 (7대 조건)</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><b>완료 조건 (3가지)</b><br>종료 코드 0(성공) · 린트/커버리지(품질) · N회 연속 통과(안정성).</li>
        <li><b>중단 조건 (4가지)</b><br>반복·비용 한도 초과, Stall(상태 불변·동일 오류), 비가역 작업 <code>HALT</code>.</li>
        <li><code>CALC-001</code> ~ <code>CALC-004</code><br><code>loop.py</code>로 4대 목표 상태 전이와 완료 리포트를 생성.</li>
      </ul>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch10 실습 + 모범 답안
  DECK.slide({
    id: 'ch10-lab',
    part: 'p4a',
    chap: 'ch10 실습 & 답안',
    theme: 'paper',
    title: 'ch10 실습: 5단계 아우터 루프 & Stall/Rollback 검증',
    notes: 'ch10/todo-loop/loop.py를 실행해 CALC-001~004 완주, 선택적 되돌림, Stall 감지를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch10',
        userPrompt: `[5단계 아우터 루프 & 7대 조건 제어기 모범 답안 재현 프롬프트]
5단계(DISCOVER->PLAN->EXECUTE->VERIFY->ITERATE) 아우터 루프 상태 전이, 선택적 롤백, 7대 완료·중단 조건 제어기(loop.py) 모범 답안을 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - todo-loop/models.py , workers.py , cost_logger.py , loop.py
   - todo-loop/sample_tasks/ 하위에 tasks_contract.json (CALC-001~CALC-004 계약 정의) 및 calc_verifier.py
   - todo-loop/tests/test_todo_loop.py

2. 핵심 구현 명세
   - models.py: TaskContract, LoopBudget(max_turns, max_retries_per_task, max_cost_usd), LoopResult, StopReason Enum(DONE, HALT_HUMAN_DECISION, HALT_BUDGET_EXCEEDED, HALT_MAX_RETRIES 등).
   - workers.py & cost_logger.py: BaseWorker, DeterministicTestWorker, LLMWorker(platform 지원) 및 토큰·비용 JSONL 기록기 CostLogger(total_cost_usd 계산).
   - loop.py: OuterLoopController(tasks, worker, budget, cost_logger). 의존성(_dependencies_done) 확인 -> 사람 승인 필요(requires_human_decision) 시 HALT_HUMAN_DECISION 중단 -> max_retries_per_task/max_cost_usd 가드 내 worker.run_task() & verify_task_independently() 실행 -> --platform auto|claude|chatgpt|gemini|offline 지원 및 JSON 결과(stop_reason, completed_tasks, halted_tasks, turns_executed, total_cost_usd) 출력.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 todo-loop/loop.py --platform claude
   - python3 -m unittest discover -s todo-loop/tests -p "test_*.py" -v`,
        kicker: 'CH10 · HANDS-ON LAB (25분)',
        heading: '제10장 실습: <span class="ha">아우터 루프</span> 실행 &amp; Stall/Rollback 검증',
        duration: '25분',
        missionTitle: 'CALC-001~004 아우터 루프 완주 및 7대 완료/중단 조건 테스트',
        steps: [
          '<code>AGENT_PLATFORM=gemini python3 todo-loop/loop.py --platform gemini</code><br>실행 후 5단계 상태 전이와 <code>CALC-001~004</code> 결과를 확인.',
          '<code>tests/test_todo_loop.py</code><br>동일 오류 반복(Stall) 시 자동 중단과 선택적 되돌림 케이스를 검증.',
          '<code>docs/ARCHITECTURE.md</code><br>아우터 루프 설계 사양과 실제 구현 흐름을 비교.',
        ],
        runCmd: 'python3 todo-loop/loop.py --platform claude\npython3 -m unittest discover -s todo-loop/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + 7대 조건)',
        answerType: 'Tree + Output',
        answerSummary: '<code>loop.py</code>는 상태 불변 또는 동일 에러 시그니처가 2회 연속 발생하면 즉시 <code>STALL_HALT</code>로 전환해 무한 토큰 소모를 차단합니다.',
        tree: `todo-loop/
├── loop.py · workers.py · cost_logger.py · models.py
├── sample_tasks/ (calc_verifier.py, tasks_contract.json)
└── tests/test_todo_loop.py`,
        codeCaption: 'loop.py 실행 및 7대 조건 출력 요약',
        answerCode: `[DISCOVER -> PLAN -> EXECUTE -> VERIFY -> COMPLETE]
Tasks done: CALC-001, CALC-002, CALC-003, CALC-004 (4/4)
Conditions: exit_zero=True, quality=True, stability_streak=2, stall_detected=False`,
      });
    },
  });
})();
