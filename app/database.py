import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# -----------------------------
# MODELS
# -----------------------------
class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, index=True)
    overtime = Column(Text)
    permission = Column(Text)


class Calendar(Base):
    __tablename__ = "calendar"

    id = Column(Integer, primary_key=True, index=True)
    prezente = Column(Text)
    concediu = Column(Text)
    wfh = Column(Text)


# -----------------------------
# INIT DB
# -----------------------------
def init_db():
    Base.metadata.create_all(bind=engine)


# -----------------------------
# SAVE HOURS
# -----------------------------
def save_hours_to_db(overtime, permission):
    db = SessionLocal()
    db.query(Hours).delete()

    new_entry = Hours(
        overtime=json.dumps(overtime),
        permission=json.dumps(permission)
    )

    db.add(new_entry)
    db.commit()
    db.close()


# -----------------------------
# SAVE CALENDAR
# -----------------------------
def save_calendar_to_db(prezente, concediu, wfh):
    db = SessionLocal()
    db.query(Calendar).delete()

    new_entry = Calendar(
        prezente=json.dumps(prezente),
        concediu=json.dumps(concediu),
        wfh=json.dumps(wfh)
    )

    db.add(new_entry)
    db.commit()
    db.close()


# -----------------------------
# GET ALL DATA
# -----------------------------
def get_all_from_db():
    db = SessionLocal()

    hours_row = db.query(Hours).first()
    calendar_row = db.query(Calendar).first()

    db.close()

    hours_data = {"overtime": {}, "permission": {}}
    calendar_data = {"prezente": [], "concediu": [], "wfh": []}

    if hours_row:
        hours_data["overtime"] = json.loads(hours_row.overtime)
        hours_data["permission"] = json.loads(hours_row.permission)

    if calendar_row:
        calendar_data["prezente"] = json.loads(calendar_row.prezente)
        calendar_data["concediu"] = json.loads(calendar_row.concediu)
        calendar_data["wfh"] = json.loads(calendar_row.wfh)

    return {
        "hours": hours_data,
        "calendar": calendar_data
    }