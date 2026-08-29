from typing import List, Optional
from pydantic import BaseModel
from backend.app.schemas.crop import CropResponse
from backend.app.schemas.disease import DiseaseResponse
from backend.app.schemas.scheme import SchemeResponse
from backend.app.schemas.loan import LoanResponse

class SyncResponse(BaseModel):
    version: str
    last_updated: str
    crops_count: int
    diseases_count: int
    schemes_count: int
    loans_count: int
    crops: List[CropResponse]
    diseases: List[DiseaseResponse]
    schemes: List[SchemeResponse]
    loans: List[LoanResponse]
