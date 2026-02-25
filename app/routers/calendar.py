from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.calendar import CalendarCreate, CalendarResponse
from app.crud import calendar as crud_calendar
from app.core.security import get_current_user
router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)


@router.post("/", response_model=CalendarResponse)
def create_calendar(
    calendar: CalendarCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_calendar.create_calendar(db, calendar)


@router.get("/", response_model=list[CalendarResponse])
def read_calendar(
    skip: int = 0,
    limit: int = 10,
    prezente: Optional[str] = None,
    concediu: Optional[str] = None,
    wfh: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_calendar.get_calendar(
        db=db,
        skip=skip,
        limit=limit,
        prezente=prezente,
        concediu=concediu,
        wfh=wfh,
        search=search,
        sort_by=sort_by,
        order=order
    )
