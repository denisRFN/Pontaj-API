from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
import sqlite3
import json

app = FastAPI()

DB_FILE = "pontaj.db"


# -----------------------------
# DB INITIALIZATION
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
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


init_db()


# -----------------------------
# MODELS
# -----------------------------
class HoursData(BaseModel):
    overtime: Dict[str, float]
    permission: Dict[str, float]


class CalendarData(BaseModel):
    prezente: List[str]
    concediu: List[str]
    wfh: List[str]


# -----------------------------
# SAVE HOURS
# -----------------------------
@app.post("/save-hours")
def save_hours(data: HoursData):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM hours")
    cursor.execute(
        "INSERT INTO hours (overtime, permission) VALUES (?, ?)",
        (json.dumps(data.overtime), json.dumps(data.permission))
    )

    conn.commit()
    conn.close()

    return {"status": "hours saved"}


# -----------------------------
# SAVE CALENDAR
# -----------------------------
@app.post("/save-calendar")
def save_calendar(data: CalendarData):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM calendar")
    cursor.execute(
        "INSERT INTO calendar (prezente, concediu, wfh) VALUES (?, ?, ?)",
        (
            json.dumps(data.prezente),
            json.dumps(data.concediu),
            json.dumps(data.wfh)
        )
    )

    conn.commit()
    conn.close()

    return {"status": "calendar saved"}


# -----------------------------
# GET ALL DATA
# -----------------------------
@app.get("/all")
def get_all():
    conn = sqlite3.connect(DB_FILE)
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