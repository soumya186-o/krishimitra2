from typing import Optional
from pydantic import BaseModel

class LoanBase(BaseModel):
    id: str
    bank_name: str
    bank_name_hi: str
    loan_type: str
    loan_type_hi: str
    purpose_en: Optional[str] = None
    purpose_hi: Optional[str] = None
    interest_rate: Optional[str] = None
    interest_rate_hi: Optional[str] = None
    max_limit: Optional[str] = None
    max_limit_hi: Optional[str] = None
    eligibility_en: Optional[str] = None
    eligibility_hi: Optional[str] = None
    documents_required: Optional[str] = None
    documents_required_hi: Optional[str] = None
    official_url: Optional[str] = None
    source: Optional[str] = None
    last_verified: Optional[str] = None

class LoanResponse(LoanBase):
    class Config:
        from_attributes = True
