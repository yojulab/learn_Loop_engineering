"""제2장: FastMCP(또는 내장 LocalFastMCP 어댑터) 기반 quote-mcp 서버."""

from __future__ import annotations

import inspect
import json
import os
import random
from pathlib import Path
from typing import Any, Callable


class LocalFastMCP:
    """외부 mcp.server.fastmcp 미설치 시 동일 데코레이터 계약을 제공하는 경량 어댑터."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._tools: dict[str, Callable[..., Any]] = {}
        self._resources: dict[str, Callable[..., Any]] = {}
        self._prompts: dict[str, Callable[..., Any]] = {}

    def tool(self, name: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or fn.__name__
            self._tools[tool_name] = fn
            return fn
        return decorator

    def resource(self, uri: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._resources[uri] = fn
            return fn
        return decorator

    def prompt(self, name: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            prompt_name = name or fn.__name__
            self._prompts[prompt_name] = fn
            return fn
        return decorator

    def list_tools(self) -> list[str]:
        return sorted(self._tools.keys())

    def list_resources(self) -> list[str]:
        return sorted(self._resources.keys())

    def list_prompts(self) -> list[str]:
        return sorted(self._prompts.keys())

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name](**kwargs)

    def read_resource(self, uri: str) -> Any:
        if uri not in self._resources:
            raise KeyError(f"Unknown resource: {uri}")
        return self._resources[uri]()

    def get_prompt(self, name: str, **kwargs: Any) -> Any:
        if name not in self._prompts:
            raise KeyError(f"Unknown prompt: {name}")
        return self._prompts[name](**kwargs)

    def run(self, transport: str = "stdio") -> dict[str, Any]:
        """오프라인 테스트용 메타데이터 요약 반환."""
        return {
            "server": self.name,
            "transport": transport,
            "tools": self.list_tools(),
            "resources": self.list_resources(),
            "prompts": self.list_prompts(),
        }


try:
    from mcp.server.fastmcp import FastMCP as _ExternalFastMCP  # type: ignore
    FastMCP = _ExternalFastMCP
    USING_EXTERNAL_FASTMCP = True
except ImportError:
    FastMCP = LocalFastMCP
    USING_EXTERNAL_FASTMCP = False

DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "quotes.json"


def _resolve_data_path() -> Path:
    raw = os.environ.get("QUOTE_DATA_PATH", "").strip()
    return Path(raw) if raw else DEFAULT_DATA_PATH


def _load_quotes(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or _resolve_data_path()
    if not target.is_file():
        return []
    return json.loads(target.read_text(encoding="utf-8"))


def _save_quotes(quotes: list[dict[str, Any]], path: Path | None = None) -> None:
    target = path or _resolve_data_path()
    target.write_text(json.dumps(quotes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


mcp = FastMCP("quote-mcp")


@mcp.tool()
def get_random_quote(tag: str | None = None) -> dict[str, Any]:
    """태그 조건(선택)에 맞는 무작위 명언 1건을 반환한다."""
    quotes = _load_quotes()
    if tag:
        needle = tag.strip().lower()
        quotes = [
            q for q in quotes
            if any(str(t).lower() == needle for t in q.get("tags", []))
        ]
    if not quotes:
        return {"error": f"No quotes found for tag={tag!r}"}
    return random.choice(quotes)


@mcp.tool()
def add_quote(text: str, author: str, tags: list[str] | None = None) -> dict[str, Any]:
    """새 명언을 저장소에 추가하고 생성된 레코드를 반환한다."""
    clean_text = text.strip()
    clean_author = author.strip()
    if not clean_text or not clean_author:
        raise ValueError("text and author must not be empty")
    quotes = _load_quotes()
    next_id = max((int(q.get("id", 0)) for q in quotes), default=0) + 1
    record = {
        "id": next_id,
        "text": clean_text,
        "author": clean_author,
        "tags": [t.strip() for t in (tags or []) if t.strip()],
    }
    quotes.append(record)
    _save_quotes(quotes)
    return {"status": "added", "quote": record}


@mcp.resource("quote://all")
def read_all_quotes() -> str:
    """저장소의 모든 명언을 JSON 문자열 리소스로 반환한다."""
    return json.dumps(_load_quotes(), ensure_ascii=False, indent=2)


@mcp.prompt()
def quote_post(topic: str, tone: str = "inspiring") -> str:
    """특정 주제와 톤에 맞춰 명언 기반 포스트 초안 프롬프트를 생성한다."""
    sample = get_random_quote(tag=topic)
    if "error" in sample:
        sample = get_random_quote()
    return (
        f"[Tone: {tone}] Write a concise engineering note on '{topic}' "
        f"anchored by the quote: \"{sample.get('text', '')}\" — {sample.get('author', 'Unknown')}."
    )


if __name__ == "__main__":
    sig = inspect.signature(mcp.run)
    if len(sig.parameters) == 0:
        mcp.run()
    else:
        print(json.dumps(mcp.run(), ensure_ascii=False))
