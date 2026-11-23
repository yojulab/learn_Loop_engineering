# Context Window Budget Guide

컨텍스트 윈도우가 75%를 초과하면 Lost-in-the-Middle 현상이 급격히 증가한다.
오래된 도구 로그와 실패한 추론은 `/compact`로 압축하거나 `/clear`로 초기화해야 한다.
핵심 규칙은 프롬프트 맨 앞과 맨 뒤에 배치해 모델의 주의 집중력을 유지한다.
