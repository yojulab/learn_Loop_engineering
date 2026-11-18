"""제5장: Top-K 제한 및 발췌 필터링(excerpt filtering) Agentic RAG 사서."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣_]+")


@dataclass
class DocumentChunk:
    source: str
    title: str
    excerpt: str
    score: int
    matched_terms: list[str]


def _tokenize(text: str) -> list[str]:
    return [tok.lower() for tok in TOKEN_RE.findall(text) if len(tok) >= 2]


def _extract_best_excerpt(
    content: str,
    query_terms: set[str],
    max_chars: int,
) -> str:
    """쿼리 토큰이 집중된 문장/줄만 발췌하여 max_chars 이내로 잘라 반환한다."""
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        return ""

    scored_lines: list[tuple[int, str]] = []
    for line in lines:
        line_tokens = set(_tokenize(line))
        overlap = sum(1 for qt in query_terms if any(qt in lt or lt in qt for lt in line_tokens))
        if overlap > 0:
            scored_lines.append((overlap, line))

    if not scored_lines:
        raw = lines[0]
    else:
        scored_lines.sort(key=lambda item: item[0], reverse=True)
        raw = " ".join(text for _, text in scored_lines[:2])

    if len(raw) <= max_chars:
        return raw
    if max_chars <= 3:
        return raw[:max_chars]
    return raw[: max_chars - 3].rstrip() + "..."


class AgenticRetriever:
    """오프라인 마크다운 코퍼스 대상 Top-K & 발췌 필터링 검색기."""

    def __init__(self, corpus_dir: Path | str) -> None:
        self.corpus_dir = Path(corpus_dir)

    def search(
        self,
        query: str,
        top_k: int = 3,
        max_chars_per_excerpt: int = 240,
    ) -> list[DocumentChunk]:
        if top_k <= 0 or max_chars_per_excerpt <= 0 or not self.corpus_dir.is_dir():
            return []

        q_terms = list(dict.fromkeys(_tokenize(query)))
        if not q_terms:
            return []
        q_set = set(q_terms)

        candidates: list[DocumentChunk] = []
        for md_path in sorted(self.corpus_dir.glob("*.md")):
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            title = next((ln.lstrip("# ").strip() for ln in lines if ln.startswith("#")), md_path.stem)
            doc_tokens = _tokenize(text)
            doc_set = set(doc_tokens)

            matched = [
                qt for qt in q_terms
                if any(qt in dt or dt in qt for dt in doc_set)
            ]
            if not matched:
                continue

            score = sum(doc_tokens.count(dt) for dt in doc_set if any(qt in dt or dt in qt for qt in q_set))
            excerpt = _extract_best_excerpt(text, q_set, max_chars_per_excerpt)
            candidates.append(
                DocumentChunk(
                    source=md_path.name,
                    title=title,
                    excerpt=excerpt,
                    score=score,
                    matched_terms=matched,
                )
            )

        candidates.sort(key=lambda c: (-c.score, c.source))
        return candidates[:top_k]
