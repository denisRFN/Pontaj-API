from pydantic import BaseModel
from datetime import date

class HoursBase(BaseModel):
    overtime: str
    permission: str

class HoursCreate(HoursBase):
    pass

class HoursResponse(HoursBase):
    id: int
    work_date: date

    class Config:
        orm_mode = True
