from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class WikiDatabase:
    """SQLite FTS5 기반 RSS Wiki 아티클 및 전문 검색 저장소."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                content TEXT NOT NULL DEFAULT '',
                tags TEXT NOT NULL DEFAULT '',
                published_at TEXT NOT NULL DEFAULT ''
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
                title,
                summary,
                content,
                tags,
                content='articles',
                content_rowid='id'
            );

            CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN
                INSERT INTO articles_fts(rowid, title, summary, content, tags)
                VALUES (new.id, new.title, new.summary, new.content, new.tags);
            END;

            CREATE TRIGGER IF NOT EXISTS articles_ad AFTER DELETE ON articles BEGIN
                INSERT INTO articles_fts(articles_fts, rowid, title, summary, content, tags)
                VALUES ('delete', old.id, old.title, old.summary, old.content, old.tags);
            END;

            CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN
                INSERT INTO articles_fts(articles_fts, rowid, title, summary, content, tags)
                VALUES ('delete', old.id, old.title, old.summary, old.content, old.tags);
                INSERT INTO articles_fts(rowid, title, summary, content, tags)
                VALUES (new.id, new.title, new.summary, new.content, new.tags);
            END;
            """
        )
        self.conn.commit()

    def upsert_article(
        self,
        *,
        link: str,
        title: str,
        summary: str = "",
        content: str = "",
        tags: list[str] | str = "",
        published_at: str = "",
    ) -> int:
        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        cur = self.conn.execute(
            """
            INSERT INTO articles(link, title, summary, content, tags, published_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(link) DO UPDATE SET
                title=excluded.title,
                summary=excluded.summary,
                content=excluded.content,
                tags=excluded.tags,
                published_at=excluded.published_at
            """,
            (link, title, summary, content, tags_str, published_at),
        )
        self.conn.commit()
        if cur.lastrowid:
            return int(cur.lastrowid)
        row = self.conn.execute("SELECT id FROM articles WHERE link = ?", (link,)).fetchone()
        return int(row["id"])

    def list_articles(self, limit: int = 50) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM articles ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_article(self, article_id: int) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
        return dict(row) if row else None

    def search_fts(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        q = query.strip()
        if not q:
            return self.list_articles(limit=limit)
        rows = self.conn.execute(
            """
            SELECT a.*
            FROM articles_fts f
            JOIN articles a ON a.id = f.rowid
            WHERE articles_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (q, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def list_wiki_tags(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for art in self.list_articles(limit=200):
            tags = [t.strip() for t in art.get("tags", "").split(",") if t.strip()]
            for tag in tags or ["untagged"]:
                grouped.setdefault(tag, []).append(art)
        return grouped

    def close(self) -> None:
        self.conn.close()
