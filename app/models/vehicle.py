from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
from datetime import datetime

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    vin = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle")
    maintenance_schedules = relationship("MaintenanceSchedule", back_populates="vehicle")