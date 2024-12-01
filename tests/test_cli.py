from unittest.mock import MagicMock, patch

import pytest

from cli import CLI
from task_manager import TaskManager


@pytest.fixture
def mock_task_manager():
    """Фикстура для создания мока TaskManager."""
    manager = MagicMock(TaskManager)
    manager.get_all_tasks.return_value = []
    return manager


@pytest.fixture
def cli(mock_task_manager):
    """Фикстура для создания экземпляра CLI с мокнутым TaskManager."""
    return CLI(taskManager=mock_task_manager)


def test_main_menu(cli):
    with patch("builtins.input", return_value="0"):
        assert cli.main_menu() == "0"


def test_display_tasks(cli, mock_task_manager):
    cli.display_tasks()
    mock_task_manager.get_all_tasks.assert_called_once()
    mock_task_manager.show_tasks.assert_called_once_with([])


def test_add_task(cli, mock_task_manager):
    inputs = ["Задача 1", "Описание 1", "1", "2024-12-31", "3"]
    with patch("builtins.input", side_effect=inputs):
        cli.add_task()
    mock_task_manager.add_task.assert_called_once_with(
        title="Задача 1",
        description="Описание 1",
        category="работа",
        due_date="2024-12-31",
        priority="высокий",
    )


def test_delete_task(cli, mock_task_manager):
    with patch("builtins.input", return_value="1"):
        cli.delete_task()
    mock_task_manager.delete_task.assert_called_once_with("1")


def test_find_task(cli, mock_task_manager):
    inputs = ["ключевое слово", "работа", "Не выполнена"]
    with patch("builtins.input", side_effect=inputs):
        cli.find_task()
    mock_task_manager.search_tasks.assert_called_once_with(
        keyword="ключевое слово",
        category="работа",
        status="Не выполнена",
    )


def test_complete_task(cli, mock_task_manager):
    with patch("builtins.input", return_value="1"):
        cli.complete_task()
    mock_task_manager.complete_task.assert_called_once_with(1)


def test_exit_from_app(cli, mock_task_manager):
    with patch("builtins.input", return_value="0"):
        cli.exit_from_app()
    mock_task_manager.save_tasks.assert_called_once()
