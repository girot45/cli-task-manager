import os

from cli import CLI
from task_manager import TaskManager

cli = CLI(TaskManager())

try:
    cli.start_app()
except KeyboardInterrupt:
    os.system("cls")
    cli.exit_from_app()
