# CLAUDE.md — Claude Code 전용 상시 규칙 (1층위)

본 파일은 『2026 모던 AI 에이전트 스택』 실습 저장소에서 Claude Code가 항상 준수하는 **1층위 상시 지침**입니다.
공통 저장소 지도와 5줄 핵심 가드레일은 [AGENTS.md](AGENTS.md)를 따릅니다.

## 1. 4계층 지침 우선순위 (제4장 원칙)
1. **1층위 (`CLAUDE.md`)**: 저장소 전역 상시 규칙, 테스트 명령, 금지 패턴
2. **2층위 (`.claude/rules/*.md`)**: `paths:` frontmatter 기반 특정 경로 조건부 규칙 (예: `ch04-context-engineering/.claude/rules/api.md`)
3. **3층위 (`AGENTS.md`)**: 도구 중립적 공용 목차형 규약 (100줄 이하)
4. **4층위 (`SKILL.md`)**: 필요 시에만 로드하는 온디맨드 전문 스킬 (예: `ch03-skills/`)

## 2. 컨텍스트 윈도우 및 오염 방지 원칙
- 작업 시작 전 관련 단원의 `README.md`와 테스트 파일만 최소 범위로 읽는다.
- 긴 로그·전체 파일 덤프를 피하고 핵심 발췌(Excerpt)만 유지한다.
- 컨텍스트 점유율이 임계치(75%)를 넘거나 작업 주제가 전환되면 `/compact` 또는 `/clear`로 세션을 정리한다.
- 대화 메모리에 의존하지 말고 상태와 검증 결과는 코드·테스트로 남긴다.

## 3. 도구·훅(Hooks) 및 가드레일
- `PreToolUse` / `PostToolUse` 훅 예시(`ch02-mcp-and-hooks/.claude/settings.json`)의 보안 정책을 준수한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`)을 절대 실행하지 않는다.
- 모든 Python 구현은 컨테이너(`graphrag_agent_app_fullstack:/apps/learn_Loop_engineering`) 내 `Python 3.13` 표준 라이브러리 우선으로 작성하며, 미설치 서드파티 패키지에 대해 오프라인 폴백을 제공한다.

## 4. 표준 검증 명령어
```bash
python3 scripts/verify_chapters.py --phase 1
python3 -m unittest discover -s tests -p "test_*.py"
```
