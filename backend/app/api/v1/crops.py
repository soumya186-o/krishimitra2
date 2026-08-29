from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Crop
from backend.app.schemas.crop import CropResponse

router = APIRouter()

@router.get("", response_model=List[CropResponse])
def get_crops(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Crop)
    if category:
        query = query.filter(Crop.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(
            (Crop.name_en.ilike(f"%{search}%")) |
            (Crop.name_hi.ilike(f"%{search}%"))
        )
    return query.all()

@router.get("/{crop_id}", response_model=CropResponse)
def get_crop_by_id(crop_id: str, db: Session = Depends(get_db)):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop
