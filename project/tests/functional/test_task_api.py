import pytest
from fastapi.testclient import TestClient

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

    assert resp.status_code == 200, "Main page should load with status code 200."

def test_create_default_task(client):
    resp = client.post("/tasks/", json={"name": "Task"})
    data = resp.json()

    assert resp.status_code == 200, "Creating a default task should succeed with status code 200."
    assert "id" in data, "Response should include an 'id' for the created task."
    assert data["name"] == "Task", "The created task's name should be 'Task'."
    assert data["completed"] == False, "The created task should be marked as not completed by default."

def test_create_empty_json_task(client):
    resp = client.post("/tasks/", json={})

    assert resp.status_code == 422, "Creating a task with empty JSON should fail with status code 422."

def test_read_task(client):
    client.post("/tasks/", json={"name": "Task"})
    resp = client.get("/tasks/")
    data = resp.json()

    assert resp.status_code == 200, "Reading tasks should succeed with status code 200."
    assert data[0]["name"] == "Task", "The task read back should have the name 'Task'."

def test_add_more_tasks(client):
    client.post("/tasks/", json={"name": "Task 1"})
    client.post("/tasks/", json={"name": "Task 2"})
    resp = client.get("/tasks/")
    data = resp.json()

    assert resp.status_code == 200, "Adding tasks should succeed with status code 200."
    assert len(data) == 2, "There should be 2 tasks in the list after adding."
    assert data[0]["id"] == 1, "The first task should have ID 1."
    assert data[1]["id"] == 2, "The second task should have ID 2."

def test_complete_task(client):
    client.post("/tasks/", json={"name": "Task"})
    put = client.put("/tasks/1/complete")
    resp = client.get("/tasks/")
    data = resp.json()

    assert put.status_code == 200, "Completing a task should succeed with status code 200."
    assert data[0]["completed"] == True, "The task should be marked as completed."

def test_complete_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.put(f"/tasks/{nonexistent_task_id}/complete")

    assert resp.status_code == 404, "Attempting to complete a nonexistent task should fail with status code 404."
    assert resp.json() == {"detail": "Task not found"}, "The error detail should indicate the task was not found."

def test_tasks_counter_empty(client):
    resp = client.get("/tasks/completed/count")
    data = resp.json()

    assert resp.status_code == 200, "Request for count of completed tasks should succeed with status code 200."
    assert data["completed_tasks_count"] == 0, "The count of completed tasks should be 0 when none are completed."

def test_tasks_counter_more(client):
    client.post("/tasks/", json={"name": "Task 1", "completed": True})
    client.post("/tasks/", json={"name": "Task 2", "completed": False})
    resp = client.get("/tasks/completed/count")
    data = resp.json()

    assert resp.status_code == 200, "Request for count of completed tasks should succeed with status code 200."
    assert data["completed_tasks_count"] == 1, "The count of completed tasks should be 1."

def test_change_name_task(client):
    client.post("/tasks/", json={"name": "Task"})
    resp = client.put("/tasks/1/update", json={"name": "New Task"})
    data = resp.json()

    assert resp.status_code == 200, "Changing a task's name should succeed with status code 200."
    assert data["name"] == "New Task", "The task's new name should be 'New Task'."

def test_change_name_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.put(f"/tasks/{nonexistent_task_id}/update", json={"name": "Task"})

    assert resp.status_code == 404, "Attempting to change the name of a nonexistent task should fail with status code 404."
    assert resp.json() == {"detail": "Task not found"}, "The error detail should indicate the task was not found."

def test_delete_task(client):
    client.post("/tasks/", json={"name": "Task"}).json()
    resp = client.delete("/tasks/1")
    data = client.get("/tasks/").json()

    assert resp.status_code == 200, "Deleting a task should succeed with status code 200."
    assert len(data) == 0, "The tasks list should be empty after deleting the task."

def test_delete_nonexistent_task(client):
    nonexistent_task_id = 9999
    resp = client.delete(f"/tasks/{nonexistent_task_id}")

    assert resp.status_code == 404, "Attempting to delete a nonexistent task should fail with status code 404."
    assert resp.json() == {"detail": "Task not found"}, "The error detail should indicate the task was not found."
