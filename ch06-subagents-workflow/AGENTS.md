# AGENTS.md — 제6장: 서브에이전트와 동적 병렬 워크플로

> 본 디렉터리(`ch06-subagents-workflow/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `.claude/agents/*.md`(5종 전문 서브에이전트), `dynamic_workflow.py`(동적 선택·병렬 실행), `quote_cli.py`(--search/--author 확장), `agents_chatgpt.json`, `agents_gemini.json`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 감사·리뷰 역할(`api-reviewer`, `security-scanner`, `code-quality`)은 읽기 전용 도구(`Read`, `Grep`, `Glob`)만 허용한다.
- 각 서브에이전트는 격리된 컨텍스트에서 병렬 실행된 뒤 단일 요약 리포트로 병합되어야 한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 dynamic_workflow.py --task-type api_change --json && python3 quote_cli.py --search "harness" --json && python3 -m unittest discover -s tests -p "test_*.py"
```
