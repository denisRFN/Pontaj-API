from sqlalchemy.orm import Session
from app.models.hours import Hours
from typing import Optional
from sqlalchemy import or_
from datetime import date
from app.schemas.hours import HoursCreate
from fastapi import HTTPException
def create_hours(db: Session, hours: HoursCreate, user_id: int):

    existing = db.query(Hours).filter(
        Hours.user_id == user_id,
        Hours.work_date == hours.work_date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Pontaj deja înregistrat pentru această zi"
        )

    db_hours = Hours(
        overtime=hours.overtime,
        permission=hours.permission,
        user_id=user_id,
        work_date=hours.work_date
    )

    db.add(db_hours)
    db.commit()
    db.refresh(db_hours)
    return db_hours
    
def get_hours(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    overtime: Optional[str] = None,
    overtime_gt: Optional[int] = None,
    overtime_lt: Optional[int] = None,
    permission: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Hours)

    # Exact filtering
    if overtime:
        query = query.filter(Hours.overtime == overtime)

    if permission:
        query = query.filter(Hours.permission == permission)

    # Numeric comparators (convert string to int safely)
    if overtime_gt is not None:
        query = query.filter(Hours.overtime.cast(Integer) > overtime_gt)

    if overtime_lt is not None:
        query = query.filter(Hours.overtime.cast(Integer) < overtime_lt)

    # Search (LIKE)
    if search:
        query = query.filter(
            or_(
                Hours.overtime.ilike(f"%{search}%"),
                Hours.permission.ilike(f"%{search}%")
            )
        )

    # Sorting
    column = getattr(Hours, sort_by, Hours.id)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # Pagination
    return query.offset(skip).limit(limit).all()
