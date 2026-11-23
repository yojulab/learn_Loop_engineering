# AGENTS.md — 제4장: 컨텍스트 엔지니어링과 윈도우의 한계

> 본 디렉터리(`ch04-context-engineering/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `prompt_template.txt`(7항목), `few_shot_reference.txt`(참조 구현), `context_budget.py`(토큰 예산 진단), `.claude/rules/api.md`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 7항목 프롬프트 구조(`[목표]`, `[맥락]`, `[참고 패턴]`, `[제약과 범위]`, `[도구/절차]`, `[완료 기준]`, `[보고 형식]`)를 준수한다.
- 컨텍스트 점유율 75% 초과 시 `/compact` 또는 `/clear`를 권고한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 context_budget.py --json && python3 -m unittest discover -s tests -p "test_*.py"
```
