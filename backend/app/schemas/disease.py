from typing import Optional
from pydantic import BaseModel

class DiseaseBase(BaseModel):
    id: str
    crop: str
    crop_hi: str
    disease_name_en: str
    disease_name_hi: str
    pathogen: Optional[str] = None
    symptoms_en: Optional[str] = None
    symptoms_hi: Optional[str] = None
    causes_en: Optional[str] = None
    causes_hi: Optional[str] = None
    treatment_organic_en: Optional[str] = None
    treatment_organic_hi: Optional[str] = None
    treatment_chemical_en: Optional[str] = None
    treatment_chemical_hi: Optional[str] = None
    prevention_en: Optional[str] = None
    prevention_hi: Optional[str] = None
    confidence_threshold: float = 0.70

class DiseaseResponse(DiseaseBase):
    class Config:
        from_attributes = True
