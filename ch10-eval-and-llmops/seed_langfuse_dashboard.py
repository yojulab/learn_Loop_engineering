"""
ch10-eval-and-llmops/seed_langfuse_dashboard.py
Langfuse v2 Dashboard / Tracing / Sessions / Generations / Scores / Models / Users / Prompts / Datasets
모든 화면 항목을 한 번에 확인할 수 있도록 AI 폴백 모드로 초기 데이터를 적재하는 CLI.

옵션(미입력 시 Default 값으로 즉시 실행):
  --hours     시간 간격(과거 N시간 분포, 기본값: 24)
  --per-hour  시간당 실행 회수(기본값: 3 -> 총 72건)
  --models    쉼표 구분 모델 목록(기본값: gpt-4o-mini,claude-3-5-sonnet,gemini-2.5-flash)
  --topic     업무 주제(기본값: 고객지원 및 장애 트리아지)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent
for p in (str(APP_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

DEFAULT_MODELS = "gpt-4o-mini,claude-3-5-sonnet,gemini-2.5-flash"
DEFAULT_TOPIC = "고객지원 및 장애 트리아지"
MODEL_TO_PLATFORM = {
    "claude": "claude",
    "gpt": "chatgpt",
    "o1": "chatgpt",
    "o3": "chatgpt",
    "gemini": "gemini",
}
# 토큰당 단가(USD / 1M tokens) — Langfuse Model costs 위젯 즉시 표시용
MODEL_PRICING_PER_M: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    "claude-3-5-sonnet": (3.00, 15.00),
    "gemini-2.5-flash": (0.15, 0.60),
}


def _infer_platform(model: str) -> str:
    low = model.lower()
    for prefix, plat in MODEL_TO_PLATFORM.items():
        if prefix in low:
            return plat
    return "offline"


def _deterministic_unit(seed_key: str) -> float:
    digest = hashlib.sha256(seed_key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def generate_fallback_response(topic: str, model: str, query: str) -> str:
    """외부 API 키 없이도 주제·모델별 현실적인 AI 폴백 응답을 생성합니다."""
    return (
        f"[{model} · AI-Fallback] '{topic}' 요청 분석 완료 — "
        f"핵심 요약: {query} | 조치: 정책 기준 확인 및 담당 큐 라우팅(신뢰도 0.92)"
    )


def build_seed_events(
    hours: int = 24,
    per_hour: int = 3,
    models: list[str] | None = None,
    topic: str = DEFAULT_TOPIC,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    """시간 간격·시간당 회수·모델·업무 주제 기반 결정론적 시드 이벤트 목록 생성."""
    if hours <= 0 or per_hour <= 0:
        raise ValueError("hours와 per_hour는 1 이상의 정수여야 합니다.")
    model_list = [m.strip() for m in (models or DEFAULT_MODELS.split(",")) if m.strip()]
    if not model_list:
        raise ValueError("최소 1개 이상의 모델을 지정해야 합니다.")

    base_now = now or datetime.now(timezone.utc)
    users = ["user_alice", "user_bob", "user_charlie", "user_dana"]
    scenarios = [
        "결제 영수증 재발급 및 법인카드 증빙 요청",
        "API 게이트웨이 502 간헐적 지연 장애 원인 분석",
        "구독 플랜 업그레이드 후 권한 동기화 누락 문의",
        "환불 정책 예외 승인 기준 및 SLA 확인",
        "웹훅 서명 검증 실패 로그 트리아지 요청",
    ]

    events: list[dict[str, Any]] = []
    idx = 0
    for h_offset in range(hours - 1, -1, -1):
        for slot in range(per_hour):
            idx += 1
            model = model_list[(idx - 1) % len(model_list)]
            user_id = users[(idx - 1) % len(users)]
            session_id = f"sess-{topic[:8]}-{(idx - 1) // 3 + 1:03d}"
            scenario = scenarios[(idx - 1) % len(scenarios)]
            u = _deterministic_unit(f"{topic}:{model}:{h_offset}:{slot}")

            # 1) 타임스탬프 분산(과거 N시간 내 균등 분포)
            minute_offset = int((slot + u * 0.7) * (60 / max(1, per_hour)))
            t_start = base_now - timedelta(hours=h_offset, minutes=max(0, 59 - minute_offset))
            span_ms = 120 + int(u * 380)
            gen_ms = 350 + int(((u * 1.7) % 1.0) * 1650)
            t_span_end = t_start + timedelta(milliseconds=span_ms)
            t_gen_end = t_span_end + timedelta(milliseconds=gen_ms)

            # 2) 토큰 및 비용 계산
            in_tokens = 180 + int(u * 420)
            out_tokens = 90 + int(((u * 2.3) % 1.0) * 260)
            in_rate, out_rate = MODEL_PRICING_PER_M.get(model, (0.50, 1.50))
            in_cost = round((in_tokens / 1_000_000) * in_rate, 6)
            out_cost = round((out_tokens / 1_000_000) * out_rate, 6)
            tot_cost = round(in_cost + out_cost, 6)

            # 3) AI 폴백 응답 및 평가 점수
            query = f"[{topic}] {scenario}"
            answer = generate_fallback_response(topic, model, scenario)
            acc_score = round(0.72 + u * 0.26, 2)
            help_score = round(0.75 + (((u * 1.3) % 1.0) * 0.24), 2)

            events.append(
                {
                    "index": idx,
                    "trace_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"loop-{topic}-{idx}-{model}")),
                    "name": f"{topic}-workflow",
                    "user_id": user_id,
                    "session_id": session_id,
                    "model": model,
                    "platform": _infer_platform(model),
                    "t_start": t_start,
                    "t_span_end": t_span_end,
                    "t_gen_end": t_gen_end,
                    "input": {"topic": topic, "query": query},
                    "output": {"answer": answer},
                    "usage": {"input": in_tokens, "output": out_tokens, "total": in_tokens + out_tokens, "unit": "TOKENS"},
                    "cost_details": {"input": in_cost, "output": out_cost, "total": tot_cost},
                    "scores": {"accuracy": acc_score, "helpfulness": help_score},
                    "tags": ["ai-fallback", _infer_platform(model), topic],
                }
            )
    return events


def seed_to_langfuse(
    events: list[dict[str, Any]],
    topic: str = DEFAULT_TOPIC,
    dry_run: bool = False,
) -> dict[str, Any]:
    """생성된 이벤트를 Langfuse v2 서버에 적재해 Dashboard/Prompts/Datasets 전체 활성화."""
    if dry_run:
        return {
            "mode": "dry-run-ai-fallback",
            "topic": topic,
            "traces_count": len(events),
            "models": sorted({e["model"] for e in events}),
            "users": sorted({e["user_id"] for e in events}),
            "sessions": len({e["session_id"] for e in events}),
            "total_cost_usd": round(sum(e["cost_details"]["total"] for e in events), 6),
        }

    from langfuse import Langfuse  # 지연 임포트: dry-run/오프라인 단위 테스트는 SDK 없이도 통과

    host = os.getenv("LANGFUSE_HOST", "http://localhost:30000")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    if not (public_key and secret_key):
        raise RuntimeError("LANGFUSE_PUBLIC_KEY 및 LANGFUSE_SECRET_KEY 환경 변수가 필요합니다.")

    lf = Langfuse(public_key=public_key, secret_key=secret_key, host=host)

    # 1) Prompts 등록 (Prompts 탭 & Generation 연결용)
    prompt_name = "loop-assistant-triage"
    prompt_client = lf.create_prompt(
        name=prompt_name,
        prompt="업무 주제({{topic}}) 요청에 대해 근거 기반으로 요약·조치를 안내하세요.\n문의: {{query}}",
        labels=["production"],
        tags=["ai-fallback", topic],
    )

    # 2) Dataset 생성 (Datasets 탭용)
    dataset_name = "loop-triage-benchmark"
    lf.create_dataset(
        name=dataset_name,
        description=f"{topic} AI 폴백 검증 데이터셋",
        metadata={"topic": topic, "mode": "ai-fallback"},
    )

    # 3) Traces · Spans · Generations · Scores 적재
    dataset_linked = 0
    for ev in events:
        trace = lf.trace(
            id=ev["trace_id"],
            name=ev["name"],
            user_id=ev["user_id"],
            session_id=ev["session_id"],
            input=ev["input"],
            output=ev["output"],
            tags=ev["tags"],
            timestamp=ev["t_start"],
            metadata={"mode": "ai-fallback", "topic": topic},
        )
        trace.span(
            name="rag-context-lookup",
            start_time=ev["t_start"],
            end_time=ev["t_span_end"],
            input={"query": ev["input"]["query"]},
            output={"hits": 3, "top_doc": "02_refund_policy.md"},
        )
        gen = trace.generation(
            name="llm-response",
            model=ev["model"],
            start_time=ev["t_span_end"],
            end_time=ev["t_gen_end"],
            input=ev["input"],
            output=ev["output"]["answer"],
            usage=ev["usage"],
            cost_details=ev["cost_details"],
            prompt=prompt_client,
            metadata={"fallback": True},
        )
        for s_name, s_val in ev["scores"].items():
            trace.score(name=s_name, value=s_val, data_type="NUMERIC", comment="ai-fallback auto eval")

        # 상위 5건은 Dataset Item + Run 링크까지 연결
        if dataset_linked < 5:
            dataset_linked += 1
            item = lf.create_dataset_item(
                dataset_name=dataset_name,
                input=ev["input"],
                expected_output=ev["output"],
                source_trace_id=ev["trace_id"],
            )
            # Dataset Run 연결 (item.link)
            if hasattr(item, "link"):
                item.link(gen, run_name="ai-fallback-baseline")

    lf.flush()
    return {
        "mode": "langfuse-live-ai-fallback",
        "host": host,
        "topic": topic,
        "traces_seeded": len(events),
        "scores_seeded": len(events) * 2,
        "models": sorted({e["model"] for e in events}),
        "users": sorted({e["user_id"] for e in events}),
        "sessions": len({e["session_id"] for e in events}),
        "prompt_name": prompt_name,
        "dataset_name": dataset_name,
        "dataset_items_linked": dataset_linked,
        "total_cost_usd": round(sum(e["cost_details"]["total"] for e in events), 6),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Langfuse v2 Dashboard 전체 항목 초기화 시더 (AI 폴백 모드, 옵션 미입력 시 Default 진행)",
    )
    parser.add_argument("--hours", type=int, default=24, help="데이터 분산 시간 간격 (기본값: 24)")
    parser.add_argument("--per-hour", type=int, default=3, help="시간당 실행 회수 (기본값: 3)")
    parser.add_argument("--models", default=DEFAULT_MODELS, help=f"쉼표 구분 Model 종류 (기본값: {DEFAULT_MODELS})")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help=f"업무 주제 (기본값: {DEFAULT_TOPIC})")
    parser.add_argument("--dry-run", action="store_true", help="Langfuse 전송 없이 AI 폴백 시드 요약만 확인")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 요약 출력")
    args = parser.parse_args(argv)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    events = build_seed_events(hours=args.hours, per_hour=args.per_hour, models=models, topic=args.topic)
    summary = seed_to_langfuse(events, topic=args.topic, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            f"[Langfuse Seed OK] mode={summary['mode']} | topic='{summary['topic']}' | "
            f"traces={summary.get('traces_seeded', summary.get('traces_count'))} | "
            f"models={','.join(summary['models'])} | total_cost=${summary['total_cost_usd']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
