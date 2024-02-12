import pytest
from fastapi.testclient import TestClient
from fastapi.responses import HTMLResponse

from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks_before_tests():
    from app.models.task_model import tasks
    tasks.clear()

def test_main_page_loaded(client):
    resp = client.get("/")
    assert resp.status_code == 200

def test_create_task(client):
    response = client.post("/tasks/", json={"name": "Task", "completed": False})
    assert response.status_code == 200