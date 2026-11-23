---
paths: ["arch_linter.py", "guardrails.py", "doc_gardening.py", "samples/**/*.py"]
---
# 제7장: 모델을 감싸는 안전장치 — 하네스 엔지니어링 조건부 규칙

- 아키텍처 단방향 의존성(`Types -> Config -> Repo -> Service -> Runtime -> UI`) 위반 시 즉시 구체적인 수정 가이드를 출력한다.
- `AGENTS.md`는 항상 100줄 이하 목차형으로 유지하고 `doc_gardening.py`로 고아 문서와 깨진 링크를 차단한다.
