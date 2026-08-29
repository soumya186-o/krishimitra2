from typing import List, Optional
from pydantic import BaseModel

class AIQueryRequest(BaseModel):
    query: str
    language: str = "auto"
    crop: Optional[str] = None
    district: Optional[str] = None

class AIQueryResponse(BaseModel):
    answer: str
    answer_hi: Optional[str] = None
    detected_intent: str
    confidence: float
    is_verified_fact: bool
    source: str
    provider: str
    recommended_actions: Optional[List[str]] = None
