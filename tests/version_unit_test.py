from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
