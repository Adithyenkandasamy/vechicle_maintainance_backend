from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal
import uuid

class MaintenanceRecordBase(BaseModel):
    service_type: str
    mileage: int
    date: datetime
    notes: Optional[str] = None
    cost: Optional[Decimal] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    vehicle_id: uuid.UUID

class MaintenanceRecord(MaintenanceRecordBase):
    id: uuid.UUID
    vehicle_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class MaintenanceScheduleBase(BaseModel):
    service_type: str
    interval_months: Optional[int] = None
    interval_miles: Optional[int] = None

class MaintenanceScheduleCreate(MaintenanceScheduleBase):
    vehicle_id: uuid.UUID

class MaintenanceSchedule(MaintenanceScheduleBase):
    id: uuid.UUID
    vehicle_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True