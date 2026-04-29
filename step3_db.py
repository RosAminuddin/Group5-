import sqlite3
import os
import json
from datetime import datetime

from step1_scrap import scrap_data


# ---------------------------------
# BASE DIRECTORY (AUTO-DETECT FILE LOCATION)
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "output")
DB_NAME = os.path.join(DB_FOLDER, "pandemic_data.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pandemic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_db(data: dict) -> dict:
    json_data = json.dumps(data)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO pandemic (data) VALUES (?)",
        (json_data,)
    )

    conn.commit()
    record_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM pandemic WHERE id = ?",
        (record_id,)
    )

    record = cursor.fetchone()
    conn.close()

    return {
        "id": record["id"],
        "data": data,
        "created_at": record["created_at"]
    }


# -------------------
# MAIN PROGRAM (TEST)
# -------------------
if __name__ == "__main__":
    init_db()

    pandemic = scrap_data("Malaysia")
    record = save_db(pandemic)

    print(json.dumps(record, indent=2))