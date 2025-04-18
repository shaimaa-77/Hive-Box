from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_app_version():
    # Test version
    respond = client.get("/version")
    assert respond.status_code == 200
    assert "version" in respond.json()


def test_app_temperature():
    # Test temperature
    respond = client.get("/temperature")
    assert respond.status_code == 200
    assert "average_temperatures" in respond.json()
