""" Скрипт для заповнення бази даних випадковими даними з бібліотеки Faker """

import sqlite3
from faker import Faker
import random

fake = Faker()
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Користувачі
for _ in range(5):
    cursor.execute("INSERT INTO users(fullname, email) VALUES (?, ?)",
                   (fake.name(), fake.unique.email()))

# Завдання
user_ids = [row[0] for row in cursor.execute("SELECT id FROM users")]
status_ids = [row[0] for row in cursor.execute("SELECT id FROM status")]

for _ in range(10):
    cursor.execute("INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                   (fake.sentence(nb_words=4),
                    fake.text(),
                    random.choice(status_ids),
                    random.choice(user_ids)))

conn.commit()
conn.close()
