from pydantic import BaseModel

class HoursBase(BaseModel):
    overtime: str
    permission: str

class HoursCreate(HoursBase):
    pass

class HoursResponse(HoursBase):
    id: int

    class Config:
        orm_mode = True
