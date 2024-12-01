from typing import Optional


class Task:
    def __init__(
        self,
        id_: str,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: str,
        status: str = "Не выполнена",
    ):
        self.id = id_
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status  # Статус по умолчанию

    def __repr__(self):
        return (
            f"ID: {self.id}\nНазвание: {self.title}\nОписание: {self.description}\n"
            f"Категория: {self.category}\nСрок: {self.due_date}\nПриоритет: {self.priority}\n"
            f"Статус: {self.status}\n{'-' * 20}"
        )

    def mark_as_done(self):
        self.status = "Выполнена"

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
    ):
        if title:
            self.title = title
        if description:
            self.description = description
        if category:
            self.category = category
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        task = Task(
            id_=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )

        return task
