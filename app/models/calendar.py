from sqlalchemy import Column, Integer, Text
from app.database import Base

class Calendar(Base):
    __tablename__ = "calendar"

    id = Column(Integer, primary_key=True, index=True)
    prezente = Column(Text)
    concediu = Column(Text)
    wfh = Column(Text)
