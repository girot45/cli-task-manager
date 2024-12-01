import pytest
import os
import json
from task import Task
from task_manager import (
    TaskManager,
    get_tasks_slice,
)  # Замените на правильный путь до вашего модуля


@pytest.fixture
def task_manager():
    """Фикстура для создания временного менеджера задач."""
    storage_file = "test_db.json"
    manager = TaskManager(storage_file=storage_file)
    yield manager
    if os.path.exists(storage_file):
        os.remove(storage_file)


@pytest.fixture
def sample_tasks():
    """Фикстура с примерными задачами."""
    return [
        Task(
            id_="1",
            title="Task 1",
            description="Description 1",
            category="работа",
            due_date="2024-12-01",
            priority="высокий",
        ),
        Task(
            id_="2",
            title="Task 2",
            description="Description 2",
            category="личное",
            due_date="2024-12-02",
            priority="средний",
        ),
        Task(
            id_="3",
            title="Task 3",
            description="Description 3",
            category="работа",
            due_date="2024-12-03",
            priority="низкий",
        ),
    ]


def test_add_task(task_manager):
    task_manager.add_task("New Task", "Description", "работа", "2024-12-31", "высокий")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "New Task"


def test_load_and_save_tasks(task_manager, sample_tasks):
    # Сохранение задач
    task_manager.tasks = sample_tasks
    task_manager.save_tasks()
    assert os.path.exists(task_manager.storage_file)

    # Загрузка задач
    task_manager.tasks = []
    task_manager.load_tasks()
    assert len(task_manager.tasks) == len(sample_tasks)
    assert task_manager.tasks[0].title == "Task 1"


def test_delete_task(task_manager, sample_tasks):
    task_manager.tasks = sample_tasks
    task_manager.delete_task("1")
    assert len(task_manager.tasks) == 2
    assert task_manager.tasks[0].id == 1  # Проверка обновления ID


def test_get_all_tasks(task_manager, sample_tasks):
    task_manager.tasks = sample_tasks
    all_tasks = task_manager.get_all_tasks()
    assert all_tasks == sample_tasks


def test_search_tasks(task_manager, sample_tasks):
    task_manager.tasks = sample_tasks
    result = task_manager.search_tasks(keyword="Task 1", category="работа")
    assert len(result) == 1
    assert result[0].title == "Task 1"


def test_edit_task(task_manager, sample_tasks):
    task_manager.tasks = sample_tasks
    task_manager.edit_task(1, title="Updated Task")
    assert task_manager.tasks[0].title == "Updated Task"


def test_complete_task(task_manager, sample_tasks):
    task_manager.tasks = sample_tasks
    task_manager.complete_task(1)
    assert task_manager.tasks[0].status == "Выполнена"


def test_get_tasks_slice(sample_tasks):
    tasks_slice, mes = get_tasks_slice(sample_tasks, 0, 2)
    assert len(tasks_slice) == 2
    assert mes.startswith("q-Выйти")
