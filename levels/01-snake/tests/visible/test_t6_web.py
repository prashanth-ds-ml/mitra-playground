from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_page_has_a_canvas_and_calls_the_api():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert '<canvas id="board"' in html
    assert "/api/state" in html and "/api/step" in html and "/api/turn" in html
    assert "ArrowUp" in html


def test_server_uses_the_api():
    src = (ROOT / "serve.py").read_text(encoding="utf-8")
    assert "http.server" in src
    assert "handle" in src and "8000" in src
