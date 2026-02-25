from sqlalchemy.orm import Session
from app.models.hours import Hours
from typing import Optional

def get_hours(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    overtime: Optional[str] = None,
    permission: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Hours)

    # Filtering
    if overtime:
        query = query.filter(Hours.overtime == overtime)

    if permission:
        query = query.filter(Hours.permission == permission)

    # Sorting
    column = getattr(Hours, sort_by, Hours.id)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # Pagination
    return query.offset(skip).limit(limit).all()
