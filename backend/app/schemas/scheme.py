from typing import Optional
from pydantic import BaseModel

class SchemeBase(BaseModel):
    id: str
    name_en: str
    name_hi: str
    category: Optional[str] = None
    category_hi: Optional[str] = None
    ministry: Optional[str] = None
    benefits_en: Optional[str] = None
    benefits_hi: Optional[str] = None
    eligibility_en: Optional[str] = None
    eligibility_hi: Optional[str] = None
    application_process_en: Optional[str] = None
    application_process_hi: Optional[str] = None
    official_url: Optional[str] = None
    source: Optional[str] = None
    last_verified: Optional[str] = None

class SchemeResponse(SchemeBase):
    class Config:
        from_attributes = True
