from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

from app.database import (
    init_db,
    save_hours_to_db,
    save_calendar_to_db,
    get_all_from_db
)

app = FastAPI(title="Pontaj API")

# Initialize PostgreSQL tables
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
# ROOT + HEALTH
# -----------------------------
@app.get("/")
def root():
    return {"status": "Pontaj API running"}


@app.get("/health")
def health():
    return {"healthy": True}


# -----------------------------
# SAVE HOURS
# -----------------------------
@app.post("/save-hours")
def save_hours(data: HoursData):
    save_hours_to_db(data.overtime, data.permission)
    return {"status": "hours saved"}


# -----------------------------
# SAVE CALENDAR
# -----------------------------
@app.post("/save-calendar")
def save_calendar(data: CalendarData):
    save_calendar_to_db(data.prezente, data.concediu, data.wfh)
    return {"status": "calendar saved"}


# -----------------------------
# GET ALL DATA
# -----------------------------
@app.get("/all")
def get_all():
    return get_all_from_db()