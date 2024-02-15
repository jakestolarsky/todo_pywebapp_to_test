import pytest
from pydantic import ValidationError

from app.schemas.task_schema import Task


def test_default_values():
    task = Task(name="Test task")

    assert task.id is None, "Expected task ID to be None by default"
    assert task.completed is False, "Expected task to be not completed (False) by default"

def test_custom_values():
    task = Task(id=1, name="Test Task", completed=False)

    assert task.id == 1, "Task ID should be equal to the custom value provided (1)"
    assert task.name == "Test Task", "Task name should match the custom value provided ('Test Task')"
    assert task.completed is False, "Task completion status should match the custom value provided (False)"

def test_invalid_values():
    with pytest.raises(ValidationError):
        Task(name=123, completed=123), "A ValidationError is expected when invalid data types are provided"

def test_empty_task():
    with pytest.raises(ValidationError):
        Task(), "A ValidationError is expected when required fields are missing"