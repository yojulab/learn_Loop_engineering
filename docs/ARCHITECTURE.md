# ARCHITECTURE — 4계층 11대 스택 및 단원별 모듈 경계 설계서

## 1. 설계 목적 및 핵심 원칙
본 저장소는 『2026 모던 AI 에이전트 스택』의 **4계층 11대 요소**를 프롤로그(`ch00-prologue`)부터 에필로그(`ch11-epilogue`)까지 단계별 실행 가능한 코드와 자동 검증 테스트로 구현합니다.

1. **오프라인 결정론적 실행(Offline Determinism)**: Python 3.13 표준 라이브러리를 기본 런타임으로 사용하며, 외부 API 키(`OPENAI_API_KEY`, `LANGFUSE_*`)나 선택적 패키지(`pytest`, `fastapi`, `mcp`, `langfuse`)가 없어도 내장 어댑터/JSONL 폴백으로 동일하게 동작합니다.
2. **챕터 루트 일원화(Canonical Chapter Roots)**: 각 정식 단원 디렉터리(`ch00-prologue/` ~ `ch10-epilogue/`) 루트에 실체 코드와 `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`를 함께 배치합니다.
3. **단계적 모듈 경계(Phase Isolation)**: 각 Phase 및 단원은 독립된 `README.md`(표준 5단 구성)와 `tests/test_*.py`(`unittest.TestCase`)를 가지며, 하위 호환 계층은 상위 계층을 역참조하지 않습니다.

---

## 2. 4계층 11대 스택 아키텍처 매핑

| 계층 | 요소 번호 & 명칭 | 핵심 책임 | 정식 단원 경로 |
| :--- | :--- | :--- | :--- |
| **Layer 1: 지식과 컨텍스트** | 01. 프롬프트 엔지니어링 | 7항목 구조화 프롬프트, Few-shot 참조 구현 | `ch04-context-engineering/` |
| **Layer 1: 지식과 컨텍스트** | 02. 컨텍스트 엔지니어링 | 토큰 예산 배분, Lost-in-the-Middle 경고, 오염 방지 | `ch04-context-engineering/` |
| **Layer 2: 행동과 도구** | 03. 에이전트 루프 & CLI | 컨텍스트 수집-수행-검증 루프 및 파이프 비대화형 실행 | `ch01-agentic-coding/` |
| **Layer 2: 행동과 도구** | 04. MCP (Model Context Protocol) | Tools/Resource/Prompt 표준 서버 및 환경변수 확장 | `ch02-mcp-and-hooks/` |
| **Layer 2: 행동과 도구** | 05. 훅 (Hooks) | `PreToolUse` 위험 명령 차단, `PostToolUse` 감사 로그 | `ch02-mcp-and-hooks/hooks/` |
| **Layer 3: 표준과 확장** | 06. 4대 층위 상시 지침 | `CLAUDE.md`, `.claude/rules/`, `AGENTS.md`, `GEMINI.md` 계층화 | 루트 & 전 챕터 |
| **Layer 3: 표준과 확장** | 07. 스킬 (Skills) | `SKILL.md` + `reference.md` + `examples/` + 검증 스크립트 | `ch03-skills/` |
| **Layer 3: 표준과 확장** | 08. 하네스 엔지니어링 | 100줄 목차형 `AGENTS.md`, 아키텍처 린터, 가드레일, 문서 정원가꾸기 | `ch06-harness-engineering/` |
| **Layer 4: 위임과 검증** | 09. 서브에이전트 & 동적 워크플로 | 읽기 전용/실행형 에이전트 분리, 병렬 실행 및 단일 요약 병합 | `ch05-subagents-workflow/` |
| **Layer 4: 위임과 검증** | 10. 이너/아우터 루프 & 3-Agent | Ralph 서킷 브레이커, 블라인드 합의, 5단계·7대 조건 컨트롤러 | `ch07-*`, `ch08-*`, `ch09-*` |
| **Layer 4: 위임과 검증** | 11. Eval & LLMOps | 프롬프트 버전 라벨, 3종 Eval, Trace/회귀 비교, Stage 1~4 진단 | `ch10-*`, `ch11-epilogue/` |

---

## 3. Phase별 경계 및 통합 검증 체계

- **Phase 1 (루트 & 프롤로그)**: 루트 4종 문서(`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`), `docs/ARCHITECTURE.md`, 통합 러너(`scripts/verify_chapters.py`), 루트 무결성 테스트(`tests/test_repo_root.py`), `ch00-prologue/` 진단 도구(`stack_check.py`).
- **Phase 2 (Part 1: 제1~3장)**: 도구와 표준 인터페이스(`ch01`~`ch03`).
- **Phase 3 (Part 2: 제4장)**: 컨텍스트 예산, 7항목 프롬프트, 4대 층위 지침(`ch04`).
- **Phase 4 (Part 3: 제5~7장)**: 서브에이전트 병렬 워크플로, 하네스 린터/정원가꾸기, SQLite FTS5 기반 이너 랄프 루프(`ch05`~`ch07`).
- **Phase 5 (Part 4 & 에필로그: 제8~11장)**: 3-Agent 오케스트레이션, 5단계 아우터 루프, Eval/LLMOps 회귀 비교, Stage 1~4 도입 성숙도 진단(`ch08`~`ch11`).

모든 검증은 `python3 scripts/verify_chapters.py --phase <N>` 또는 `--all`로 통합 실행되며, `pytest`가 미설치된 환경에서도 자동으로 `python3 -m unittest`로 폴백하여 동일한 검증 계약을 강제합니다.
