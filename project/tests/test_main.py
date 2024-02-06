from fastapi.responses import HTMLResponse
import httpx
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Jan!" in response.text