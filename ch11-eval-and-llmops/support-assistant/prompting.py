from __future__ import annotations

from models import PromptRecord, SupportTicket


def compile_prompt(prompt: PromptRecord, ticket: SupportTicket) -> str:
    return prompt.compile(
        ticket_id=ticket.ticket_id,
        product=ticket.product,
        subject=ticket.subject,
        message=ticket.message,
    )
