from datetime import date
from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, index=True)
    work_date = Column(Date, nullable=False)

    permission = Column(Text)  # WFO, WFH, Vacation, Leave

    # overtime real 
    overtime_hours = Column(Integer, default=0)

    # leave in hours
    leave_hours = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="hours")
