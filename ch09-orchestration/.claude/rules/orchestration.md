---
paths: ["run.py", "src/harness/**/*.py", "tests/**/*.py"]
---
# 제9장: 다중 에이전트 오케스트레이션 (3-Agent & 블라인드 합의) 조건부 규칙

- 작성자(Planner/Generator)와 평가자(Evaluator)의 도구 권한을 `permissions.py`로 엄격히 분리한다.
- 의사결정은 첫 줄(`선택: A`) 블라인드 합의로 비교하며 3회 불일치 또는 비가역 결정 시 `docs/HALT`를 생성한다.
