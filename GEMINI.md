# GEMINI.md — Antigravity(agy CLI) 전용 상시 규칙 & 라우팅 포인터

본 파일은 Antigravity(`agy` CLI) 에이전트가 『2026 모던 AI 에이전트 스택』 실습 저장소에서 작업할 때 참조하는 진입 지침입니다.
핵심 저장소 규칙과 지도는 [AGENTS.md](AGENTS.md) 및 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)로 라우팅합니다.

## 1. 라우팅 포인터
- **전체 구조 & 단원 경계**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **공통 가드레일 & 목차형 규칙**: [AGENTS.md](AGENTS.md)
- **단원별 실행 가이드**: 각 단원 디렉터리(`ch00-prologue/` ~ `ch11-epilogue/`)의 `README.md`

## 2. 에이전트 루프 및 서브에이전트 협업 원칙
- **단일 책임 및 경계 준수**: 각 Phase/단원 작업 시 명시된 파일(`touch` 범위) 외의 파일이나 다음 Phase를 선행 수정하지 않는다.
- **오프라인 결정론적 검증**: 외부 LLM/SaaS 키 없이도 로컬 테스트(`unittest`)와 검증 스크립트가 통과해야 한다.
- **비가역 작업 금지**: `Dockerfile*`, `docker-compose*.yml` 및 보호 브랜치 직접 수정은 금지한다.

## 3. 컨테이너 실행 및 검증 명령
- 실행 대상: `graphrag_agent_app_fullstack:/apps/learn_Loop_engineering`
```bash
python3 ch00-prologue/stack_check.py --json
python3 scripts/verify_chapters.py --phase 1
python3 -m unittest discover -s tests -p "test_*.py"
```
