"""제6장: 키워드(--search), 작성자(--author), 태그(--tag) 검색이 확장된 quote-cli."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

DEFAULT_QUOTES_PATH = Path(__file__).resolve().parent / "quotes.json"


def load_quotes(path: Path | str = DEFAULT_QUOTES_PATH) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def search_quotes(quotes: list[dict[str, Any]], keyword: str) -> list[dict[str, Any]]:
    needle = keyword.strip().lower()
    if not needle:
        return list(quotes)
    return [
        q for q in quotes
        if needle in str(q.get("text", "")).lower()
        or needle in str(q.get("author", "")).lower()
        or any(needle in str(t).lower() for t in q.get("tags", []))
    ]


def filter_by_author(quotes: list[dict[str, Any]], author: str) -> list[dict[str, Any]]:
    needle = author.strip().lower()
    return [q for q in quotes if needle in str(q.get("author", "")).lower()]


def filter_by_tag(quotes: list[dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    needle = tag.strip().lower()
    return [
        q for q in quotes
        if any(str(t).lower() == needle for t in q.get("tags", []))
    ]


def format_quotes(quotes: list[dict[str, Any]], as_json: bool = False) -> str:
    if as_json:
        return json.dumps(quotes, ensure_ascii=False, indent=2)
    if not quotes:
        return "No matching quotes found."
    return "\n".join(
        f"[{q.get('id', '?')}] \"{q['text']}\" — {q['author']} (tags: {', '.join(q.get('tags', []))})"
        for q in quotes
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="검색 확장 Quote CLI (제6장)")
    parser.add_argument("--search", type=str, default=None, help="키워드 검색")
    parser.add_argument("--author", type=str, default=None, help="작성자 필터")
    parser.add_argument("--tag", type=str, default=None, help="태그 필터")
    parser.add_argument("--all", action="store_true", help="전체 출력")
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    parser.add_argument("--seed", type=int, default=None, help="결정론적 시드")
    parser.add_argument("--data", type=str, default=str(DEFAULT_QUOTES_PATH))
    args = parser.parse_args(argv)

    results = load_quotes(args.data)
    filtered = False
    if args.search:
        results = search_quotes(results, args.search)
        filtered = True
    if args.author:
        results = filter_by_author(results, args.author)
        filtered = True
    if args.tag:
        results = filter_by_tag(results, args.tag)
        filtered = True

    if not filtered and not args.all and results:
        rng = random.Random(args.seed) if args.seed is not None else random
        results = [rng.choice(results)]

    print(format_quotes(results, as_json=args.json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
