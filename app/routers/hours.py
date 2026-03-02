from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Optional

from app.database import get_db
from app.schemas.hours import HoursCreate, HoursResponse
from app.crud import hours as crud_hours
from app.core.security import get_current_user
from app.core.dependencies import require_admin
from app.models.user import User
from app.models.hours import Hours


router = APIRouter(
    prefix="/hours",
    tags=["Hours"]
)


# ===============================
# 🔹 ANNUAL BALANCE (USER ONLY)
# ===============================
@router.get("/balance/{year}")
def get_balance(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_hours.get_annual_balance(
        db,
        current_user.id,
        year
    )


# ===============================
# 🔹 MY HOURS (USER ONLY)
# ===============================
@router.get("/me", response_model=list[HoursResponse])
def read_my_hours(
    month: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Hours).filter(
        Hours.user_id == current_user.id
    )

    if month and year:
        query = query.filter(
            extract("month", Hours.work_date) == month,
            extract("year", Hours.work_date) == year
        )

    return query.all()


# ===============================
# 🔹 CREATE (USER ONLY)
# ===============================
@router.post("/", response_model=HoursResponse)
def create_hours(
    hours: HoursCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_hours.create_hours(db, hours, current_user.id)


# ===============================
# 🔹 READ ALL HOURS (ADMIN ONLY)
# ===============================
@router.get("/", response_model=list[HoursResponse])
def read_all_hours(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,  # 🔥 optional filter
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return crud_hours.get_hours(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id
    )


# ===============================
# 🔹 UPDATE (ONLY OWN RECORDS)
# ===============================
@router.put("/{hour_id}", response_model=HoursResponse)
def update_hour(
    hour_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hour = db.query(Hours).filter(
        Hours.id == hour_id,
        Hours.user_id == current_user.id
    ).first()

    if not hour:
        raise HTTPException(status_code=404, detail="Not found")

    hour.permission = data.get("permission", hour.permission)
    hour.overtime_hours = data.get("overtime_hours", hour.overtime_hours)
    hour.leave_hours = data.get("leave_hours", hour.leave_hours)

    db.commit()
    db.refresh(hour)

    return hour


# ===============================
# 🔹 DELETE (ADMIN ONLY)
# ===============================
@router.delete("/{hour_id}")
def delete_hour(
    hour_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    hour = db.query(Hours).filter(Hours.id == hour_id).first()

    if not hour:
        raise HTTPException(status_code=404, detail="Hour not found")

    db.delete(hour)
    db.commit()

    return {"message": "Deleted successfully"}
