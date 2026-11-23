# AGENTS.md — 하네스 엔지니어링 100줄 이하 목차형 템플릿

> 본 템플릿은 제7장의 **하네스 설계 4대 질문**을 기준으로 100줄 이하 목차형 구조를 따릅니다.

## 1. 무엇을 막을 것인가 (Guardrails)
- `guardrails.py` 5줄 핵심 차단 규칙을 위반하는 파괴적 명령 실행을 금지한다.
- `arch_linter.py`의 단방향 계층 순서(`Types -> Config -> Repo -> Service -> Runtime -> UI`)를 역행하거나 건너뛰지 않는다.

## 2. 무엇을 보여줄 것인가 (Context & Map)
- 아키텍처 계층 정의: `arch_linter.py`
- 파괴적 명령 가드레일: `guardrails.py`
- 문서 무결성 및 고아 문서 점검: `doc_gardening.py`
- 정상/위반 샘플 픽스처: `samples/valid_app/`, `samples/invalid_app/`

## 3. 어떤 도구를 줄 것인가 (Tools & Verification)
```bash
python3 arch_linter.py --root samples/valid_app
python3 doc_gardening.py --root samples/valid_app
python3 -m unittest discover -s tests -p "test_*.py"
```

## 4. 어떻게 갈아 끼울 것인가 (Replaceability)
- 모델이나 프레임워크가 바뀌어도 `Types`~`UI` 경계와 린터·테스트 계약이 동일하면 구현체 교체가 가능하다.
- 깨진 링크와 오래된 목차는 `doc_gardening.py`로 주기적으로 정리(Gardening)한다.
