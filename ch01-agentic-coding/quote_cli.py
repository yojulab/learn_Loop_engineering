"""제1장: 에이전트 루프와 비대화형 UNIX 파이프 실습용 명언 CLI."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

DEFAULT_QUOTES_PATH = Path(__file__).resolve().parent / "quotes.json"


def load_quotes(path: Path | str = DEFAULT_QUOTES_PATH) -> list[dict[str, Any]]:
    """JSON 파일에서 명언 목록을 로드한다."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("quotes.json must contain a JSON array")
    return data


def get_random_quote(
    quotes: list[dict[str, Any]],
    rng: random.Random | None = None,
) -> dict[str, Any]:
    """명언 목록에서 무작위 1건을 선택한다."""
    if not quotes:
        raise ValueError("Cannot select a random quote from an empty list")
    picker = rng if rng is not None else random
    return picker.choice(quotes)


def filter_by_tag(quotes: list[dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    """지정한 태그(대소문자 무시)를 포함한 명언 목록을 반환한다."""
    needle = tag.strip().lower()
    if not needle:
        return list(quotes)
    return [
        q for q in quotes
        if any(str(t).lower() == needle for t in q.get("tags", []))
    ]


def format_quotes(quotes: list[dict[str, Any]], as_json: bool = False) -> str:
    """명언 목록을 JSON 또는 사람이 읽기 쉬운 텍스트로 포맷한다."""
    if as_json:
        return json.dumps(quotes, ensure_ascii=False, indent=2)
    if not quotes:
        return "No matching quotes found."
    lines = []
    for q in quotes:
        tags = ", ".join(q.get("tags", []))
        lines.append(f"[{q.get('id', '?')}] \"{q['text']}\" — {q['author']} (tags: {tags})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="에이전틱 코딩 실습용 Quote CLI")
    parser.add_argument("--all", action="store_true", help="모든 명언 출력")
    parser.add_argument("--tag", type=str, default=None, help="특정 태그로 필터링")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    parser.add_argument("--seed", type=int, default=None, help="결정론적 무작위 시드")
    parser.add_argument("--data", type=str, default=str(DEFAULT_QUOTES_PATH), help="quotes.json 경로")
    args = parser.parse_args(argv)

    quotes = load_quotes(args.data)
    if args.tag:
        selected = filter_by_tag(quotes, args.tag)
    elif args.all:
        selected = quotes
    else:
        rng = random.Random(args.seed) if args.seed is not None else None
        selected = [get_random_quote(quotes, rng=rng)]

    print(format_quotes(selected, as_json=args.json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
