# 혼자서 프로젝트 5개 돌리는 개발자의 비밀: 루프 엔지니어링

> **프롬프트 노가다는 끝났다 — 1인 멀티 프로젝트를 자동화하는 AI 설계·관측·개선 루프의 모든 것**
>
> 🔗 **웹 PPT 바로가기**: [https://yojulab.github.io/learn_Loop_engineering/](https://yojulab.github.io/learn_Loop_engineering/)  
> ([프롤로그 PPT](https://yojulab.github.io/learn_Loop_engineering/prologue.html) · [메인 5시간 강의 PPT](https://yojulab.github.io/learn_Loop_engineering/lecture.html) · [카툰 심화 워크숍 PPT](https://yojulab.github.io/learn_Loop_engineering/workshop.html))

감으로 프롬프트만 고치다 실패하는 패턴을 깨고, **배포(Launch) · 관측(Observe) · 평가(Evaluate) · 개선(Improve)** 의 데이터 기반 루프로 전환하여 1인이 멀티 프로젝트를 자동화하는 실전 아키텍처와 전 단원(`ch00`~`ch12`) 실습 코드를 제공합니다.

## 1. 단원 학습 목표 & 12대 스택 4계층 맵

- **학습 목표 1**: 감에 의존하는 프롬프팅을 넘어 **배포(Launch)·관측(Observe)·평가(Evaluate)·개선(Improve)** 루프와 이를 뒷받침하는 **4계층 12대 요소**의 책임을 이해한다.
- **학습 목표 2**: 프롬프트·컨텍스트·RAG·메모리(1계층), 에이전트 루프·MCP·훅(2계층), 지침 파일·스킬·하네스(3계층), 서브에이전트·오케스트레이션·Eval/LLMOps(4계층)를 실행 가능한 코드로 검증한다.
- **학습 목표 3**: 각 챕터 폴더(`ch00-prologue/` ~ `ch12-epilogue/`)로 이동한 뒤 AI CLI(`claude` / `agy` / `codex`)에 접속해 **사용자 입력 프롬프트**로 실습을 수행한다.
- **학습 목표 4**: 도서 본문 내 `💻 Git 예제` 경로(`ch01/`~`ch11/`)와 정식 단원 루트 디렉터리(`ch00-prologue/`~`ch12-epilogue/`)를 동일한 인터페이스로 탐색한다.

| 계층 (Layer) | 핵심 역할 | 12대 스택 요소 | 매핑 단원 |
| :--- | :--- | :--- | :--- |
| **Layer 1. 지식과 기억** | 모델이 무엇을 알고 판단하는가 | ① 프롬프트 & 컨텍스트, ② Agentic RAG, ③ 지속 Memory | `ch04`, `ch05` |
| **Layer 2. 행동과 도구** | 모델이 외부 세계와 어떻게 상호작용하는가 | ④ 에이전트 루프, ⑤ MCP, ⑥ 훅(Hooks) | `ch01`, `ch02` |
| **Layer 3. 표준과 확장** | 팀 규칙과 전문 노하우를 어떻게 재사용하는가 | ⑦ 상시 지침(`AGENTS.md`/`CLAUDE.md`/`GEMINI.md`), ⑧ 스킬(Skills), ⑨ 하네스 엔지니어링 | `ch03`, `ch04`, `ch07` |
| **Layer 4. 위임과 검증** | 복수 에이전트가 어떻게 장기 작업을 완주하고 검증받는가 | ⑩ 서브에이전트, ⑪ 이너·아우터 루프 & 오케스트레이션, ⑫ Eval & LLMOps | `ch06`, `ch08`, `ch09`, `ch10`, `ch11` |

## 2. 아키텍처 다이어그램 (Mermaid)

```mermaid
flowchart TB
    L0["ch00-prologue: 4계층 12대 스택 진단 (stack_check.py)"]
    subgraph L1["Layer 1: 지식과 기억"]
        E1["1. 프롬프트 & 컨텍스트 (ch04)"]
        E2["2. Agentic RAG (ch05)"]
        E3["3. 지속 Memory (ch05)"]
    end
    subgraph L2["Layer 2: 행동과 도구"]
        E4["4. 에이전트 루프 (ch01)"]
        E5["5. MCP 서버 (ch02)"]
        E6["6. Hooks 가드레일 (ch02)"]
    end
    subgraph L3["Layer 3: 표준과 확장"]
        E7["7. 상시 지침 AGENTS/CLAUDE/GEMINI (전 챕터)"]
        E8["8. 온디맨드 Skills (ch03)"]
        E9["9. 하네스 린터/정원가꾸기 (ch07)"]
    end
    subgraph L4["Layer 4: 위임과 검증"]
        E10["10. 서브에이전트 & 워크플로 (ch06)"]
        E11["11. 이너/아우터 루프 & 3-Agent 오케스트레이션 (ch08~ch10)"]
        E12["12. Eval & LLMOps (ch11)"]
    end
    L12["ch12-epilogue: Stage 1~4 도입 진단 (stage_readiness_check.py)"]

    L0 --> L1 --> L2 --> L3 --> L4 --> L12
```

## 3. 디렉터리 및 소스 파일 구조 (전 챕터 AI 지침·폴더 표준화)

모든 챕터(`ch00-prologue/` ~ `ch12-epilogue/`) 루트에는 해당 단원에 맞춘 **`AGENTS.md`**, **`CLAUDE.md`**, **`GEMINI.md`** 와 관련 AI 폴더(**`.claude/`**, **`.gemini/`**)가 기본 구성되어 있어, 해당 챕터 폴더로 이동 후 AI CLI에 접속하면 지침이 즉시 반영됩니다.

| 단원 루트 경로 | 도서 호환 경로 (`💻 Git 예제`) | 핵심 내용 | 상태 |
| :--- | :--- | :--- | :--- |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHATGPT.md`, `GEMINI.md`, `platforms/`, `docs/ARCHITECTURE.md` | 루트 | 범용 규칙서, 에이전트별 포인터, 4계층 설계서 | Phase 1 |
| `scripts/verify_chapters.py`, `tests/test_repo_root.py` | 루트 | 전 단원 통합 검증 러너 및 루트 무결성 테스트 | Phase 1 |
| `ch00-prologue/` | `ch00-prologue/` | `stack_check.py` (4계층 12대 스택 진단), `agent_check.py` (로컬 AI & 플랫폼 확인) | Phase 1 |
| `ch01-agentic-coding/` | `ch01/quote-cli/` | `quote_cli.py`, `interactive_demo.py`, `quotes.json` | Phase 2 |
| `ch02-mcp-and-hooks/` | `ch02/quote-mcp/`, `ch04/quote-cli/` *(제2장 오타 호환)* | MCP 명언 서버(`main.py`) + `.mcp.json` + `.claude/settings.json` 훅(`hooks/`) | Phase 2 |
| `ch03-skills/` | `ch03/github-workflow-skills/` | 3단계 확장형 GitHub 워크플로 스킬 5종 (`git-commit`, `gh-issue`, `gh-pr`, `gh-review`, `gh-address-review`) | Phase 2 |
| `ch04-context-engineering/` | `ch04/` (`prompt_template.txt` 등) | 7항목 프롬프트, Few-shot, 4대 층위 지침, `context_budget.py` | Phase 3 |
| `ch05-rag-and-memory/` | `ch05/memory_pattern/` | `memory_manager.py`, `agentic_rag.py`, `TASKS.md`/`JOURNAL.md`, `corpus/` | Phase 3 |
| `ch06-subagents-workflow/` | `ch06/quote-cli/` | `.claude/agents/` 5종, 검색 확장 `quote_cli.py`, `dynamic_workflow.py` | Phase 4 |
| `ch07-harness-engineering/` | `ch07/harness-templates/` | 100줄 `AGENTS.md`, `arch_linter.py`, `guardrails.py`, `doc_gardening.py` | Phase 4 |
| `ch08-inner-ralph-loop/` | `ch08/rss-wiki/` | FTS5 `db.py`, `collector.py`, `app.py`, `ralph_loop.sh`, `goal_evaluator.py` | Phase 4 |
| `ch09-orchestration/` | `ch09/harness/` | 3-Agent 오케스트레이션(`run.py`, `src/harness/`), 블라인드 합의, 0~3점 채점표 | Phase 5 |
| `ch10-outer-loop/` | `ch10/todo-loop/` | 5단계 아우터 루프(`loop.py`), 7대 완료·중단 조건, `CALC-001`~`004` | Phase 5 |
| `ch11-eval-and-llmops/` | `ch11/support-assistant/` | `litellm_proxy/`, `trace_to_prompt.py`, `fetch_prompt.py`, 3종 Eval, `regression_compare.py` | Phase 5 |
| `ch12-epilogue/` | `ch12-epilogue/` | 4계층 치트시트, `stage_readiness_check.py` | Phase 5 |

## 4. 실습 방식 & 사용자 입력 프롬프트 예시 (AI CLI)

### 4.1 표준 실습 절차 (해당 챕터 폴더 이동 후 AI CLI 접속)

```bash
# 1) 실습할 챕터 루트 폴더로 이동 (예: ch02-mcp-and-hooks)
cd ch02-mcp-and-hooks

# 2) AI CLI 접속 (현재 챕터의 AGENTS.md / CLAUDE.md / GEMINI.md 및 .claude/ · .gemini/ 자동 인식)
claude   # 또는 agy / codex
```

### 4.2 사용자 입력 프롬프트 예시 (3개 이상)

- **프롬프트 예시 1 (챕터별 지침 확인 및 핵심 실습 실행)**:
  > "현재 챕터 폴더의 `AGENTS.md`(또는 `CLAUDE.md`/`GEMINI.md`)와 `README.md`를 읽고, 본 단원의 핵심 스크립트를 실행해 JSON 결과와 동작 요약을 출력해줘."

- **프롬프트 예시 2 (단원별 단위 테스트 검증 및 자가 수정 루프)**:
  > "현재 챕터의 `tests/` 단위 테스트(`python3 -m unittest discover -s tests -p 'test_*.py' -v`)를 실행해 모든 테스트가 통과하는지 확인하고 결과를 요약해줘."

- **프롬프트 예시 3 (전체 저장소 Stage 1~4 성숙도 진단 및 통합 게이트 실행)**:
  > "`python3 ch12-epilogue/stage_readiness_check.py --format json`과 `python3 scripts/verify_chapters.py --all`을 실행해 Stage 1~4 준비 상태와 전 단원 통합 검증 결과를 보고해줘."

### 4.3 참고용 컨테이너 실행 & 테스트 명령어

```bash
# 프롤로그 4계층 12대 스택 진단
python3 ch00-prologue/stack_check.py --json
python3 ch00-prologue/agent_check.py --platform gemini --prompt "에이전트 런타임 확인"

# 전 단원 통합 검증
python3 scripts/verify_chapters.py --all
```

### Docker Compose 실습 환경 (`dockers/`)

- **구성**: Langfuse(`http://localhost:30000`) + PostgreSQL + LiteLLM Proxy(`http://localhost:4000`) + 앱 컨테이너(Python 3.13 · Claude Code CLI · Antigravity CLI `agy` · langfuse SDK)
- **설정**: 볼륨 경로·계정·API 키는 `dockers/.env`에서 설정 (`cp dockers/.env.example dockers/.env`)
- **실행**: `cd dockers && docker compose up -d --build && docker compose exec app bash` (자세한 내용: [`dockers/README.md`](dockers/README.md))

#### Langfuse 대시보드 초기 데이터 적재 (`seed_langfuse_dashboard.py --json`)

```bash
# 기본값으로 적재 (24시간 간격 × 시간당 3회 = 72건, 3대 모델, '고객지원 및 장애 트리아지')
python3 ch11-eval-and-llmops/seed_langfuse_dashboard.py --json
```

### Any-Platform 실행 지원 (Claude · ChatGPT · Gemini)

| 플랫폼 | 진입 지침 파일 | 어댑터 & 단원별 호환 파일 (`*_[플랫폼].*`) | 비대화형 실행 예시 |
| :--- | :--- | :--- | :--- |
| **Claude** | `CLAUDE.md` (`.claude/`) | `platforms/adapter_claude.py`, `*_claude.*` | `AGENT_PLATFORM=claude python3 ch10-outer-loop/loop.py --platform claude` |
| **ChatGPT / Codex** | `AGENTS.md`, `CHATGPT.md` | `platforms/adapter_chatgpt.py`, `*_chatgpt.*` | `AGENT_PLATFORM=chatgpt python3 ch10-outer-loop/loop.py --platform chatgpt` |
| **Gemini / Antigravity** | `GEMINI.md` (`.gemini/`) | `platforms/adapter_gemini.py`, `*_gemini.*` | `AGENT_PLATFORM=gemini python3 ch10-outer-loop/loop.py --platform gemini` |

### Web PPT (GitHub Pages: `docs/`)

- **배포 URL**: [https://yojulab.github.io/learn_Loop_engineering/](https://yojulab.github.io/learn_Loop_engineering/)
- **분기 덱**: [`docs/index.html`](docs/index.html) (Home) · [`docs/prologue.html`](docs/prologue.html) (프롤로그 4장) · [`docs/lecture.html`](docs/lecture.html) (5시간 메인 39장) · [`docs/workshop.html`](docs/workshop.html) (카툰 워크숍 39장) · [`docs/presenter.html`](docs/presenter.html) (발표자 창)
- **구성**: `ch00`~`ch12` 전 단원 이론 슬라이드 + **단원별 실습 미션(AI CLI 사용자 입력 프롬프트 예시 3선 포함)과 클릭 토글(`<details>`) 모범 답안 & 해결 프롬프트 한 페이지 배치**

## 5. 핵심 체크리스트

- [ ] 루트 및 전 챕터(`ch00-prologue/` ~ `ch12-epilogue/`)에 `AGENTS.md`(100줄 이하), `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.gemini/`가 구성되어 있는가?
- [ ] 모든 단원 `README.md`가 표준 5단 템플릿과 **사용자 입력 프롬프트 예시 3개 이상**을 포함하는가?
- [ ] 외부 네트워크/API 키 없이 `unittest` 및 `scripts/verify_chapters.py --all`이 결정론적으로 통과하는가?
- [ ] 도서 본문 내 `💻 Git 예제` 호환 경로(`ch01/`~`ch11/`, `ch04/quote-cli/`)가 깨짐 없이 연결되는가?
