from pydantic import BaseModel
from datetime import date

class HoursBase(BaseModel):
    work_date: date
    permission: str
    overtime_hours: int = 0
    leave_hours: int = 0

class HoursCreate(HoursBase):
    pass

class HoursResponse(HoursBase):
    id: int

    class Config:
        from_attributes = True
