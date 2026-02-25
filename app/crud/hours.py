from sqlalchemy.orm import Session
from app.models.hours import Hours
from app.schemas.hours import HoursCreate

def create_hours(db: Session, hours: HoursCreate):
    db_hours = Hours(**hours.dict())
    db.add(db_hours)
    db.commit()
    db.refresh(db_hours)
    return db_hours

def get_hours(db: Session):
    return db.query(Hours).all()
