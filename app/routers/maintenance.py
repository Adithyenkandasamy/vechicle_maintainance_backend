from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.vehicle import Vehicle
from ..models.maintenance import MaintenanceRecord, MaintenanceSchedule
from ..schemas.maintenance import (
    MaintenanceRecordCreate,
    MaintenanceRecord as MaintenanceRecordSchema,
    MaintenanceScheduleCreate,
    MaintenanceSchedule as MaintenanceScheduleSchema
)
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/records", response_model=MaintenanceRecordSchema)
async def create_maintenance_record(
    record: MaintenanceRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == record.vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db_record = MaintenanceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/records/{vehicle_id}", response_model=List[MaintenanceRecordSchema])
async def get_maintenance_records(
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
    
    return db.query(MaintenanceRecord).filter(
        MaintenanceRecord.vehicle_id == vehicle_id
    ).all()

@router.post("/schedules", response_model=MaintenanceScheduleSchema)
async def create_maintenance_schedule(
    schedule: MaintenanceScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == schedule.vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db_schedule = MaintenanceSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/schedules/{vehicle_id}", response_model=List[MaintenanceScheduleSchema])
async def get_maintenance_schedules(
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
    
    return db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.vehicle_id == vehicle_id
    ).all()