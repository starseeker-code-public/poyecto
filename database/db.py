"""Low-level SQLite functions for the `tasks` table.

Every function opens its own short-lived connection, so there is no state to
manage. The table is created automatically the first time it is needed.
Rows are returned as plain dicts: {"id", "created_at", "completed", "description"}.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Default location: <project root>/tasks.db (next to main.py)
DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"


def set_db_path(path) -> None:
    """Use a different sqlite file (handy for tests). ':memory:' is NOT
    supported because every call opens a new connection; use a temp file."""
    global DB_PATH
    DB_PATH = Path(path)


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT    NOT NULL,
                completed   INTEGER NOT NULL DEFAULT 0,
                description TEXT    NOT NULL
            )
            """
        )
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "created_at": datetime.fromisoformat(row["created_at"]),
        "completed": bool(row["completed"]),
        "description": row["description"],
    }


# ---------------------------------------------------------------- CREATE
def create_task(description: str, completed: bool = False,
                created_at: datetime | None = None) -> dict:
    """Insert a task and return it (with its generated id)."""
    created_at = (created_at or datetime.now()).replace(microsecond=0)
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (created_at, completed, description) VALUES (?, ?, ?)",
            (created_at.isoformat(), int(completed), description),
        )
        task_id = cur.lastrowid
    return {
        "id": task_id,
        "created_at": created_at,
        "completed": completed,
        "description": description,
    }


# ------------------------------------------------------------------ READ
def get_task(task_id: int) -> dict | None:
    """Return the task with that id, or None if it doesn't exist."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _row_to_dict(row) if row else None


def get_all_tasks(completed: bool | None = None) -> list[dict]:
    """Return all tasks ordered by id. Pass completed=True/False to filter."""
    query, params = "SELECT * FROM tasks", ()
    if completed is not None:
        query += " WHERE completed = ?"
        params = (int(completed),)
    with _connect() as conn:
        rows = conn.execute(query + " ORDER BY id", params).fetchall()
    return [_row_to_dict(r) for r in rows]


# ---------------------------------------------------------------- UPDATE
def update_task(task_id: int, description: str | None = None,
                completed: bool | None = None) -> bool:
    """Update the given fields (those left as None are untouched).
    Returns True if the task exists, False if the id doesn't exist."""
    fields, params = [], []
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if completed is not None:
        fields.append("completed = ?")
        params.append(int(completed))
    if not fields:
        return get_task(task_id) is not None
    with _connect() as conn:
        cur = conn.execute(
            f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", (*params, task_id)
        )
        return cur.rowcount > 0


# ---------------------------------------------------------------- DELETE
def delete_task(task_id: int) -> bool:
    """Delete a task. Returns True if it existed, False otherwise."""
    with _connect() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cur.rowcount > 0
