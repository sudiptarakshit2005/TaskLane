
import sqlite3

DB_FILE = "tasklane.db"


def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = connect()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            person TEXT NOT NULL,
            status TEXT DEFAULT 'todo'
        )
        """
    )

    conn.commit()
    conn.close()


def add_task(title, person):
    conn = connect()

    conn.execute(
        "INSERT INTO tasks (title, person, status) VALUES (?, ?, ?)",
        (title, person, "todo")
    )

    conn.commit()
    conn.close()


def all_tasks():
    conn = connect()

    rows = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def move_task(task_id, status):
    if status not in ["todo", "doing", "done"]:
        return

    conn = connect()

    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = connect()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()
