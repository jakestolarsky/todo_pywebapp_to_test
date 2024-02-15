import pytest
from pydantic import ValidationError

from app.models.task_model import tasks
from app.schemas.task_schema import Task


@pytest.fixture(autouse=True)
def clear_tasks_before_tests():
    tasks.clear()
    yield

def test_add_task_to_list():
    task = Task(name="Test task")
    tasks.append(task)

    assert len(tasks) == 1, "The tasks list should contain exactly one task after adding a task."
    assert tasks[0].name == "Test task", "The name of the task in the list should match 'Test task'."

def test_remove_task_from_list():
    task = Task(name="Test task")
    tasks.append(task)
    tasks.remove(task)

    assert len(tasks) == 0, "The tasks list should be empty after removing the task."

def test_find_task_by_id():
    tasks.append(Task(id=1, name="Task 1"))
    tasks.append(Task(id=2, name="Task 2"))

    find_task = next((task for task in tasks if task.id == 1), None)

    assert find_task is not None, "A task with ID 1 should be found in the list."
    assert find_task.name == "Task 1", "The name of the found task should be 'Task 1'."

def test_empty_task_in_list():
    with pytest.raises(ValidationError):
        tasks.append(Task()), "Adding an empty task should raise a ValidationError due to missing required fields."
