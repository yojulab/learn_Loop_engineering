"""cli_litellm_eval.py — API 키 없이 CLI(`agy -p` / `claude -p`) -> LiteLLM Proxy -> Langfuse 통합 실행·평가 엔진.

Langfuse 공식 스펙(https://langfuse.com/docs) 준수 항목:
1. Trace Context: `userId`, `sessionId`, `tags`, `trace_name` 전달
2. Prompt Linkage: `promptName` + `promptVersion` 연결
3. Model & Cost: `/api/public/models`에 커스텀 모델 정의 자동 등록 (`matchPattern`, `inputPrice`, `outputPrice`)
4. Latency & Usage: LiteLLM `start_time`/`end_time` 기반 실제 지연시간 및 `TOKENS` 단위 사용량 기록
5. Observation-linked Scores: `observationId`(`uuid5("gen-" + trace_id)`)와 함께
   `accuracy`, `helpfulness`, `eval_safety_passed`, `eval_total_score` 점수 기록
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


def call_litellm_cli(
    prompt: str,
    *,
    trace_id: str,
    observation_id: str,
    model: str,
    user_id: str,
    session_id: str,
    prompt_name: str | None = None,
    prompt_version: int | None = None,
    proxy_url: str | None = None,
    master_key: str | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    resolved_base = _resolve_proxy_url(proxy_url)
    resolved_key = master_key or os.getenv("LITELLM_MASTER_KEY", "sk-litellm-local")
    metadata: dict[str, Any] = {
        "trace_id": trace_id,
        "observation_id": observation_id,
        "model_alias": model,
        "user_id": user_id,
        "session_id": session_id,
        "trace_name": f"support-eval:{model}",
    }
    if prompt_name:
        metadata["prompt_name"] = prompt_name
    if prompt_version is not None:
        metadata["prompt_version"] = int(prompt_version)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "metadata": metadata,
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


def run_cli_litellm_eval(
    *,
    model: str = "gemini-cli",
    query: str = "결제 오류로 환불 절차가 궁금합니다.",
    ticket_id: str = "T-CLI-001",
    product: str = "LoopPlatform",
    user_id: str = "user_cli_eval",
    session_id: str | None = None,
    proxy_url: str | None = None,
    expected_keywords: list[str] | None = None,
    reference_answer: str = DEFAULT_REFERENCE,
    store_dir: str | Path = "/tmp/langfuse_cli_eval_store",
    trace_id: str | None = None,
) -> dict[str, Any]:
    ops = LangfuseOpsClient(store_dir=store_dir)
    if ops.remote_enabled:
        ops.ensure_custom_model(
            model_name=model,
            match_pattern=f"(?i)^({model}|openai/{model})$",
            input_price=0.0000001,
            output_price=0.0000004,
            unit="TOKENS",
        )

    prompt_name = "support-answer"
    prompt_source = "default-template"
    prompt_version: int | None = None
    try:
        rec = ops.get_prompt(name=prompt_name, label="production")
        prompt_source = "langfuse-remote" if ops.remote_enabled else "offline-store"
        prompt_version = rec.version
        ticket = SupportTicket(
            ticket_id=ticket_id,
            product=product,
            subject="고객 문의",
            message=query,
            expected_keywords=expected_keywords or ["환불", "다음 단계"],
        )
        compiled_prompt = compile_prompt(rec, ticket)
    except Exception:
        prompt_name = "support-answer-fallback"
        compiled_prompt = (
            f"고객 티켓 {ticket_id} (제품: {product}) 문의에 대해 한국어로 답변하세요. "
            f"반드시 '다음 단계' 섹션을 포함하세요.\n문의: {query}"
        )

    tid = trace_id or str(uuid.uuid4())
    obs_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"gen-{tid}"))
    sid = session_id or f"sess-{model}-{tid[:8]}"
    resolved_proxy = _resolve_proxy_url(proxy_url)

    resp_json = call_litellm_cli(
        compiled_prompt,
        trace_id=tid,
        observation_id=obs_id,
        model=model,
        user_id=user_id,
        session_id=sid,
        prompt_name=prompt_name if prompt_version is not None else None,
        prompt_version=prompt_version,
        proxy_url=resolved_proxy,
    )
    answer = str(resp_json["choices"][0]["message"]["content"])

    kw_list = expected_keywords or ["환불", "다음 단계"]
    report = run_three_evals(answer, expected_keywords=kw_list, reference_answer=reference_answer)

    if ops.offline_mode:
        ops.log_trace(
            trace_id=tid,
            prompt_name=f"support-eval:{model}",
            prompt_version=prompt_version or 1,
            output=answer,
            score=report.total_score,
            input_payload=[{"role": "user", "content": compiled_prompt}],
        )

    comment = f"[{model}] rule={report.rule_score}, judge={report.judge_score}, safety={report.safety_passed}"
    # 대시보드 기본 컬럼(# accuracy, # helpfulness) + 안전성/종합 점수 모두 observationId와 함께 연결
    ops.log_score(tid, "accuracy", report.judge_score, comment=comment, observation_id=obs_id)
    ops.log_score(tid, "helpfulness", report.rule_score, comment=comment, observation_id=obs_id)
    ops.log_score(tid, "eval_safety_passed", 1.0 if report.safety_passed else 0.0, comment=comment, observation_id=obs_id)
    ops.log_score(tid, "eval_total_score", report.total_score, comment=comment, observation_id=obs_id)

    return {
        "trace_id": tid,
        "observation_id": obs_id,
        "user_id": user_id,
        "session_id": sid,
        "model": model,
        "proxy_url": resolved_proxy,
        "prompt_name": prompt_name,
        "prompt_version": prompt_version,
        "prompt_source": prompt_source,
        "langfuse_mode": "remote" if ops.remote_enabled else "offline-fallback",
        "langfuse_host": ops.host or None,
        "answer": answer,
        "eval": {
            "accuracy": report.judge_score,
            "helpfulness": report.rule_score,
            "safety_passed": report.safety_passed,
            "total_score": report.total_score,
        },
    }


def run_eval_cli(default_model: str, description: str) -> None:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--query", default="결제 오류로 환불 절차가 궁금합니다.")
    parser.add_argument("--ticket-id", default=f"T-{default_model.upper()}-001")
    parser.add_argument("--product", default="LoopPlatform")
    parser.add_argument("--user-id", default=f"user_{default_model.replace('-', '_')}")
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--model", default=default_model)
    parser.add_argument("--proxy-url", default=None)
    parser.add_argument("--expected-keywords", default="환불,다음 단계")
    parser.add_argument("--reference-answer", default=DEFAULT_REFERENCE)
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.expected_keywords.split(",") if k.strip()]
    try:
        result = run_cli_litellm_eval(
            model=args.model,
            query=args.query,
            ticket_id=args.ticket_id,
            product=args.product,
            user_id=args.user_id,
            session_id=args.session_id,
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
        print(f"[trace_id]       {result['trace_id']}")
        print(f"[observation_id] {result['observation_id']}")
        print(f"[user/session]   {result['user_id']} / {result['session_id']}")
        print(f"[model]          {result['model']} via {result['proxy_url']}")
        print(f"[langfuse]       {result['langfuse_mode']} ({result['langfuse_host']})")
        print(f"[eval]           {result['eval']}")
        print(f"[answer]\n{result['answer']}")
