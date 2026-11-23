# AGENTS.md — 제1장: 바이브 코딩과 에이전틱 코딩의 탄생 (Quote CLI)

> 본 디렉터리(`ch01-agentic-coding/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `quotes.json`(명언 데이터), `quote_cli.py`(--all/--tag/--seed/--json), `interactive_demo.py`(3단계 루프), `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 모든 작업은 컨텍스트 수집(Gather) -> CLI 실행(Execute) -> 테스트 검증(Verify) 3단계 폐쇄 루프로 수행한다.
- CLI 출력은 비대화형 파이프(`--json`)와 결정론적 시드(`--seed`)를 지원해야 한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 quote_cli.py --tag engineering --json && python3 quote_cli.py --seed 42 --json && python3 -m unittest discover -s tests -p "test_*.py"
```
