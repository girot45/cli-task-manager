import json
import os
import pprint
from typing import List

from task import Task


def get_tasks_slice(tasks: List[Task], start: int, end: int):
    mes = "q-Выйти"
    if start > 4:
        mes += " p-Назад"
    if len(tasks) > end:
        mes += " n-Дальше"
    mes += "\nВыберите действие: "
    return tasks[start:end:1], mes


class TaskManager:
    def __init__(self, storage_file: str = "db.json"):
        self.tasks: List[Task] = []
        self.storage_file = storage_file

    def add_task(
        self, title: str, description: str, category: str, due_date: str, priority: str
    ):
        id_ = self.get_new_task_id()
        task = Task(id_, title, description, category, due_date, priority)
        self.tasks.append(task)

    def load_tasks(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                pprint.pp(tasks_data, indent=4)
                self.tasks = [Task.from_dict(task) for task in tasks_data]
        except FileNotFoundError:
            with open(self.storage_file, "w", encoding="utf-8") as file:
                pass

    def save_tasks(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def get_all_tasks(self):
        return self.tasks

    def get_new_task_id(self):
        if len(self.tasks) == 0:
            return "1"
        return str(self.tasks[-1].id + 1)

    def delete_task(self, task_id: str):
        self.tasks.pop(int(task_id) - 1)
        self.__count_new_ids()
        return True

    def __count_new_ids(self):
        for ind, task in enumerate(self.tasks):
            task.id = ind + 1

    def search_tasks(
        self, keyword: str = "", category: str = "", status: str = ""
    ) -> List[Task]:
        return [
            task
            for task in self.tasks
            if (
                keyword.lower() in task.title.lower()
                or keyword.lower() in task.description.lower()
            )
            and (category == "" or task.category == category)
            and (status == "" or task.status == status)
        ]

    @staticmethod
    def show_tasks(tasks: List[Task]):
        if not len(tasks):
            os.system("cls")
            print("Нет задач")
            input("Нажмите enter, чтобы продолжить...")
            return
        start = 0
        end = 5
        choice = ""

        while choice != "q":
            os.system("cls")
            print("Постраничный вывод по 5 задач")
            input("Нажмите enter для просмотра...")
            while True:
                tasks_slice, mes = get_tasks_slice(tasks=tasks, start=start, end=end)
                for task in tasks_slice:
                    pprint.pp(task, indent=4)

                choice = input(mes)
                if choice.lower() == "n":
                    start += 5
                    end += 5
                elif choice.lower() == "p":
                    start -= 5
                    end -= 5
                elif choice.lower() == "q":
                    break
                else:
                    print("Некорректный выбор")

    def get_task_by_id(self, task_id: int):
        return self.tasks[task_id - 1]

    def edit_task(self, task_id: int, **kwargs):
        task: Task = self.get_task_by_id(task_id)
        task.update(**kwargs)
        print(task)

    def complete_task(self, task_id: int):
        task: Task = self.get_task_by_id(task_id)
        task.mark_as_done()
        print(task)
