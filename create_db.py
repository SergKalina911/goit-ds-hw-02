""" Скрипт створення таблиць """

import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Створення таблиці users з полями id, fullname та email
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
""")

# Створення таблиці status з полями id та name
cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE
);
""")

# Створення таблиці tasks з полями id, title, description, status_id та user_id с посиланням на
# таблиці status та users
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

# Заповнення статусів
cursor.executemany("INSERT OR IGNORE INTO status(name) VALUES (?)",
                   [('new',), ('in progress',), ('completed',)])

conn.commit()
conn.close()
