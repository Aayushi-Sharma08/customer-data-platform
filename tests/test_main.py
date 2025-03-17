from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_main_app_running():
    response = client.get("/")
    assert response.status_code == 404  # root endpoint not defined, so expect 404
