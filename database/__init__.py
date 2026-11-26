"""Tasks persistence package (SQLite).

    from database import Task
    t = Task.create("Buy milk")
    t.completed = True
    t.save()
    Task.all()
    t.delete()

The raw functions are also exposed in case you want them directly.
"""

from .db import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
    set_db_path,
    update_task,
)
from .task import Task

__all__ = [
    "Task",
    "create_task", "get_task", "get_all_tasks", "update_task", "delete_task",
    "set_db_path",
]
