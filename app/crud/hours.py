from sqlalchemy.orm import Session
from sqlalchemy import extract
from fastapi import HTTPException
from app.models.hours import Hours


# ==========================================
# 🔹 ANNUAL BALANCE (PER USER)
# ==========================================
def get_annual_balance(db: Session, user_id: int, year: int):

    records = db.query(Hours).filter(
        Hours.user_id == user_id,
        extract("year", Hours.work_date) == year
    ).all()

    total_overtime = sum(r.overtime_hours or 0 for r in records)
    total_leave = sum(r.leave_hours or 0 for r in records)

    overtime_balance = total_overtime - total_leave

    return {
        "total_overtime_hours": total_overtime,
        "total_leave_hours": total_leave,
        "overtime_balance_hours": overtime_balance
    }


# ==========================================
# 🔹 CREATE (PER USER)
# ==========================================
def create_hours(db: Session, hours, user_id: int):

    print("CREATING FOR USER:", user_id)  # 🔥 DEBUG

    existing = db.query(Hours).filter(
        Hours.user_id == user_id,
        Hours.work_date == hours.work_date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Pontaj deja înregistrat")

    db_hours = Hours(
        work_date=hours.work_date,
        permission=hours.permission,
        overtime_hours=hours.overtime_hours or 0,
        leave_hours=hours.leave_hours or 0,
        user_id=user_id
    )

    db.add(db_hours)
    db.commit()
    db.refresh(db_hours)

    return db_hours


# ==========================================
# 🔹 ADMIN: GET HOURS (OPTIONAL FILTER USER)
# ==========================================
def get_hours(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    user_id: int | None = None
):

    query = db.query(Hours)

    if user_id:
        query = query.filter(Hours.user_id == user_id)

    return query.order_by(Hours.work_date.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()
