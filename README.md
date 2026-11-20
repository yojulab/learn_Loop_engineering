# Loop Engineering — 『2026 모던 AI 에이전트 스택』 전 단원 실습 저장소

## 1. 단원 학습 목표 & 12대 스택 4계층 맵

- **학습 목표 1**: LLM을 감싸는 **4계층 12대 요소**의 구조와 각 계층 간 책임을 한눈에 이해한다.
- **학습 목표 2**: 프롬프트·컨텍스트·RAG·메모리(1계층), 에이전트 루프·MCP·훅(2계층), 지침 파일·스킬·하네스(3계층), 서브에이전트·오케스트레이션·Eval/LLMOps(4계층)를 실행 가능한 코드로 검증한다.
- **학습 목표 3**: 외부 API 키나 네트워크 없이도 컨테이너 내부에서 결정론적 오프라인 테스트와 CLI 실습을 재현한다.
- **학습 목표 4**: 도서 본문 내 `💻 Git 예제` 경로(`ch01/`~`ch11/`)와 정식 단원 디렉터리(`ch00-prologue/`~`ch12-epilogue/`)를 동일한 인터페이스로 탐색한다.

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
        E7["7. 상시 지침 AGENTS/CLAUDE/GEMINI (ch04, root)"]
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

## 3. 디렉터리 및 소스 파일 구조

| 단원 / 경로 | 도서 호환 경로 (`💻 Git 예제`) | 핵심 내용 | 상태 |
| :--- | :--- | :--- | :--- |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHATGPT.md`, `GEMINI.md`, `platforms/`, `docs/ARCHITECTURE.md` | 루트 | 범용 규칙서, 에이전트별 포인터, 4계층 설계서 | Phase 1 |
| `scripts/verify_chapters.py`, `tests/test_repo_root.py` | 루트 | 전 단원 통합 검증 러너 및 루트 무결성 테스트 | Phase 1 |
| `ch00-prologue/` | `ch00-prologue/` | `stack_check.py` (4계층 12대 스택 진단), `agent_check.py` (로컬 AI & 플랫폼 확인) | Phase 1 |
| `ch01-agentic-coding/quote-cli/` | `ch01/quote-cli/` | `quote_cli.py`, `interactive_demo.py`, `quotes.json` | Phase 2 |
| `ch02-mcp-and-hooks/quote-mcp/` | `ch02/quote-mcp/`, `ch04/quote-cli/` *(제2장 오타 호환)* | MCP 명언 서버 + PreToolUse/PostToolUse 훅 | Phase 2 |
| `ch03-skills/github-workflow-skills/` | `ch03/github-workflow-skills/` | 3단계 확장형 GitHub 워크플로 스킬 5종 | Phase 2 |
| `ch04-context-engineering/` | `ch04/` (`prompt_template.txt` 등) | 7항목 프롬프트, Few-shot, 4대 층위 지침, `context_budget.py` | Phase 3 |
| `ch05-rag-and-memory/memory_pattern/` | `ch05/memory_pattern/` | `memory_manager.py`, `agentic_rag.py`, `TASKS.md`/`JOURNAL.md` | Phase 3 |
| `ch06-subagents-workflow/` | `ch06/quote-cli/` | `.claude/agents/` 5종, 검색 확장 CLI, `dynamic_workflow.py` | Phase 4 |
| `ch07-harness-engineering/harness-templates/` | `ch07/harness-templates/` | 100줄 `AGENTS.md`, `arch_linter.py`, `guardrails.py`, `doc_gardening.py` | Phase 4 |
| `ch08-inner-ralph-loop/rss-wiki/` | `ch08/rss-wiki/` | FTS5 `db.py`, `collector.py`, `app.py`, `ralph_loop.sh`, `goal_evaluator.py` | Phase 4 |
| `ch09-orchestration/harness/` | `ch09/harness/` | 3-Agent 오케스트레이션, 블라인드 합의, 0~3점 채점표 | Phase 5 |
| `ch10-outer-loop/todo-loop/` | `ch10/todo-loop/` | 5단계 아우터 루프, 7대 완료·중단 조건, `CALC-001`~`004` | Phase 5 |
| `ch11-eval-and-llmops/support-assistant/` | `ch11/support-assistant/` | `seed_prompts.py`, `prompting.py`, 3종 Eval, JSONL 폴백, 회귀 비교기 | Phase 5 |
| `ch12-epilogue/` | `ch12-epilogue/` | 4계층 치트시트, `stage_readiness_check.py` | Phase 5 |

## 4. 컨테이너 실행 & 테스트 명령어

컨테이너 작업 디렉터리: `graphrag_agent_app_fullstack:/apps/learn_Loop_engineering`

```bash
# 프롤로그 4계층 12대 스택 진단
python3 ch00-prologue/stack_check.py
python3 ch00-prologue/stack_check.py --json

