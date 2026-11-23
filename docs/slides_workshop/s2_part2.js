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
    title: 'Part 2 · 지식과 기억 (ch04 ~ ch05)',
    notes: 'Part 2는 프롬프트·컨텍스트 엔지니어링(ch04)과 Agentic RAG·지속 메모리(ch05)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:100px;top:270px;width:1040px';
      chip(box, 'PART 2', { bg: 'rgba(124,92,255,.28)', fg: '#C7B8FF' });
      h('div', 'h1', box, '모델이 무엇을 알고 기억할지<br><span class="hv">컨텍스트와 메모리</span> 설계').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch04 7항목 프롬프트 &amp; 컨텍스트 예산 · ch05 Agentic RAG &amp; TASKS/JOURNAL').style.cssText = 'margin-top:28px;color:#AEB8D3';
      A(box, 'up', 0, { dur: 0.5 });
      const capWrap = h('div', 'abs', el);
      capWrap.style.cssText = 'right:85px;top:90px;width:610px;height:900px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);border-radius:24px;padding:16px;box-shadow:0 28px 60px -22px rgba(8,14,34,.55);border:2px solid rgba(255,255,255,.22)';
      capWrap.innerHTML = `<img src="assets/cartoons/cap_05_in.jpg" alt="Part 2 도입 카툰: RAG·Context·Memory 사서·책상·수첩 비교" style="width:100%;height:100%;object-fit:contain;border-radius:14px;display:block">`;
      A(capWrap, 'up', 0.16, { dur: 0.5 });
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

  // ch05 이론
  DECK.slide({
    id: 'ch05-theory',
    part: 'p2',
    chap: 'ch05 RAG & Memory',
    theme: 'paper',
    title: 'ch05: Agentic RAG (하이브리드 검색+자기비평) & 지속 메모리',
    notes: '단순 Top-K 벡터 검색은 문맥이 끊기거나 근거가 부실해도 답을 만듭니다. Agentic RAG와 파일 기반 메모리(TASKS.md/JOURNAL.md)를 결합합니다.',
    build(el, A) {
      const T = title(el, 'CH05 · AGENTIC RAG & MEMORY', '단순 검색을 넘는 <span class="hl">Agentic RAG</span> &amp; 3단 기억 계층', { y: 64 });
      A(T.t, 'up', 0, { dur: 0.4 });

      const c1 = card(el, { x: 100, y: 230, w: 840, h: 720, pad: 34 });
      c1.innerHTML = `<div class="h3">Agentic RAG 파이프라인 (<code>agentic_rag.py</code>)</div>
      <ul class="lab-steps" style="margin-top:18px">
        <li><b>Query Rewrite</b><br>모호한 사용자 질의를 핵심 검색 키워드로 확장.</li>
        <li><b>Hybrid + RRF</b><br>TF-IDF 코사인 유사도와 키워드 점수를 Reciprocal Rank Fusion으로 결합.</li>
        <li><b>Self-Critique</b><br>근거 신뢰도가 기준 미달이면 재검색 루프를 실행.</li>
      </ul>`;
      A(c1, 'up', 0.1, { dur: 0.45 });

      const c2 = card(el, { x: 980, y: 230, w: 840, h: 720, pad: 34 });
      c2.innerHTML = `<div class="h3">파일 기반 지속 메모리 (<code>memory_manager.py</code>)</div>
      <div class="col" style="gap:16px;margin-top:20px">
        <div style="padding:18px;border-radius:14px;background:var(--green-l)"><b>Working Memory (작업 목록)</b> → <code>TASKS.md</code> (체크리스트 상태 유지)</div>
        <div style="padding:18px;border-radius:14px;background:var(--blue-l)"><b>Episodic Memory (작업 일지)</b> → <code>JOURNAL.md</code> (시도·오류·결정 누적)</div>
        <div style="padding:18px;border-radius:14px;background:var(--violet-l)"><b>Semantic Memory (지식 베이스)</b> → <code>KNOWLEDGE.md</code> / <code>CLAUDE/CHATGPT/GEMINI</code> 동기화</div>
      </div>`;
      A(c2, 'up', 0.2, { dur: 0.45 });
    },
  });

  // ch05 실습 + 모범 답안
  DECK.slide({
    id: 'ch05-lab',
    part: 'p2',
    chap: 'ch05 실습 & 답안',
    theme: 'white',
    title: 'ch05 실습: Agentic RAG 검색 재순위화 & 지속 메모리 기록',
    notes: 'agentic_rag.py로 쿼리 재작성·RRF 검색을 실행하고 memory_manager.py로 세션 간 상태 영속화를 확인합니다.',
    build(el, A) {
      buildLabSlide(el, A, {
        id: 'ch05',
        userPrompt: `[실습 해결용 사용자 프롬프트 — 현재 챕터 루트 폴더에서 AI CLI에 입력]
현재 챕터 폴더에서 AGENTS.md · CLAUDE.md · GEMINI.md 지침에 따라 Agentic RAG 발췌 검색과 지속 메모리(TASKS.md, JOURNAL.md) 상태를 조회해 출력해줘.

1) 프롬프트 1 (Agentic RAG 발췌 검색): python3 agentic_rag.py 를 실행해 corpus/ 문서 대상 질의 재작성 및 상위 발췌 결과를 출력해줘.
2) 프롬프트 2 (지속 메모리 상태 조회): python3 memory_manager.py --status --json 으로 TASKS.md 완료/대기 건수와 JOURNAL.md 기록 상태를 출력해줘.
3) 프롬프트 3 (단위 테스트 검증): python3 -m unittest discover -s tests -p "test_*.py" -v 를 실행해 발췌 상한 및 상태 전이 테스트를 검증해줘.`,
        kicker: 'CH05 · HANDS-ON LAB',
        heading: '제5장 실습: <span class="hv">Agentic RAG</span> &amp; 지속 메모리 실행',
        duration: '',
        missionTitle: '챕터 루트에 RAG·지속 메모리 구성 후 AI CLI 프롬프트로 조회 결과 출력',
        steps: [
          '<code>AGENTS.md</code> · <code>CLAUDE.md</code> · <code>GEMINI.md</code> · <code>.claude/</code> · <code>.gemini/</code><br>챕터 루트에 AI 지침서, <code>corpus/</code> 4종 문서, <code>agentic_rag.py</code>, <code>memory_manager.py</code>를 배치.',
          '<code>해당 챕터 폴더 이동 후 AI CLI 접속</code><br><code>TASKS.md</code> · <code>JOURNAL.md</code>가 있는 챕터 루트로 이동해 <code>claude</code> · <code>agy</code> · <code>codex</code>로 접속.',
          '<code>사용자 입력 프롬프트로 RAG·메모리 검증</code><br>아래 프롬프트 예시 3선(또는 단축키 A)을 입력해 RAG 검색 결과와 메모리 상태 JSON을 확인.',
        ],
        promptExamples: [
          '1) "python3 agentic_rag.py를 실행해 corpus/ 대상 하이브리드 검색 상위 발췌 결과를 보여줘."',
          '2) "python3 memory_manager.py --status --json으로 TASKS.md와 JOURNAL.md 상태를 출력해줘."',
          '3) "tests/test_memory_pattern.py 단위 테스트를 실행해 발췌 길이 상한과 상태 전이를 검증해줘."',
        ],
        runCmd: 'python3 agentic_rag.py\npython3 memory_manager.py --status --json\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + AI CLI 실행 결과)',
        answerType: 'Tree + JSON',
        answerSummary: '챕터 루트에서 AI CLI가 <code>corpus/</code> Agentic RAG 검색과 <code>TASKS.md</code>/<code>JOURNAL.md</code> 상태를 함께 조회·검증합니다.',
        tree: `project/
├── AGENTS.md · CLAUDE.md · GEMINI.md
├── .claude/rules/rag-memory.md · .gemini/settings.json
├── corpus/ (01~04_*.md)      # 외부 지식 저장소 (RAG)
├── agentic_rag.py            # Query Rewrite + Top-K 발췌 검색
├── memory_manager.py         # --status --json 지속 메모리 관리
├── TASKS.md · JOURNAL.md     # 세션 간 지속 상태 파일
└── tests/test_memory_pattern.py`,
        codeCaption: 'AI CLI 프롬프트 입력 후 기대 출력 (RAG 검색 + 메모리 상태)',
        answerCode: `{"query": "컨텍스트 오염 방어", "top_doc": "01_context_budget.md", "rrf_score": 0.0328}
{
  "tasks_total": 3,
  "tasks_done": 1,
  "tasks_pending": 2,
  "journal_entries": 1
}`,
      });
    },
  });
})();
