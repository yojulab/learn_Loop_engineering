from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from db import WikiDatabase

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


@dataclass
class MiniResponse:
    status_code: int
    text: str

    def json(self) -> dict[str, Any]:
        import json
        return json.loads(self.text)


class MiniTestClient:
    """FastAPI 미설치 환경에서도 동일 라우트 계약을 검증하는 경량 TestClient."""

    def __init__(self, app: "MiniWebApp") -> None:
        self.app = app

    def get(self, url: str) -> MiniResponse:
        parsed = urlparse(url)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        status, body = self.app.dispatch("GET", parsed.path, query)
        return MiniResponse(status_code=status, text=body)


class MiniWebApp:
    def __init__(self, db: WikiDatabase) -> None:
        self.db = db
        self.routes: list[tuple[str, Callable[..., tuple[int, str]]]] = []

    def dispatch(self, method: str, path: str, query: dict[str, str]) -> tuple[int, str]:
        if path == "/health":
            return 200, '{"status":"ok","fts5":true}'
        if path in {"/", "/articles"}:
            articles = self.db.list_articles()
            items = "".join(f"<li>{html.escape(a['title'])}</li>" for a in articles)
            tpl = (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")
            return 200, tpl.replace("{{items}}", items)
        if path.startswith("/articles/"):
            try:
                aid = int(path.split("/")[-1])
            except ValueError:
                return 404, "Not Found"
            art = self.db.get_article(aid)
            if not art:
                return 404, "Not Found"
            tpl = (TEMPLATES_DIR / "article.html").read_text(encoding="utf-8")
            return 200, tpl.replace("{{title}}", html.escape(art["title"])).replace("{{content}}", html.escape(art["content"]))
        if path == "/search":
            q = query.get("q", "")
            results = self.db.search_fts(q)
            items = "".join(f"<li>{html.escape(r['title'])}</li>" for r in results)
            tpl = (TEMPLATES_DIR / "search.html").read_text(encoding="utf-8")
            return 200, tpl.replace("{{query}}", html.escape(q)).replace("{{items}}", items)
        if path == "/wiki":
            tags = self.db.list_wiki_tags()
            tag_li = "".join(f"<li>{html.escape(k)} ({len(v)})</li>" for k, v in sorted(tags.items()))
            tpl = (TEMPLATES_DIR / "wiki.html").read_text(encoding="utf-8")
            return 200, tpl.replace("{{tags}}", tag_li)
        return 404, "Not Found"


def create_app(db_path: str | Path = ":memory:") -> Any:
    db = WikiDatabase(db_path)
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse, JSONResponse
        from fastapi.templating import Jinja2Templates

        app = FastAPI(title="RSS Wiki")
        app.state.db = db
        templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

        @app.get("/health")
        def health() -> JSONResponse:
            return JSONResponse({"status": "ok", "fts5": True})

        @app.get("/", response_class=HTMLResponse)
        @app.get("/articles", response_class=HTMLResponse)
        def index(request: Request) -> HTMLResponse:
            articles = db.list_articles()
            items = "".join(f"<li>{html.escape(a['title'])}</li>" for a in articles)
            tpl = (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")
            return HTMLResponse(tpl.replace("{{items}}", items))

        @app.get("/articles/{article_id}", response_class=HTMLResponse)
        def article_detail(article_id: int) -> HTMLResponse:
            art = db.get_article(article_id)
            if not art:
                return HTMLResponse("Not Found", status_code=404)
            tpl = (TEMPLATES_DIR / "article.html").read_text(encoding="utf-8")
            return HTMLResponse(tpl.replace("{{title}}", html.escape(art["title"])).replace("{{content}}", html.escape(art["content"])))

        @app.get("/search", response_class=HTMLResponse)
        def search(q: str = "") -> HTMLResponse:
            results = db.search_fts(q)
            items = "".join(f"<li>{html.escape(r['title'])}</li>" for r in results)
            tpl = (TEMPLATES_DIR / "search.html").read_text(encoding="utf-8")
            return HTMLResponse(tpl.replace("{{query}}", html.escape(q)).replace("{{items}}", items))

        @app.get("/wiki", response_class=HTMLResponse)
        def wiki() -> HTMLResponse:
            tags = db.list_wiki_tags()
            tag_li = "".join(f"<li>{html.escape(k)} ({len(v)})</li>" for k, v in sorted(tags.items()))
            tpl = (TEMPLATES_DIR / "wiki.html").read_text(encoding="utf-8")
            return HTMLResponse(tpl.replace("{{tags}}", tag_li))

        return app
    except ImportError:
        return MiniWebApp(db)


def get_test_client(app: Any) -> Any:
    if isinstance(app, MiniWebApp):
        return MiniTestClient(app)
    from fastapi.testclient import TestClient
    return TestClient(app)
