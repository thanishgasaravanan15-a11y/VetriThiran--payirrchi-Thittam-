from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_demo_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    # The generator is created at import time, so instantiate a fresh one through
    # a direct route dependency replacement for a deterministic test.
    from backend import routes
    from backend.services.ai_generator import GeminiDocumentGenerator

    old = routes.generator
    routes.generator = GeminiDocumentGenerator()
    try:
        response = client.post(
            "/generate",
            json={
                "document_type": "General Agreement",
                "parties": "Alice, Bob",
                "terms": "Payment on delivery; Confidentiality",
                "dates": "September 27, 2026",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["demo_mode"] is True
        assert "GENERAL AGREEMENT" in data["content"]
    finally:
        routes.generator = old