# 로컬 AI 동작 및 Agent Platform 확인 (간략 문장 응답)
python3 ch00-prologue/agent_check.py
python3 ch00-prologue/agent_check.py --platform gemini --prompt "에이전트 런타임 확인"
AGENT_PLATFORM=gemini python3 ch00-prologue/agent_check.py --json

# Phase 1 통합 검증 (루트 문서, 가드레일, ch00-prologue)
python3 scripts/verify_chapters.py --phase 1
python3 scripts/verify_chapters.py --phase 1 --json

# 단위 테스트 직접 실행
python3 -m unittest discover -s tests -p "test_*.py"
python3 -m unittest discover -s ch00-prologue/tests -p "test_*.py"

# 전 단원 통합 검증 (전체 Phase 구현 완료 시)
python3 scripts/verify_chapters.py --all
```

### Docker Compose 실습 환경 (`dockers/`)

- **구성**: Langfuse + PostgreSQL + 앱 컨테이너(Python 3.13 · Claude Code CLI · langfuse SDK), 호스트 포트 미게시
- **설정**: 볼륨 경로·계정·API 키는 `dockers/.env`에서 설정 (`cp dockers/.env.example dockers/.env`)
- **실행**: `cd dockers && docker compose up -d --build && docker compose exec app bash` (자세한 내용: [`dockers/README.md`](dockers/README.md))

### Any-Platform 실행 지원 (Claude · ChatGPT · Gemini)

| 플랫폼 | 진입 지침 파일 | 어댑터 & 단원별 호환 파일 (`*_[플랫폼].*`) | 비대화형 실행 예시 |
| :--- | :--- | :--- | :--- |
| **Claude** | `CLAUDE.md` | `platforms/adapter_claude.py`, `*_claude.*` | `AGENT_PLATFORM=claude python3 ch10/todo-loop/loop.py --platform claude` |
| **ChatGPT / Codex** | `AGENTS.md`, `CHATGPT.md` | `platforms/adapter_chatgpt.py`, `*_chatgpt.*` | `AGENT_PLATFORM=chatgpt python3 ch10/todo-loop/loop.py --platform chatgpt` |
| **Gemini / Antigravity** | `GEMINI.md` | `platforms/adapter_gemini.py`, `*_gemini.*` | `AGENT_PLATFORM=gemini python3 ch10/todo-loop/loop.py --platform gemini` |

### 5시간 과정 Web PPT (GitHub Pages: `docs/`)

- **경로**: [`docs/index.html`](docs/index.html) (발표자 대시보드: [`docs/presenter.html`](docs/presenter.html))
- **최종 목적 아키텍처**: `LangGraph`(상태 기반 에이전트 오케스트레이션) + `LiteLLM Proxy` + `Langfuse`(Trace 모니터링 · Eval · Save as Prompt 버전 개선 루프)
- **구성**: `ch00`~`ch12` 전 단원(총 300분) 이론 슬라이드 + **단원별 실습 미션과 클릭 토글(`<details>`) 모범 답안(Tree + 코드/CLI) 한 페이지 배치**
- **GitHub Pages 배포**: 저장소 `Settings → Pages → Source`에서 `main` 또는 `develop` 브랜치의 `/docs` 폴더 선택 (`.nojekyll` 포함, 100% 상대 경로)
- **로컬 미리보기**: `python3 -m http.server 8080 --directory docs` 후 브라우저에서 `http://localhost:8080` 접속 (단축키 `A`: 모범답안 토글, `O`: 목차, `P`: 발표자 창, `F`: 전체 화면, `?print`: PDF 인쇄)

## 5. 핵심 체크리스트

- [ ] `AGENTS.md`는 제7장 원칙에 따라 100줄 이하 목차형 규칙서로 유지되는가?
- [ ] 모든 단원(`ch00-prologue/` ~ `ch12-epilogue/`)이 표준 5단 `README.md` 템플릿을 준수하는가?
- [ ] 외부 네트워크/API 키 없이 `unittest` 및 `scripts/verify_chapters.py`가 결정론적으로 통과하는가?
- [ ] 도서 본문 내 `💻 Git 예제` 호환 경로(`ch01/`~`ch11/`, `ch04/quote-cli/`)가 깨짐 없이 연결되는가?
