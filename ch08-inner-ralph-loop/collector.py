from __future__ import annotations

import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from db import WikiDatabase

_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class FeedItem:
    title: str
    link: str
    summary: str
    content: str
    tags: list[str] = field(default_factory=list)
    published_at: str = ""


def clean_html(text: str) -> str:
    unescaped = html.unescape(text or "")
    return re.sub(r"\s+", " ", _TAG_RE.sub(" ", unescaped)).strip()


def parse_rss_xml(xml_text: str) -> list[FeedItem]:
    root = ET.fromstring(xml_text)
    items: list[FeedItem] = []
    for item_el in root.findall(".//item"):
        title = clean_html(item_el.findtext("title", ""))
        link = (item_el.findtext("link", "") or "").strip()
        desc = clean_html(item_el.findtext("description", ""))
        pub = (item_el.findtext("pubDate", "") or "").strip()
        cats = [clean_html(c.text or "") for c in item_el.findall("category") if (c.text or "").strip()]
        if title and link:
            items.append(
                FeedItem(
                    title=title,
                    link=link,
                    summary=desc[:200],
                    content=desc,
                    tags=cats,
                    published_at=pub,
                )
            )
    return items


def collect_from_source(source: str | Path, db: WikiDatabase | None = None) -> list[FeedItem]:
    src_str = str(source)
    if src_str.startswith(("http://", "https://")):
        with urllib.request.urlopen(src_str, timeout=10) as resp:
            xml_text = resp.read().decode("utf-8")
    else:
        xml_text = Path(source).read_text(encoding="utf-8")
    items = parse_rss_xml(xml_text)
    if db is not None:
        for item in items:
            db.upsert_article(
                link=item.link,
                title=item.title,
                summary=item.summary,
                content=item.content,
                tags=item.tags,
                published_at=item.published_at,
            )
    return items
