import os
from datetime import datetime

from task_manager import TaskManager

CATEGORIES = {
    "1": "работа",
    "2": "личное",
    "3": "обучение",
}

PRIORITIES = {
    "1": "низкий",
    "2": "средний",
    "3": "высокий",
}


class CLI:
    def __init__(self, taskManager: TaskManager):
        self.taskManager = taskManager
        self.MENU_VARIANTS = {
            "1": self.display_tasks,
            "2": self.add_task,
            "3": self.edit_task,
            "4": self.delete_task,
            "5": self.find_task,
            "6": self.complete_task,
            "0": self.exit_from_app,
        }

    def start_app(self) -> None:
        self.taskManager.load_tasks()
        self.__run_menu()

    def __run_menu(self) -> None:
        while True:
            os.system("cls")
            choice = self.main_menu()
            os.system("cls")
            if choice == "0":
                self.exit_from_app()
                break
            self.MENU_VARIANTS[choice]()

    @staticmethod
    def main_menu() -> str:
        print("\nДобро пожаловать в Менеджер задач!")
        print("1. Просмотреть все задачи")
        print("2. Добавить новую задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Поиск задач")
        print("0. Выйти")
        return input("Выберите действие (1-6): ")

    def display_tasks(self) -> None:
        all_tasks = self.taskManager.get_all_tasks()
        self.taskManager.show_tasks(all_tasks)

    @staticmethod
    def __choose_parameter(parametrs: dict, message: str) -> str:
        while True:
            try:
                res = parametrs[input(message)]
                return res
            except KeyError:
                print("Неверный параметр. Попробуйте еще раз")

    def add_task(self) -> None:
        print("\nДобавление новой задачи:")
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        category = self.__choose_parameter(
            CATEGORIES,
            "Категории задач (работа, личное, обучение)\nВыберите категорию 1 2 3: ",
        )
        due_date = input("Введите срок выполнения (ГГГГ-ММ-ДД): ")
        priority = self.__choose_parameter(
            PRIORITIES,
            "Приоритеты (низкий, средний, высокий)\nВыберите приоритет 1 2 3: ",
        )
        self.taskManager.add_task(
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
        )

    def edit_task(self) -> None:
        choice = input(
            "Для изменения задачи, вам необходимо знать id.\n"
            "Если вы не знаете id, то сначала воспользуйтесь"
            "'поиском задачи' в главном меню\n1. Продолжить\n2. В главное меню\nВыберите действие (1-2):"
        )
        if choice == "2":
            return

        task_id = input("\nВведите ID задачи для редактирования: ")
        print("Оставьте поле пустым, если не хотите менять значение.")
        title = input("Новое название задачи: ")
        description = input("Новое описание задачи: ")
        category = self.__choose_parameter(
            CATEGORIES,
            "Категории задач (работа, личное, обучение)\nВыберите категорию 1 2 3: ",
        )
        due_date = self.get_date_from_user()
        priority = self.__choose_parameter(
            PRIORITIES,
            "Приоритеты (низкий, средний, высокий)\nВыберите приоритет 1 2 3: ",
        )
        self.taskManager.edit_task(
            task_id=task_id,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
        )

        input("Нажмите enter для просмотра...")

    @staticmethod
    def get_date_from_user() -> str:
        while True:
            try:
                due_date = input("Новый срок выполнения (ГГГГ-ММ-ДД): ")
                if due_date == "-1":
                    return
                return datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                print(
                    "Некорректный формат даты. Используйте формат ГГГГ-ММ-ДД. Или введите -1, чтобы выйти"
                )

    def delete_task(self) -> None:
        task_id = input("\nВведите ID задачи для удаления: ")
        self.taskManager.delete_task(task_id)
        print("Задача удалена")
        input("Нажмите enter для просмотра...")

    def find_task(self) -> None:
        print("\nПоиск задач:")
        keyword = input("Введите ключевое слово: ")
        category = input("Введите категорию (оставьте пустым для всех): ")
        status = input(
            "Введите статус (Не выполнена/Выполнена, оставьте пустым для всех): "
        )
        found_tasks = self.taskManager.search_tasks(
            keyword=keyword, category=category, status=status
        )
        self.taskManager.show_tasks(found_tasks)

    def complete_task(self):
        task_id = input("\nВведите ID задачи для редактирования: ")
        self.taskManager.complete_task(int(task_id))
        input("Нажмите enter для просмотра...")

    def exit_from_app(self):
        print("\nСпасибо за использование Менеджера задач! До свидания.")
        self.taskManager.save_tasks()
