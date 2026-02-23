import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "pontaj.db")


# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_FILE)


# -----------------------------
# INIT DB
# -----------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hours (
            id INTEGER PRIMARY KEY,
            overtime TEXT,
            permission TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY,
            prezente TEXT,
            concediu TEXT,
            wfh TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SAVE HOURS
# -----------------------------
def save_hours_to_db(overtime, permission):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM hours")
    cursor.execute(
        "INSERT INTO hours (overtime, permission) VALUES (?, ?)",
        (json.dumps(overtime), json.dumps(permission))
    )

    conn.commit()
    conn.close()


# -----------------------------
# SAVE CALENDAR
# -----------------------------
def save_calendar_to_db(prezente, concediu, wfh):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM calendar")
    cursor.execute(
        "INSERT INTO calendar (prezente, concediu, wfh) VALUES (?, ?, ?)",
        (
            json.dumps(prezente),
            json.dumps(concediu),
            json.dumps(wfh)
        )
    )

    conn.commit()
    conn.close()


# -----------------------------
# GET ALL DATA
# -----------------------------
def get_all_from_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT overtime, permission FROM hours LIMIT 1")
    hours_row = cursor.fetchone()

    cursor.execute("SELECT prezente, concediu, wfh FROM calendar LIMIT 1")
    calendar_row = cursor.fetchone()

    conn.close()

    hours_data = {"overtime": {}, "permission": {}}
    calendar_data = {"prezente": [], "concediu": [], "wfh": []}

    if hours_row:
        hours_data["overtime"] = json.loads(hours_row[0])
        hours_data["permission"] = json.loads(hours_row[1])

    if calendar_row:
        calendar_data["prezente"] = json.loads(calendar_row[0])
        calendar_data["concediu"] = json.loads(calendar_row[1])
        calendar_data["wfh"] = json.loads(calendar_row[2])

    return {
        "hours": hours_data,
        "calendar": calendar_data
    }