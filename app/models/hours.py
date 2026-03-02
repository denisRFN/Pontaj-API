from sqlalchemy import Column, Integer, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, index=True)

    overtime = Column(Text)
    permission = Column(Text)

    work_date = Column(Date, default=date.today)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="hours")
