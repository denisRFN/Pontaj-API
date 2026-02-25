from pydantic import BaseModel

class CalendarBase(BaseModel):
    prezente: str
    concediu: str
    wfh: str

class CalendarCreate(CalendarBase):
    pass

class CalendarResponse(CalendarBase):
    id: int

    class Config:
        orm_mode = True
