import sqlite3

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            mood_tag TEXT,
            is_done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def add_task(title, category, mood_tag):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, category, mood_tag) VALUES (?, ?, ?)",
              (title, category, mood_tag))
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    res = c.fetchall()
    conn.close()
    return res


def get_tasks_by_categories(categories):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    placeholders = ",".join("?" * len(categories))
    c.execute(f"SELECT * FROM tasks WHERE category IN ({placeholders})", categories)
    res = c.fetchall()
    conn.close()
    return res


def mark_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
