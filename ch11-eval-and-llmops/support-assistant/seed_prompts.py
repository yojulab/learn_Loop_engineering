from __future__ import annotations

from langfuse_ops import LangfuseOpsClient

V1_TEMPLATE = (
    "[티켓 {ticket_id}] 제품({product}) 문의 '{subject}' 확인했습니다.\n"
    "요청 내용: {message}\n"
    "안내: 정책을 확인해 주세요."
)

V2_TEMPLATE = (
    "[티켓 {ticket_id}] 제품({product}) 문의 '{subject}'에 대한 안내입니다.\n"
    "핵심 확인: {message} 관련 환불/계정 정책을 점검했습니다.\n"
    "다음 단계: 주문 번호와 함께 고객센터로 회신해 주시면 즉시 처리해 드리겠습니다."
)


def seed_default_prompts(ops: LangfuseOpsClient) -> None:
    ops.create_prompt(name="support-answer", prompt=V1_TEMPLATE, labels=["production"])
    ops.create_prompt(name="support-answer", prompt=V2_TEMPLATE, labels=["candidate"])
