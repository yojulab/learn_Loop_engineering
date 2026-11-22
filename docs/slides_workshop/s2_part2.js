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
        userPrompt: `[7항목 프롬프트 & 컨텍스트 예산 모범 답안 재현 프롬프트]
7항목 구조화 프롬프트 템플릿과 4대 지침 층위, 컨텍스트 예산 분석기(context_budget.py) 및 단위 테스트를 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - prompt_template.txt (Role, Goal, Context, Constraints, Few-shot, Format, Self-Check 7항목 템플릿)
   - few_shot_reference.txt
   - claude_working_guidelines.md
   - guidelines_claude.md , guidelines_chatgpt.md , guidelines_gemini.md
   - AGENTS.md , CLAUDE.md , GEMINI.md , .claude/rules/api.md
   - context_budget.py
   - tests/test_context_engineering.py

2. 핵심 구현 명세 (context_budget.py)
   - BudgetAllocation dataclass(system, instructions, tools, history, output, max_window, total_tokens, utilization, status, lost_in_the_middle_risk, recommendations)
   - estimate_tokens(text): max(1, (len(stripped) + 3) // 4) 근사 토큰 계산
   - evaluate_budget(system, instructions, tools, history, output, max_window=200_000, warn_ratio=0.75):
     * utilization >= 0.90 이면 status="CRITICAL" + /clear 권고
     * utilization >= warn_ratio 이면 status="WARN" + /compact 권고, 그 외 "OK"
     * utilization >= 0.65 또는 history/max_window >= 0.50 이면 lost_in_the_middle_risk=True
     * tools/max_window >= 0.30 이면 Top-K & 발췌 필터링 권고 추가
   - format_budget_report(alloc, as_json=False) 및 --json CLI 출력

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 context_budget.py --json
   - python3 -m unittest discover -s tests -p "test_*.py" -v`,
        kicker: 'CH04 · HANDS-ON LAB',
        heading: '제4장 실습: <span class="hv">컨텍스트 예산</span> 계산 &amp; 프롬프트 어댑팅',
        duration: '',
        missionTitle: '토큰 예산 80% 경보 시뮬레이션과 3대 플랫폼 프롬프트 포맷 변환',
        steps: [
          '<code>context_budget.py --json</code><br>시스템·도구·히스토리별 토큰 점유율과 압축 권고 경고를 확인.',
          '<code>prompt_template.txt</code> · <code>few_shot_reference.txt</code><br>7항목 프롬프트와 Few-shot 예시, 플랫폼별 <code>guidelines_*.md</code>를 비교.',
          '<code>tests/test_context_engineering.py</code><br>단위 테스트를 실행해 전 케이스 통과를 확인.',
        ],
        runCmd: 'python3 context_budget.py --json\npython3 -m unittest discover -s tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + 예산 JSON)',
        answerType: 'Tree + JSON',
        answerSummary: '<code>context_budget.py --json</code>은 시스템·지침·도구·히스토리별 토큰 비중과 압축 필요 여부를 계산하며, 4대 층위(<code>AGENTS.md</code>·<code>CLAUDE.md</code>·<code>GEMINI.md</code>·<code>.claude/rules/</code>)가 분리되어 있습니다.',
        tree: `project/
├── prompt_template.txt
├── few_shot_reference.txt
├── claude_working_guidelines.md
├── context_budget.py           # 토큰 예산·압축 분석기
├── guidelines_claude.md · guidelines_chatgpt.md · guidelines_gemini.md
├── AGENTS.md · CLAUDE.md · GEMINI.md · .claude/rules/api.md
└── tests/test_context_engineering.py`,
        codeCaption: 'context_budget.py --json 핵심 출력 예시',
        answerCode: `{
  "system": 4000,
  "instructions": 3000,
  "tools": 18000,
  "history": 65000,
  "output": 8000,
  "utilization_pct": 76.56,
  "compaction_needed": true
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
        userPrompt: `[Agentic RAG & 지속 메모리 모범 답안 재현 프롬프트]
외부 벡터 DB 없이 순수 Python만으로 Top-K·발췌 필터링 Agentic RAG와 파일 기반 지속 메모리(TASKS.md/JOURNAL.md) 모범 답안을 아래 명세에 맞게 구현하고 검증해줘.

1. 생성할 파일 구조
   - memory_pattern/agentic_rag.py
   - memory_pattern/memory_manager.py
   - memory_pattern/corpus/ 하위에 4종 샘플 마크다운 문서(01~04) 생성
   - memory_pattern/TASKS.md , JOURNAL.md
   - memory_pattern/tests/test_memory_pattern.py

2. 핵심 구현 명세
   - agentic_rag.py: DocumentChunk(source, title, excerpt, score, matched_terms) dataclass와 AgenticRetriever(corpus_dir) 구현. search(query, top_k=3, max_chars_per_excerpt=240) 메서드는 한·영 토큰화(_tokenize) 후 코퍼스 .md 파일을 스캔해 _extract_best_excerpt()로 핵심 문장만 max_chars_per_excerpt 이내로 잘라 상위 top_k건을 점수 내림차순(-score, source)으로 반환할 것.
   - memory_manager.py: TaskItem(task_id, title, status, note) dataclass와 MemoryManager(tasks_path, journal_path) 구현. '- [ ] **ID**: 제목' / '[x]' / '[!]' 정규식 파싱(parse_tasks), next_pending_task(), mark_task_done(), mark_task_blocked('[BLOCKED] ...'), append_journal(actor, decision, evidence) 제공.

3. 검증 명령 (전부 exit 0 통과 필수)
   - python3 memory_pattern/agentic_rag.py
   - python3 -m unittest discover -s memory_pattern/tests -p "test_*.py" -v`,
        kicker: 'CH05 · HANDS-ON LAB',
        heading: '제5장 실습: <span class="hl">Agentic RAG</span> &amp; 파일 기반 지속 메모리',
        duration: '',
        missionTitle: '하이브리드 RRF 검색과 TASKS.md / JOURNAL.md 상태 전이 검증',
        steps: [
          '<code>memory_pattern/agentic_rag.py</code><br>실행 후 <code>corpus/</code> 문서 대상 하이브리드 검색과 RRF 순위 점수를 확인.',
          '<code>memory_pattern/memory_manager.py</code><br><code>TASKS.md</code> 작업 상태와 <code>JOURNAL.md</code> 기록 관리 동작을 검증.',
          '<code>tests/test_memory_pattern.py</code><br>단위 테스트를 실행해 메모리·RAG 동작을 확인.',
        ],
        runCmd: 'python3 memory_pattern/agentic_rag.py\npython3 -m unittest discover -s memory_pattern/tests -p "test_*.py" -v',
        answerLabel: '모범 답안 열기 (Tree + RRF 코드)',
        answerType: 'Tree + Python',
        answerSummary: '외부 벡터 DB 없이도 <code>corpus/</code> 4종 문서를 대상으로 순수 Python 하이브리드 검색 + RRF 재순위화와 Markdown 기반 Working/Episodic 메모리를 재현합니다.',
        tree: `memory_pattern/
├── agentic_rag.py              # Query Rewrite + Hybrid + RRF
├── memory_manager.py           # TASKS.md / JOURNAL.md 관리
├── corpus/ (01~04_*.md)
├── TASKS.md · JOURNAL.md
└── tests/test_memory_pattern.py`,
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
