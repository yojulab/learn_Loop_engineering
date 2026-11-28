# AGENTS.md — 프롤로그: 4계층 11대 스택 & Any-Platform 환경 진단

> 본 디렉터리(`ch00-prologue/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `stack_check.py`(4계층 11대 스택 진단), `agent_check.py`(플랫폼 어댑터 점검), `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 4계층(Layer 1~4)과 11대 요소 메타데이터가 누락 없이 유지되어야 한다.
- 외부 API 키가 없어도 `AGENT_PLATFORM=offline` 폴백으로 항상 종료 코드 0과 유효한 JSON을 반환한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 stack_check.py --json && AGENT_PLATFORM=offline python3 agent_check.py --json && python3 -m unittest discover -s tests -p "test_*.py"
```
