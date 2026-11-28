from __future__ import annotations

import re
from dataclasses import dataclass, field

_MUSTACHE_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


@dataclass
class SupportTicket:
    ticket_id: str
    product: str
    subject: str
    message: str
    expected_keywords: list[str] = field(default_factory=list)


@dataclass
class PromptRecord:
    name: str
    version: int
    template: str
    labels: list[str] = field(default_factory=list)

    def compile(self, **kwargs: object) -> str:
        """Langfuse Mustache `{{var}}` 문법과 Python `{var}` 문법을 모두 지원해 변수를 치환합니다."""
        rendered = _MUSTACHE_RE.sub(
            lambda m: str(kwargs[m.group(1)]) if m.group(1) in kwargs else m.group(0),
            self.template,
        )
        if any(f"{{{k}}}" in rendered for k in kwargs):
            try:
                return rendered.format(**kwargs)
            except KeyError:
                pass
        return rendered


@dataclass
class EvalReport:
    rule_score: float
    judge_score: float
    safety_passed: bool
    total_score: float
