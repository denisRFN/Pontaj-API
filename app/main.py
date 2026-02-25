from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.models.hours import Hours
from app.models.calendar import Calendar
app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/hours")
def create_hours(overtime: str, permission: str, db: Session = Depends(get_db)):
    new_entry = Hours(
        overtime=overtime,
        permission=permission
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@app.post("/calendar")
def create_calendar(prezente: str, concediu: str, wfh: str, db: Session = Depends(get_db)):
    new_entry = Calendar(
        prezente=prezente,
        concediu=concediu,
        wfh=wfh
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry
