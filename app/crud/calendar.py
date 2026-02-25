from sqlalchemy.orm import Session
from app.models.calendar import Calendar
from app.schemas.calendar import CalendarCreate

def create_calendar(db: Session, calendar: CalendarCreate):
    db_calendar = Calendar(**calendar.dict())
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar

def get_calendar(db: Session):
    return db.query(Calendar).all()
