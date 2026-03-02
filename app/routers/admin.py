from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.dependencies import require_admin
from app.models.hours import Hours
from app.models.hours import Hours

@router.get("/hours/{user_id}")
def get_hours_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Hours).filter(
        Hours.user_id == user_id
    ).all()
@router.get("/hours/{user_id}")
def get_hours_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Hours).filter(
        Hours.user_id == user_id
    ).all()
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).all()
