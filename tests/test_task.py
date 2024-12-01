import pytest
from task import Task


def test_task_initialization():
    task = Task(
        id_="1",
        title="Test Task",
        description="Test Description",
        category="работа",
        due_date="2024-12-31",
        priority="высокий",
    )
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.category == "работа"
    assert task.due_date == "2024-12-31"
    assert task.priority == "высокий"
    assert task.status == "Не выполнена"


def test_mark_as_done():
    task = Task(
        id_="2",
        title="Another Task",
        description="Another Description",
        category="Personal",
        due_date="2024-11-30",
        priority="средний",
    )
    task.mark_as_done()
    assert task.status == "Выполнена"


def test_update_task():
    task = Task(
        id_="3",
        title="Old Task",
        description="Old Description",
        category="Work",
        due_date="2024-10-01",
        priority="низкий",
    )
    task.update(
        title="Updated Task",
        description="Updated Description",
        category="Updated Category",
        due_date="2024-12-01",
        priority="высокий",
    )
    assert task.title == "Updated Task"
    assert task.description == "Updated Description"
    assert task.category == "Updated Category"
    assert task.due_date == "2024-12-01"
    assert task.priority == "высокий"


def test_to_dict():
    task = Task(
        id_="4",
        title="Dict Task",
        description="To Dict",
        category="работа",
        due_date="2024-09-01",
        priority="средний",
    )
    task_dict = task.to_dict()
    expected_dict = {
        "id": "4",
        "title": "Dict Task",
        "description": "To Dict",
        "category": "работа",
        "due_date": "2024-09-01",
        "priority": "средний",
        "status": "Не выполнена",
    }
    assert task_dict == expected_dict


def test_from_dict():
    data = {
        "id": "5",
        "title": "From Dict Task",
        "description": "From Dict Description",
        "category": "обучение",
        "due_date": "2024-10-15",
        "priority": "низкий",
        "status": "Не выполнена",
    }
    task = Task.from_dict(data)
    assert task.id == "5"
    assert task.title == "From Dict Task"
    assert task.description == "From Dict Description"
    assert task.category == "обучение"
    assert task.due_date == "2024-10-15"
    assert task.priority == "низкий"
    assert task.status == "Не выполнена"
