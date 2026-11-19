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
    title: 'Part 2 · 지식과 기억 (ch04 ~ ch05, 45분)',
    notes: 'Part 2는 프롬프트·컨텍스트 엔지니어링(ch04)과 Agentic RAG·지속 메모리(ch05)를 다룹니다.',
    build(el, A) {
      const box = h('div', 'abs', el);
      box.style.cssText = 'left:120px;top:300px;width:1500px';
      chip(box, 'PART 2 · 45분', { bg: 'rgba(124,92,255,.28)', fg: '#C7B8FF' });
      h('div', 'h1', box, '모델이 무엇을 알고 기억할지<br><span class="hv">컨텍스트와 메모리</span> 설계').style.cssText = 'margin-top:24px';
      h('div', 'b1', box, 'ch04 7항목 프롬프트 &amp; 컨텍스트 예산 · ch05 Agentic RAG &amp; TASKS/JOURNAL').style.cssText = 'margin-top:28px;color:#AEB8D3';
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
        <li><code>prompt_adapter.py</code><br>Claude XML · ChatGPT JSON Schema · Gemini Instruction 포맷으로 변환.</li>
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
        kicker: 'CH04 · HANDS-ON LAB (20분)',
        heading: '제4장 실습: <span class="hv">컨텍스트 예산</span> 계산 &amp; 프롬프트 어댑팅',
        duration: '20분',
        missionTitle: '토큰 예산 80% 경보 시뮬레이션과 3대 플랫폼 프롬프트 포맷 변환',
        steps: [
          '<code>ch04/context_budget.py --demo</code><br>시스템·도구·히스토리별 토큰 점유율과 압축 경고를 확인.',
          '<code>ch04/prompt_adapter.py --platform claude|chatgpt|gemini</code><br><code>prompt_template.txt</code>를 각 플랫폼 형식으로 변환해 비교.',
          '<code>tests/test_context_engineering.py</code><br>단위 테스트를 실행해 전 케이스 통과를 확인.',
        ],
        runCmd: 'python3 ch04/context_budget.py --demo\npython3 -m unittest discover -s ch04-context-engineering/tests -p "test_*.py" -v',
        answerLabel: 'ch04 모범 답안 열기 (Tree + 예산·어댑터)',
        answerType: 'Tree + Output',
        answerSummary: '컨텍스트 사용률이 임계치(예: 75%)를 넘으면 <code>context_budget.py</code>가 요약·압축 권고를 반환하며, <code>prompt_adapter.py</code>는 플랫폼별 최적 구분자(XML vs JSON Schema)를 생성합니다.',
        tree: `ch04-context-engineering/  (# ch04/ symlink)
├── prompt_template.txt         # 7항목 표준 프롬프트
├── few_shot_examples.md
├── context_budget.py           # 토큰 예산·압축 트리거
├── prompt_adapter.py           # claude / chatgpt / gemini 변환기
├── layers/ (global, root, subdir, skill)
└── tests/test_context_engineering.py`,
        codeCaption: 'context_budget.py & prompt_adapter.py 결과 예시',
        answerCode: `{
  "max_tokens": 128000,
  "used_tokens": 98400,
  "utilization_pct": 76.9,
  "compaction_recommended": true,
  "claude_format": "<role>...</role><constraints>...</constraints>",
  "chatgpt_format": "### Role\\n...\\n### Constraints\\n..."
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
        kicker: 'CH05 · HANDS-ON LAB (25분)',
        heading: '제5장 실습: <span class="hl">Agentic RAG</span> &amp; 파일 기반 지속 메모리',
        duration: '25분',
        missionTitle: '하이브리드 RRF 검색과 TASKS.md / JOURNAL.md 상태 전이 검증',
        steps: [
          '<code>ch05/memory_pattern/agentic_rag.py --query "토큰 예산 초과 시 압축 전략"</code><br>실행 후 RRF 순위 점수와 자기비평 결과를 확인.',
          '<code>ch05/memory_pattern/memory_manager.py --self-test</code><br><code>TASKS.md</code> 완료 마킹과 <code>JOURNAL.md</code> 기록을 검증.',
          '<code>tests/test_rag_and_memory.py</code><br>단위 테스트를 실행해 메모리·RAG 동작을 확인.',
        ],
        runCmd: 'python3 ch05/memory_pattern/agentic_rag.py --query "컨텍스트 오염 방지"\npython3 -m unittest discover -s ch05-rag-and-memory/memory_pattern/tests -p "test_*.py" -v',
        answerLabel: 'ch05 모범 답안 열기 (Tree + RRF 코드)',
        answerType: 'Tree + Python',
        answerSummary: '외부 벡터 DB 없이도 순수 Python 하이브리드 검색 + RRF 재순위화와 Markdown 기반 Working/Episodic 메모리를 재현합니다.',
        tree: `ch05-rag-and-memory/memory_pattern/  (# ch05/memory_pattern)
├── agentic_rag.py              # Query Rewrite + Hybrid + RRF
├── memory_manager.py           # TASKS.md / JOURNAL.md 관리
├── TASKS.md
├── JOURNAL.md
└── tests/test_rag_and_memory.py`,
        codeCaption: 'RRF(Reciprocal Rank Fusion) 결합 핵심 구현',
        answerCode: `def rrf_fuse(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for rank_list in rankings:
        for rank, doc_id in enumerate(rank_list, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)`,
      });
    },
  });
})();
