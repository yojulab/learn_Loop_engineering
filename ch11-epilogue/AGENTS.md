# AGENTS.md — 제11장 에필로그: 4계층 아키텍처 치트시트 & Stage 1~4 도입 진단

> 본 디렉터리(`ch11-epilogue/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `stage_readiness_check.py`(--format json|text), `README.md`(4계층 치트시트), `tests/test_stage_readiness.py`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 조직 도입 성숙도를 Stage 1(기반 구축) -> Stage 2(역할 분리) -> Stage 3(아우터 루프) -> Stage 4(LLMOps) 4단계로 진단한다.
- 모든 단계 진단과 단위 테스트는 외부 네트워크 없이 결정론적으로 동작해야 한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 stage_readiness_check.py --format json && python3 -m unittest discover -s tests -p "test_*.py"
```
