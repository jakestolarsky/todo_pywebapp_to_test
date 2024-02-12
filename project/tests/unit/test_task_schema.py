import pytest
from pydantic import ValidationError

from app.schemas.task_schema import Task


def test_default_values():
    task = Task(name="Test task")

    assert task.id is None
    assert task.completed is False

def test_custom_values():
    task = Task(id=1, name="Test Task", completed=False)

    assert task.id == 1
    assert task.name == "Test Task"
    assert task.completed is False

def test_invalid_values():
    with pytest.raises(ValidationError):
        Task(name=123, completed=123)

def test_empty_task():
    with pytest.raises(ValidationError):
        Task()