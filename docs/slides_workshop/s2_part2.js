(function () {
  const { h } = DECK;
  const { title, card, win, chip, buildLabSlide } = UI;

  // Part 2 Divider
  DECK.slide({
    id: 'p2-div',
    part: 'p2',
    chap: 'Part 2 시작',
    theme: 'ink',
    dots: true,
    title: 'Part 2 · 지식과 컨텍스트 (ch04)',
    notes: 'Part 2는 프롬프트·컨텍스트 엔지니어링과 4대 지침 층위(ch04)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 2', { bg: 'rgba(124,92,255,.28)', fg: '#C7B8FF' });
      h('div', 'h1', box, '모델이 무엇을 알고 집중할지<br><span class="hv">프롬프트와 컨텍스트</span> 설계').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch04 7항목 프롬프트 · 컨텍스트 예산 관리 · 4대 층위 지침').style.cssText = 'margin-top:28px;color:#AEB8D3';
      A(box, 'up', 0, { dur: 0.5 });
    },
  });

  // ch04 이론
  DECK.slide({
    id: 'ch04-theory',
    part: 'p2',
    chap: 'ch04 컨텍스트 엔지니어링',
    theme: 'paper',
    title: 'ch04: 7항목 프롬프트, 4대 지침 층위 & 컨텍스트 오염 방지',
    notes: '프롬프트 작성에서 한 걸음 나아가 토큰 예산(Context Budget), 4가지 오염 패턴(Lost in the Middle 등), 4계층 지침 우선순위를 배웁니다.',
    build(el, A) {
      const T = title(el, 'CH04 · CONTEXT ENGINEERING', '프롬프트를 넘어 <span class="hv">컨텍스트 예산</span>과 <span class="hl">4대 층위</span> 관리로', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 840, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">7항목 구조화 프롬프트 &amp; 4대 지침 층위</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><b>7항목 프롬프트 템플릿</b><br>Role · Goal · Context · Constraints · Few-shot · Format · Self-Check로 구성.</li>
        <li><b>4대 지침 층위 우선순위</b><br>System Global → Project Root(<code>AGENTS.md</code>) → Subdir → Skill 순으로 적용.</li>
        <li><code>guidelines_claude.md</code> · <code>chatgpt.md</code> · <code>gemini.md</code><br>3대 플랫폼에 맞춘 계층별 지침 포맷을 동시 제공.</li>
      </ul>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 230, w: 840, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">컨텍스트 4대 오염 &amp; <code>context_budget.py</code></div>
      <div class="col" style="gap:16px;margin-top:20px">
        <div style="padding:16px 20px;border-radius:14px;background:var(--red-l)"><b class="hr">1. Poisoning (환각 잔류)</b> — 잘못된 추론이 이후 턴을 오염</div>
        <div style="padding:16px 20px;border-radius:14px;background:var(--amber-l)"><b style="color:#9A5B00">2. Distraction (주의 분산)</b> — 불필요한 로그·파일 과다 투입</div>
        <div style="padding:16px 20px;border-radius:14px;background:var(--blue-l)"><b class="hb">3. Confusion (모순 지침)</b> — 상위/하위 규칙 충돌</div>
        <div style="padding:16px 20px;border-radius:14px;background:var(--violet-l)"><b class="hv">4. Clash (도구/형식 충돌)</b> — 포맷 불일치 → 압축·격리 필요</div>
      </div>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch04 실습 + 모범 답안
  DECK.slide({
    id: 'ch04-lab',
    part: 'p2',
    chap: 'ch04 실습 & 답안',
    theme: 'white',
    title: 'ch04 실습: 컨텍스트 예산 계산 & 플랫폼별 프롬프트 변환',
    notes: 'context_budget.py로 토큰 점유율을 계산하고 prompt_adapter.py로 Claude/ChatGPT/Gemini 형식으로 변환합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch04',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더의 4대 층위 지침(CLAUDE.md, .claude/rules/api.md, AGENTS.md, GEMINI.md)과 7항목 프롬프트 템플릿을 적용하고 컨텍스트 예산 분석 결과를 출력해줘.

1) 프롬프트 1 (7항목 템플릿 & 4대 층위 점검): prompt_template.txt(7항목)와 .claude/rules/api.md, few_shot_reference.txt 구성을 확인해 요약해줘.
2) 프롬프트 2 (컨텍스트 예산 & 압축 임계치 진단): python3 context_budget.py --json 과 --history-tokens 135000 실행 결과를 비교해 /compact 시점을 설명해줘.
3) 프롬프트 3 (단위 테스트 검증): python3 -m unittest discover -s tests -p "test_*.py" -v 실행 결과를 출력해줘.`,
        kicker: 'CH04 · HANDS-ON LAB',
        heading: '제4장 실습: <span class="hl">7항목 프롬프트</span> &amp; 컨텍스트 예산 진단',
        duration: '',
        missionTitle: '챕터 루트에 7항목 템플릿·4대 층위 지침 구성 후 AI CLI로 예산 분석 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/rules/api.md</code> · <code>.gemini/</code><br>4대 층위 지속 지침과 경로 한정 규칙 파일, <code>few_shot_reference.txt</code>를 작성.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br><code>prompt_template.txt</code>(7항목)와 <code>context_budget.py</code>가 있는 챕터 루트에서 AI CLI를 실행.',
          '<code>사용자 입력 프롬프트로 예산 진단 출력</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 7항목 점검 결과와 예산 JSON 출력을 확인.',
        ],
        promptExamples: [
          '1) "prompt_template.txt 7항목 구조와 .claude/rules/api.md 조건부 규칙을 점검해 요약해줘."',
          '2) "context_budget.py --json과 --history-tokens 135000을 실행해 압축 권고 시점을 비교해줘."',
          '3) "tests/test_context_engineering.py 단위 테스트를 실행해 전체 통과 결과를 출력해줘."',
        ],
        runCmd: 'python3 context_budget.py --json\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트의 상시 지침과 7항목 프롬프트를 AI CLI가 자동 참조해 규칙 준수 및 토큰 점유율 임계치 경보 JSON을 출력합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/api.md · .gemini/settings.json
├── prompt_template.txt         # [목표]~[보고 형식] 7항목
├── few_shot_reference.txt      # 입출력 참조 구현
├── context_budget.py           # 토큰 예산·압축 경보 분석기
└── tests/test_context_engineering.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (context_budget.py --json)',
        answerCode: `{
  "total_budget": 8000,
  "used_tokens": 6840,
  "usage_ratio": 0.855,
  "compression_recommended": true,
  "warning": "Context usage >= 75%: compact or /clear with TASKS.md"
}`,
      });
    },
  });
})();
