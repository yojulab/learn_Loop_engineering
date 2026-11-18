# AGENTS.md — Hermes Engineering 범용 규칙서 (목차형)

> 본 문서는 제7장 하네스 엔지니어링 원칙에 따라 **100줄 이하 목차형**으로 유지합니다.
> 상세 설계는 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) 및 각 단원 `README.md`를 참조하세요.

## 1. 저장소 지도 (Map)
- `README.md`: 4계층 12대 스택 전체 지도 및 단원 네비게이션
- `docs/ARCHITECTURE.md`: 4계층 12대 스택 모듈 경계 및 오프라인 폴백 설계서
- `CLAUDE.md`: Claude Code 전용 1층위 상시 규칙 및 컨텍스트 예산 지침
- `GEMINI.md`: Antigravity / Gemini CLI 전용 상시 규칙 및 라우팅 포인터
- `ch00-prologue/` ~ `ch12-epilogue/`: 정식 단원별 실습 코드 및 `tests/`
- `ch01/` ~ `ch11/`: 도서 본문 `💻 Git 예제` 호환 상대 심볼릭 링크 및 브릿지
- `scripts/verify_chapters.py`: Phase/단원별 통합 검증 러너

## 2. 역할 경계 & 협업 원칙
- **Maker / Checker 분리**: 구현자는 스스로 `PASS`/`FAIL`을 판정하지 않고 독립 검증(테스트·러너)에 위임한다.
- **파일 매개 협업**: 대화 이력이 아닌 코드, 테스트 결과, 문서 파일로 상태를 전달한다.
- **단원 격리 수정**: 현재 작업 단원(`chXX-*`) 및 허용된 `scripts/`, `tests/`, `docs/` 범위만 수정한다.

## 3. 5줄 핵심 가드레일
1. 파괴적 명령(`rm -rf`, `git push --force`, `git reset --hard`, `DROP TABLE`)을 실행하지 않는다.
2. 보호 브랜치(`main`, `master`, `production`)에 직접 커밋·푸시하지 않는다.
3. API 키, 토큰, 비밀번호 등 민감 정보를 코드나 문서에 하드코딩하지 않는다.
4. 모든 예제는 외부 네트워크/API 키 없이 결정론적 오프라인 폴백과 `unittest`로 검증 가능해야 한다.
5. `AGENTS.md`는 100줄 이하 목차형 구조를 유지하며, 세부 구현 규칙은 단원 문서로 위임한다.

## 4. 필수 검증 명령어
```bash
python3 ch00-prologue/stack_check.py
python3 scripts/verify_chapters.py --phase 1
python3 -m unittest discover -s tests -p "test_*.py"
```

## 5. 환경별 라우팅
- Claude Code 실행 시: `CLAUDE.md` 및 `.claude/rules/` 참조
- Gemini CLI / Antigravity 실행 시: `GEMINI.md` 참조
