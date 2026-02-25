from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.calendar import CalendarCreate, CalendarResponse
from app.crud import calendar as crud_calendar

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/", response_model=CalendarResponse)
def create_calendar(calendar: CalendarCreate, db: Session = Depends(get_db)):
    return crud_calendar.create_calendar(db, calendar)

@router.get("/", response_model=list[CalendarResponse])
def read_calendar(db: Session = Depends(get_db)):
    return crud_calendar.get_calendar(db)
