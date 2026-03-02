from datetime import date
from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Hours(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, index=True)
    work_date = Column(Date, nullable=False)

    # tip zi
    permission = Column(Text)  # WFO, WFH, Vacation, Leave

    # overtime real numeric
    overtime_hours = Column(Integer, default=0)

    # leave in hours (optional)
    leave_hours = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
