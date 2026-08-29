from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Disease
from backend.app.schemas.disease import DiseaseResponse

router = APIRouter()

@router.get("", response_model=List[DiseaseResponse])
def get_diseases(crop: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Disease)
    if crop:
        query = query.filter(Disease.crop.ilike(f"%{crop}%"))
    return query.all()

@router.get("/{disease_id}", response_model=DiseaseResponse)
def get_disease_by_id(disease_id: str, db: Session = Depends(get_db)):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease
