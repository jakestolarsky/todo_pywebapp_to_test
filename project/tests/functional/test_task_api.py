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

def test_create_default_task(client):
    resp = client.post("/tasks/", json={"name": "Task"})
    data = resp.json()

    assert resp.status_code == 200
    assert "id" in data
    assert data["name"] == "Task"
    assert data["completed"] == False

def test_create_empty_json_task(client):
    resp = client.post("/tasks/", json={})

    assert resp.status_code == 422

def test_read_task(client):
    client.post("/tasks/", json={"name": "Task"})
    resp = client.get("/tasks/")
    data = resp.json()

    assert resp.status_code == 200
    assert data[0]["name"] == "Task"

def test_add_more_tasks(client):
    client.post("/tasks/", json={"name": "Task 1"})
    client.post("/tasks/", json={"name": "Task 2"})
    resp = client.get("/tasks/")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

def test_complete_task(client):
    client.post("/tasks/", json={"name": "Task"})
    put = client.put("/tasks/1/complete")
    resp = client.get("/tasks/")
    data = resp.json()

    assert put.status_code == 200
    assert data[0]["completed"] == True

def test_complete_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.put(f"/tasks/{nonexistent_task_id}/complete")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Task not found"}

def test_tasks_counter_empty(client):
    resp = client.get("/tasks/completed/count")
    data = resp.json()

    assert resp.status_code == 200
    assert data["completed_tasks_count"] == 0

def test_tasks_counter_more(client):
    client.post("/tasks/", json={"name": "Task 1", "completed": True})
    client.post("/tasks/", json={"name": "Task 2", "completed": False})
    resp = client.get("/tasks/completed/count")
    data = resp.json()

    assert resp.status_code == 200
    assert data["completed_tasks_count"] == 1

def test_change_name_task(client):
    client.post("/tasks/", json={"name": "Task"})
    task_id = client.get("/tasks/").json()[0]
    resp = client.put(f"/tasks/{task_id["id"]}/update", json={"name": "New Task"})
    data = resp.json()

    assert resp.status_code == 200
    assert data["name"] == "New Task"

def test_change_name_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.put(f"/tasks/{nonexistent_task_id}/update", json={"name": "Task"})

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Task not found"}

def test_delete_task(client):
    task_to_delete = client.post("/tasks/", json={"name": "Task"}).json()
    resp = client.delete(f"/tasks/{task_to_delete["id"]}")
    data = client.get("/tasks/").json()

    assert resp.status_code == 200
    assert len(data) == 0

def test_delete_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.delete(f"/tasks/{nonexistent_task_id}")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Task not found"}