---
paths: ["*/SKILL.md", "*/reference.md", "*/scripts/validate_*.py", "tests/**/*.py"]
---
# 제3장: 온디맨드 노하우 모듈 — 3단계 확장형 스킬(Skills) 조건부 규칙

- 모든 스킬은 1단계(YAML frontmatter: name, description) -> 2단계(`SKILL.md` 본문 절차) -> 3단계(`reference.md`, `examples/`, `scripts/validate_*.py`)의 점진적 공개(Progressive Disclosure) 구조를 준수한다.
- 산출물 생성 후 반드시 해당 스킬의 `scripts/validate_*.py`로 형식 무결성을 검증한다.
