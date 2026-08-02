""" 
Необов'язковий скрипт для автоматичного запуску create_db.py, seed.py та виконання SQL-запитів з queries.sql.
"""

import os
import sqlite3
import subprocess
import sys
from tabulate import tabulate

DB_NAME = "tasks.db"
QUERIES_FILE = "queries.sql"

def run_python_script(script_name):
    """Запускає Python-скрипт у тому ж середовищі."""
    print(f"\n▶ Запуск {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {script_name} виконано успішно.")
    else:
        print(f"❌ Помилка у {script_name}:\n{result.stderr}")

def run_queries():
    """Виконує SQL-запити з файлу queries.sql та виводить результати."""
    if not os.path.exists(DB_NAME):
        print(f"⚠️ База даних '{DB_NAME}' не знайдена.")
        return

    if not os.path.exists(QUERIES_FILE):
        print(f"⚠️ Файл '{QUERIES_FILE}' не знайдено.")
        return

    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        print("\n▶ Виконання SQL-запитів...\n")
        try:
            with open(QUERIES_FILE, "r", encoding="utf-8") as f:
                sql_lines = f.readlines()

            queries = []
            current_query = []
            for line in sql_lines:
                if line.strip().startswith("--"):
                    if current_query:
                        queries.append(current_query)
                        current_query = []
                    queries.append([line.strip()])
                else:
                    current_query.append(line)
                    if ";" in line:
                        queries.append(current_query)
                        current_query = []
            if current_query:
                queries.append(current_query)

            for q in queries:
                if all(line.startswith("--") for line in q):
                    print("\n".join(q))
                else:
                    sql = "".join(q).strip()
                    if not sql:
                        continue
                    print(f"\nSQL: {sql}")
                    try:
                        cur.execute(sql)
                        rows = cur.fetchall()
                        col_names = [desc[0] for desc in cur.description] if cur.description else []
                        if rows:
                            print(tabulate(rows, headers=col_names, tablefmt="grid"))
                        else:
                            print("⚠️ Запит не повернув результатів.")
                    except Exception as e:
                        print(f"❌ Помилка виконання: {e}")
        except Exception as e:
            print(f"❌ Помилка читання файлу: {e}")

if __name__ == "__main__":
    run_python_script("create_db.py")
    run_python_script("seed.py")
    run_queries()
