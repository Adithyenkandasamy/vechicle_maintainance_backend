from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.vehicle import Vehicle
from ..schemas.vehicle import VehicleCreate, VehicleUpdate, Vehicle as VehicleSchema
from ..utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[VehicleSchema])
async def get_vehicles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Vehicle).filter(Vehicle.user_id == current_user.id).all()

@router.post("/", response_model=VehicleSchema)
async def create_vehicle(
    vehicle: VehicleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_vehicle = Vehicle(**vehicle.dict(), user_id=current_user.id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/{vehicle_id}", response_model=VehicleSchema)
async def get_vehicle(
    vehicle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleSchema)
async def update_vehicle(
    vehicle_id: str,
    vehicle_update: VehicleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    for key, value in vehicle_update.dict().items():
        setattr(db_vehicle, key, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}