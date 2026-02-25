from sqlalchemy import Column, Integer, Text
from app.database import Base

class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, index=True)
    overtime = Column(Text)
    permission = Column(Text)
