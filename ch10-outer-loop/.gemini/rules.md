# .gemini/rules.md — 제10장: 아우터 루프 엔지니어링 (5단계 루프 & 7대 완료·중단 조건)

- `Discover -> Plan -> Execute -> Verify -> Iterate` 5단계 루프와 7대 완료·중단 조건(예산, 반복, 연속 실패, 인간 이관 HALT)을 준수한다.
- 워커의 자체 완료 선언과 무관하게 `calc_verifier.py` 독립 검증기가 통과해야만 `DONE`으로 전이한다.
