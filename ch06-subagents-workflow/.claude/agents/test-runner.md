---
name: test-runner
description: 단위 테스트를 실행하고 실패 원인과 커버리지 요약을 보고하는 워커
tools: [Read, Bash, Grep]
model: haiku
---

# test-runner

테스트 스위트를 실행하고 종료 코드와 실패 케이스 요약만 반환합니다.
