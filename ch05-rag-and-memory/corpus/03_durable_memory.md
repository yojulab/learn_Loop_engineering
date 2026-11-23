# Durable File Memory Pattern

대화 세션이 종료되어도 작업 연속성을 보장하려면 TASKS.md와 JOURNAL.md 파일에 상태를 저장해야 한다.
TASKS.md는 pending, done, blocked 상태를 관리하고 JOURNAL.md는 의사결정과 검증 증거만 요약 기록한다.
