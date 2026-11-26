from datetime import datetime

from . import db


class Task:
    def __init__(self, description: str, completed: bool = False,
                 id: int | None = None, created_at: datetime | None = None):
        self.id = id                  # None until saved
        self.created_at = created_at  # None until saved
        self.completed = completed
        self.description = description

    def __repr__(self) -> str:
        return (f"Task(id={self.id}, completed={self.completed}, "
                f"created_at={self.created_at}, description={self.description!r})")

    @classmethod
    def _from_dict(cls, data: dict) -> "Task":
        return cls(data["description"], data["completed"], data["id"], data["created_at"])

    # ---- CREATE / UPDATE
    def save(self) -> "Task":
        """INSERT if the task is new (no id), otherwise UPDATE it.
        Returns self so you can chain: Task("x").save()"""
        if self.id is None:
            data = db.create_task(self.description, self.completed, self.created_at)
            self.id, self.created_at = data["id"], data["created_at"]
        elif not db.update_task(self.id, self.description, self.completed):
            raise LookupError(f"Task {self.id} no longer exists in the database")
        return self

    @classmethod
    def create(cls, description: str, completed: bool = False) -> "Task":
        """Shortcut: build and save in one step."""
        return cls(description, completed).save()

    # ---- READ
    @classmethod
    def get(cls, task_id: int) -> "Task | None":
        data = db.get_task(task_id)
        return cls._from_dict(data) if data else None

    @classmethod
    def all(cls, completed: bool | None = None) -> list["Task"]:
        return [cls._from_dict(d) for d in db.get_all_tasks(completed)]

    def refresh(self) -> "Task":
        """Reload this task's fields from the database."""
        data = db.get_task(self.id) if self.id is not None else None
        if data is None:
            raise LookupError(f"Task {self.id} not found in the database")
        self.created_at, self.completed, self.description = (
            data["created_at"], data["completed"], data["description"])
        return self

    # ---- DELETE
    def delete(self) -> bool:
        """Delete from the database. Returns True if a row was removed."""
        if self.id is None:
            return False
        removed = db.delete_task(self.id)
        self.id = None
        return removed
