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
    title: 'Part 4A · 합의와 아우터 루프 (ch08 ~ ch09)',
    notes: 'Part 4A는 3-Agent 블라인드 합의 오케스트레이션(ch08)과 5단계 아우터 루프(ch09)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:100px;top:270px;width:1040px';
      chip(box, 'PART 4A', { bg: 'rgba(245,165,36,.2)', fg: '#F5A524' });
      h('div', 'h1', box, '작성자와 검증자의 분리,<br>그리고 <span class="ha">아우터 루프</span> 통제').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch08 3-Agent 블라인드 합의 · ch09 5단계 루프 &amp; 7대 중단 조건').style.cssText = 'margin-top:28px;color:#AEB8D3';
      A(box, 'up', 0, { dur: 0.5 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_08_in.jpg" alt="Part 4A 도입 카툰: 자가 채점 편향 문제 → 3-Agent 분리" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
    },
  });

  // ch08 이론
  DECK.slide({
    id: 'ch08-theory',
    part: 'p4a',
    chap: 'ch08 3-Agent 오케스트레이션',
    theme: 'paper',
    title: 'ch08: Maker != Checker (Planner · Generator · Evaluator)',
    notes: '작성자(Maker)가 스스로 채점하면 긍정 편향에 빠집니다. 파일 매개 블라인드 합의와 0~3점 채점표(Rubric)로 편향을 제거합니다.',
    build(el, A) {
      const T = title(el, 'CH08 · 3-AGENT ORCHESTRATION', '자기 평가 편향을 없애는 <span class="hb">3-Agent</span> &amp; <span class="hl">블라인드 합의</span>', { y: 64 });
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

  // ch08 실습 + 모범 답안
  DECK.slide({
    id: 'ch08-lab',
    part: 'p4a',
    chap: 'ch08 실습 & 답안',
    theme: 'white',
    title: 'ch08 실습: 3-Agent 오케스트레이터 & 블라인드 합의 시뮬레이션',
    notes: 'orchestrator.py를 실행해 touch 스코프 검증, 블라인드 합의, 0~3점 채점표 판정을 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch08',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더에서 3-Agent(Planner·Generator·Evaluator) 파일 매개 오케스트레이션과 블라인드 합의를 실행해 결과를 출력해줘.

1) 프롬프트 1 (3-Agent 합의 시뮬레이션): python3 run.py --mode sim --platform chatgpt 를 실행해 블라인드 합의와 루브릭 채점 판정 JSON을 출력해줘.
2) 프롬프트 2 (권한 매트릭스 & 채점표 점검): src/harness/permissions.py 의 역할별 권한 분리와 rubric.py 의 0~3점 채점 기준을 요약해줘.
3) 프롬프트 3 (HALT 에스컬레이션 & 테스트): python3 -m unittest discover -s tests -p "test_*.py" -v 로 3회 합의 불일치 docs/HALT 생성과 전체 테스트를 검증해줘.`,
        kicker: 'CH08 · HANDS-ON LAB',
        heading: '제8장 실습: <span class="hl">3-Agent 합의</span> &amp; 루브릭 채점 출력',
        duration: '',
        missionTitle: '챕터 루트에 3-Agent 파일 협업·루브릭 구성 후 AI CLI로 합의 결과 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서와 <code>run.py</code>, <code>src/harness/</code>(<code>orchestrator</code>, <code>consensus</code>, <code>rubric</code>, <code>permissions</code>)를 구성.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br>챕터 루트로 이동해 <code>claude</code> · <code>agy</code> · <code>codex</code>로 접속하여 Maker≠Checker 규칙을 로드.',
          '<code>사용자 입력 프롬프트로 합의·채점 실행</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 <code>consensus: agreed</code>와 <code>PASS</code> 결과를 확인.',
        ],
        promptExamples: [
          '1) "python3 run.py --mode sim --platform chatgpt를 실행해 3-Agent 합의 JSON을 출력해줘."',
          '2) "src/harness/permissions.py와 rubric.py의 역할 권한 분리 및 0~3점 채점 기준을 점검해줘."',
          '3) "tests/test_orchestration_harness.py로 3회 불일치 docs/HALT 생성을 검증해줘."',
        ],
        runCmd: 'python3 run.py --mode sim --platform chatgpt\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI가 3-Agent 파이프라인을 실행해 블라인드 합의 및 0~3점 루브릭 <code>PASS</code> 판정 JSON을 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/orchestration.md · .gemini/settings.json
├── run.py · pyproject.toml   # --mode sim|dry-run --platform claude|chatgpt|gemini
├── src/harness/
│   ├── orchestrator.py · consensus.py · rubric.py · permissions.py
│   └── prompts/ (planner.md, generator.md, evaluator.md)
└── tests/test_orchestration_harness.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (run.py --mode sim)',
        answerCode: `{
  "mode": "sim",
  "platform": "chatgpt",
  "consensus": "agreed",
  "rubric_avg": 2.5,
  "status": "PASS"
}`,
      });
    },
  });

  // ch09 이론
  DECK.slide({
    id: 'ch09-theory',
    part: 'p4a',
    chap: 'ch09 아우터 루프',
    theme: 'ink',
    dots: true,
    title: 'ch09: 아우터 루프 5단계, 선택적 되돌림 & 7대 완료·중단 조건',
    notes: '이해 부채(Comprehension Debt)를 남기지 않고 장시간 프로젝트를 완주하게 만드는 Outer Loop 구조를 배웁니다.',
    build(el, A) {
      const T = title(el, 'CH09 · OUTER LOOP ARCHITECTURE', '<span class="hl">5단계 운영 루프</span> · 선택적 되돌림 · <span class="ha">7대 완료/중단 조건</span>', { y: 64 });
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

  // ch09 실습 + 모범 답안
  DECK.slide({
    id: 'ch09-lab',
    part: 'p4a',
    chap: 'ch09 실습 & 답안',
    theme: 'paper',
    title: 'ch09 실습: 5단계 아우터 루프 & Stall/Rollback 검증',
    notes: 'ch09-outer-loop/loop.py를 실행해 CALC-001~004 완주, 선택적 되돌림, Stall 감지를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch09',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더에서 CALC-001~004 계약 태스크를 5단계 아우터 루프로 실행하고 7대 완료·중단 조건 검증 결과를 출력해줘.

1) 프롬프트 1 (5단계 아우터 루프 실행): python3 loop.py --platform claude 를 실행해 completed_tasks, halted_tasks, stop_reason, total_cost_usd 를 출력해줘.
2) 프롬프트 2 (독립 검증기 & 재시도 점검): sample_tasks/tasks_contract.json 과 calc_verifier.py 의 CALC-002 재시도 및 CALC-003 HALT 조건을 설명해줘.
3) 프롬프트 3 (비용 로거 & 단위 테스트): python3 -m unittest discover -s tests -p "test_*.py" -v 실행 결과를 출력해줘.`,
        kicker: 'CH09 · HANDS-ON LAB',
        heading: '제9장 실습: <span class="hl">아우터 루프</span> &amp; 7대 중단 조건 실행',
        duration: '',
        missionTitle: '챕터 루트에 5단계 루프·예산 제어기 구성 후 AI CLI로 완주 결과 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서, <code>loop.py</code>, <code>workers.py</code>, <code>cost_logger.py</code>, <code>sample_tasks/</code>를 배치.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br>챕터 루트에서 <code>claude</code> · <code>agy</code> · <code>codex</code>로 접속해 5단계 아우터 루프 지침을 로드.',
          '<code>사용자 입력 프롬프트로 아우터 루프 실행</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 태스크 완료/중단 상태와 비용 JSON을 확인.',
        ],
        promptExamples: [
          '1) "python3 loop.py --platform claude를 실행해 CALC-001~004 상태 전이와 비용 JSON을 출력해줘."',
          '2) "sample_tasks/calc_verifier.py의 독립 검증 규칙과 CALC-003 HALT 조건을 점검해줘."',
          '3) "tests/test_todo_loop.py를 실행해 재시도·의존성 순서·비용 로깅 테스트를 검증해줘."',
        ],
        runCmd: 'python3 loop.py --platform claude\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI가 아우터 루프를 구동해 <code>CALC-001~004</code> 완료 내역, 중단 사유, 누적 비용 JSON을 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/outer-loop.md · .gemini/settings.json
├── loop.py · workers.py · cost_logger.py · models.py
├── sample_tasks/ (tasks_contract.json, calc_verifier.py)
└── tests/test_todo_loop.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (loop.py --platform claude)',
        answerCode: `{
  "stop_reason": "all_tasks_completed",
  "completed_tasks": ["CALC-001", "CALC-002", "CALC-004"],
  "halted_tasks": ["CALC-003"],
  "turns_executed": 4,
  "total_cost_usd": 0.0024
}`,
      });
    },
  });
})();
