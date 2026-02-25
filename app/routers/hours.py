from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.hours import HoursCreate, HoursResponse
from app.crud import hours as crud_hours
from app.core.security import get_current_user
router = APIRouter(
    prefix="/hours",
    tags=["Hours"]
)


@router.post("/", response_model=HoursResponse)
def create_hours(
    hours: HoursCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_hours.create_hours(db, hours)


@router.get("/", response_model=list[HoursResponse])
def read_hours(
    skip: int = 0,
    limit: int = 10,
    overtime: Optional[str] = None,
    overtime_gt: Optional[int] = None,
    overtime_lt: Optional[int] = None,
    permission: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_hours.get_hours(
        db=db,
        skip=skip,
        limit=limit,
        overtime=overtime,
        overtime_gt=overtime_gt,
        overtime_lt=overtime_lt,
        permission=permission,
        search=search,
        sort_by=sort_by,
        order=order
    )
