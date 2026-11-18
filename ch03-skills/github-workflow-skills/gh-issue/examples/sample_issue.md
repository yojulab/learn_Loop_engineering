# [BUG] quote-cli 태그 필터 대소문자 미일치 오류
라벨: bug, ch01

## 재현 절차
1. `python3 quote_cli.py --tag ENGINEERING` 실행
2. 빈 결과가 출력되는지 확인

## 기대 결과
대소문자 구분 없이 engineering 태그 명언이 출력되어야 한다.
