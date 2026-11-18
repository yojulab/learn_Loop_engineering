from __future__ import annotations

from dataclasses import dataclass, field


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
        return self.template.format(**kwargs)


@dataclass
class EvalReport:
    rule_score: float
    judge_score: float
    safety_passed: bool
    total_score: float
