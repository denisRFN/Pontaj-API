from sqlalchemy.orm import Session
from app.models.calendar import Calendar
from typing import Optional
from sqlalchemy import or_

def get_calendar(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    prezente: Optional[str] = None,
    concediu: Optional[str] = None,
    wfh: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Calendar)

    if prezente:
        query = query.filter(Calendar.prezente == prezente)

    if concediu:
        query = query.filter(Calendar.concediu == concediu)

    if wfh:
        query = query.filter(Calendar.wfh == wfh)

    if search:
        query = query.filter(
            or_(
                Calendar.prezente.ilike(f"%{search}%"),
                Calendar.concediu.ilike(f"%{search}%"),
                Calendar.wfh.ilike(f"%{search}%")
            )
        )

    column = getattr(Calendar, sort_by, Calendar.id)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query.offset(skip).limit(limit).all()
