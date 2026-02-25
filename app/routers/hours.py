from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.hours import HoursCreate, HoursResponse
from app.crud import hours as crud_hours

router = APIRouter(prefix="/hours", tags=["Hours"])

@router.post("/", response_model=HoursResponse)
def create_hours(hours: HoursCreate, db: Session = Depends(get_db)):
    return crud_hours.create_hours(db, hours)

@router.get("/", response_model=list[HoursResponse])
def read_hours(db: Session = Depends(get_db)):
    return crud_hours.get_hours(db)
