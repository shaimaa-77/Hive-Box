from fastapi.testclient import TestClient
from main import app
import httpx
client = TestClient(app)


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
    assert response.json()["version"] == app.version


