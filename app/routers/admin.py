from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.models.user import User
from app.models.hours import Hours
from app.core.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# 🔹 GET ALL USERS
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).all()


# 🔹 GET USER HOURS
@router.get("/hours/{user_id}")
def get_hours_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Hours).filter(
        Hours.user_id == user_id
    ).all()

@router.get("/dashboard/{year}")
def admin_dashboard(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    results = (
        db.query(
            User.id,
            User.username,
            func.count(Hours.id).label("total_days"),
            func.coalesce(func.sum(Hours.overtime_hours), 0).label("total_overtime"),
            func.coalesce(func.sum(Hours.leave_hours), 0).label("total_leave"),
        )
        .outerjoin(Hours, Hours.user_id == User.id)
        .filter(extract("year", Hours.work_date) == year)
        .group_by(User.id)
        .all()
    )

    permission_stats = (
        db.query(
            User.id,
            User.username,
            Hours.permission,
            func.count(Hours.id).label("count")
        )
        .join(Hours, Hours.user_id == User.id)
        .filter(extract("year", Hours.work_date) == year)
        .group_by(User.id, Hours.permission)
        .all()
    )

    users_data = {}

    for r in results:
        users_data[r.id] = {
            "user_id": r.id,
            "username": r.username,
            "total_days": r.total_days,
            "total_overtime": r.total_overtime,
            "total_leave": r.total_leave,
            "balance": r.total_overtime - r.total_leave,
            "permissions": {
                "WFO": 0,
                "WFH": 0,
                "Vacation": 0
            }
        }

    for p in permission_stats:
        if p.id in users_data:
            users_data[p.id]["permissions"][p.permission] = p.count

    return list(users_data.values())

# 🔹 USERS SUMMARY BY YEAR
@router.get("/users-summary")
def get_users_summary(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    results = (
        db.query(
            User.id,
            User.username,
            func.coalesce(func.sum(Hours.overtime_hours), 0).label("total_overtime"),
            func.coalesce(func.sum(Hours.leave_hours), 0).label("total_leave"),
        )
        .outerjoin(Hours, Hours.user_id == User.id)
        .group_by(User.id)
        .all()
    )

    response = []
    for r in results:
        response.append({
            "user_id": r.id,
            "username": r.username,
            "total_overtime": r.total_overtime,
            "total_leave": r.total_leave,
            "balance": r.total_overtime - r.total_leave
        })

    return response
