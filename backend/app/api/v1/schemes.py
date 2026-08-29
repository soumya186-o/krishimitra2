from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Scheme
from backend.app.schemas.scheme import SchemeResponse

router = APIRouter()

@router.get("", response_model=List[SchemeResponse])
def get_schemes(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Scheme)
    if category:
        query = query.filter(Scheme.category.ilike(f"%{category}%"))
    return query.all()

@router.get("/{scheme_id}", response_model=SchemeResponse)
def get_scheme_by_id(scheme_id: str, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
