---
paths: ["stack_check.py", "agent_check.py", "tests/**/*.py"]
---
# 프롤로그: 4계층 11대 스택 & Any-Platform 환경 진단 조건부 규칙

- 4계층(Layer 1~4)과 11대 요소 메타데이터가 누락 없이 유지되어야 한다.
- 외부 API 키가 없어도 `AGENT_PLATFORM=offline` 폴백으로 항상 종료 코드 0과 유효한 JSON을 반환한다.
