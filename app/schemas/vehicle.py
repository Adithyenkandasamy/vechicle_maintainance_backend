from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class VehicleBase(BaseModel):
    name: str
    make: str
    model: str
    year: int
    vin: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True