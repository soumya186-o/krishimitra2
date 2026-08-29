from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Crop, Disease, Scheme, Loan
from backend.app.schemas.sync import SyncResponse
from backend.app.schemas.crop import CropResponse
from backend.app.schemas.disease import DiseaseResponse
from backend.app.schemas.scheme import SchemeResponse
from backend.app.schemas.loan import LoanResponse

router = APIRouter()

@router.get("", response_model=SyncResponse)
def sync_all_data(db: Session = Depends(get_db)):
    crops = db.query(Crop).all()
    diseases = db.query(Disease).all()
    schemes = db.query(Scheme).all()
    loans = db.query(Loan).all()

    return SyncResponse(
        version="1.0.0",
        last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        crops_count=len(crops),
        diseases_count=len(diseases),
        schemes_count=len(schemes),
        loans_count=len(loans),
        crops=[CropResponse.model_validate(c, from_attributes=True) for c in crops],
        diseases=[DiseaseResponse.model_validate(d, from_attributes=True) for d in diseases],
        schemes=[SchemeResponse.model_validate(s, from_attributes=True) for s in schemes],
        loans=[LoanResponse.model_validate(l, from_attributes=True) for l in loans]
    )
