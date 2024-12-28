from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
from datetime import datetime

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = Column(String, ForeignKey("vehicles.id"))
    service_type = Column(String)
    mileage = Column(Integer)
    date = Column(DateTime)
    notes = Column(String, nullable=True)
    cost = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="maintenance_records")

class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = Column(String, ForeignKey("vehicles.id"))
    service_type = Column(String)
    interval_months = Column(Integer, nullable=True)
    interval_miles = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="maintenance_schedules")
