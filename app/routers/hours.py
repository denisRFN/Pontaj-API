from typing import Optional

@router.get("/", response_model=list[HoursResponse])
def read_hours(
    skip: int = 0,
    limit: int = 10,
    overtime: Optional[str] = None,
    permission: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return crud_hours.get_hours(
        db=db,
        skip=skip,
        limit=limit,
        overtime=overtime,
        permission=permission,
        sort_by=sort_by,
        order=order
    )
