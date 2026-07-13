from fastapi.testclient import TestClient
from helm import __version__
from helm.main import app

client = TestClient(app)


def test_health_reports_only_api_liveness(monkeypatch) -> None:
    monkeypatch.setenv("HELM_ENVIRONMENT", "test")
    from helm.config import get_settings

    get_settings.cache_clear()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "helm-api",
        "version": __version__,
        "environment": "test",
    }


def test_version_matches_openapi_version() -> None:
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "service": "helm-api",
        "version": app.version,
        "runtimes": {
            "hermes": "not-configured",
            "vibe": "not-configured",
        },
    }
