"""agy_litellm_eval.py — API 키 없이 `agy -p` -> LiteLLM Proxy -> Langfuse(Trace + Eval Scores) 통합 실행기.

동작 흐름:
1. Langfuse에서 `production` 프롬프트(`support-answer`)를 조회(또는 기본 템플릿 사용)해 문의 티켓을 컴파일
2. 고유 `trace_id`를 생성해 LiteLLM Proxy(`model="agy-cli"`)로 `/chat/completions` 호출
   - LiteLLM은 `agy_openai_bridge`를 통해 `agy -p`를 실행하므로 OPENAI/ANTHROPIC/GEMINI API 키 불필요
   - LiteLLM의 `langfuse_v2_callback`이 동일한 `trace_id`로 Langfuse Trace 및 Generation 자동 적재
3. 응답 결과에 대해 `evaluator.run_three_evals()`(규칙·유사도·안전성 3종 Eval) 실행
4. 산출된 평가 점수 4종을 Langfuse `/api/public/scores`에 동일한 `trace_id`와 연결해 기록
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from evaluator import run_three_evals  # noqa: E402
from langfuse_ops import LangfuseOpsClient  # noqa: E402
from models import SupportTicket  # noqa: E402
from prompting import compile_prompt  # noqa: E402


DEFAULT_REFERENCE = (
    "결제 오류 확인 후 다음 단계 안내: 영수증 번호와 결제 시각을 회신해 주시면 "
    "영업일 기준 3일 이내 환불 처리됩니다."
)


def _resolve_proxy_url(explicit_url: str | None = None) -> str:
    if explicit_url:
        return explicit_url.rstrip("/")
    env_url = os.getenv("OPENAI_BASE_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")
    for candidate in ("http://litellm-proxy:4000/v1", "http://localhost:4000/v1"):
        health_url = candidate.rsplit("/v1", 1)[0] + "/health/liveliness"
        try:
            with urllib.request.urlopen(health_url, timeout=2) as resp:
                if resp.status == 200:
                    return candidate
        except Exception:
            continue
    return "http://localhost:4000/v1"


def call_litellm_agy(
    prompt: str,
    *,
    trace_id: str,
    model: str = "agy-cli",
    proxy_url: str | None = None,
    master_key: str | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    resolved_base = _resolve_proxy_url(proxy_url)
    resolved_key = master_key or os.getenv("LITELLM_MASTER_KEY", "sk-litellm-local")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "metadata": {"trace_id": trace_id},
    }
    req = urllib.request.Request(
        f"{resolved_base}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {resolved_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_agy_litellm_eval(
    *,
    query: str = "결제 오류로 환불 절차가 궁금합니다.",
    ticket_id: str = "T-AGY-001",
    customer_tier: str = "pro",
    model: str = "agy-cli",
    proxy_url: str | None = None,
    expected_keywords: list[str] | None = None,
    reference_answer: str = DEFAULT_REFERENCE,
    store_dir: str | Path = "/tmp/langfuse_agy_eval_store",
    trace_id: str | None = None,
) -> dict[str, Any]:
    ops = LangfuseOpsClient(store_dir=store_dir)
    prompt_source = "default-template"
    prompt_version = 1
    try:
        rec = ops.get_prompt(name="support-answer", label="production")
        prompt_source = "langfuse-remote" if ops.remote_enabled else "offline-store"
        prompt_version = rec.version
        ticket = SupportTicket(ticket_id=ticket_id, product=customer_tier, subject="고객 문의", message=query, expected_keywords=expected_keywords or ["환불", "다음 단계"])
        compiled_prompt = compile_prompt(rec, ticket)
    except Exception:
        compiled_prompt = (
            f"고객 티켓 {ticket_id} (등급: {customer_tier}) 문의에 대해 한국어로 답변하세요. "
            f"반드시 '다음 단계' 섹션을 포함하세요.\n문의: {query}"
        )

    tid = trace_id or str(uuid.uuid4())
    resolved_proxy = _resolve_proxy_url(proxy_url)
    resp_json = call_litellm_agy(
        compiled_prompt,
        trace_id=tid,
        model=model,
        proxy_url=resolved_proxy,
    )
    answer = str(resp_json["choices"][0]["message"]["content"])

    # LiteLLM이 remote Langfuse에 비동기로 보내는 동안에도 오프라인 모드일 땐 로컬 트레이스 보장
    kw_list = expected_keywords or ["환불", "다음 단계"]
    report = run_three_evals(answer, expected_keywords=kw_list, reference_answer=reference_answer)

    if ops.offline_mode:
        ops.log_trace(
            trace_id=tid,
            prompt_name=f"litellm:{model}",
            prompt_version=prompt_version,
            output=answer,
            score=report.total_score,
            input_payload=[{"role": "user", "content": compiled_prompt}],
        )

    comment = f"rule={report.rule_score}, judge={report.judge_score}, safety={report.safety_passed}"
    ops.log_score(tid, "eval_rule_score", report.rule_score, comment=comment)
    ops.log_score(tid, "eval_judge_score", report.judge_score, comment=comment)
    ops.log_score(tid, "eval_safety_passed", 1.0 if report.safety_passed else 0.0, comment=comment)
    ops.log_score(tid, "eval_total_score", report.total_score, comment=comment)

    return {
        "trace_id": tid,
        "model": model,
        "proxy_url": resolved_proxy,
        "prompt_source": prompt_source,
        "langfuse_mode": "remote" if ops.remote_enabled else "offline-fallback",
        "langfuse_host": ops.host or None,
        "answer": answer,
        "eval": {
            "rule_score": report.rule_score,
            "judge_score": report.judge_score,
            "safety_passed": report.safety_passed,
            "total_score": report.total_score,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="agy -p -> LiteLLM -> Langfuse Trace & Eval 실행기")
    parser.add_argument("--query", default="결제 오류로 환불 절차가 궁금합니다.")
    parser.add_argument("--ticket-id", default="T-AGY-001")
    parser.add_argument("--customer-tier", default="pro")
    parser.add_argument("--model", default="agy-cli")
    parser.add_argument("--proxy-url", default=None)
    parser.add_argument("--expected-keywords", default="환불,다음 단계")
    parser.add_argument("--reference-answer", default=DEFAULT_REFERENCE)
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.expected_keywords.split(",") if k.strip()]
    try:
        result = run_agy_litellm_eval(
            query=args.query,
            ticket_id=args.ticket_id,
            customer_tier=args.customer_tier,
            model=args.model,
            proxy_url=args.proxy_url,
            expected_keywords=keywords,
            reference_answer=args.reference_answer,
        )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"ERROR: LiteLLM 호출 실패 (HTTP {exc.code}): {body}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[trace_id] {result['trace_id']}")
        print(f"[model]    {result['model']} via {result['proxy_url']}")
        print(f"[langfuse] {result['langfuse_mode']} ({result['langfuse_host']})")
        print(f"[eval]     {result['eval']}")
        print(f"[answer]\n{result['answer']}")


if __name__ == "__main__":
    main()
