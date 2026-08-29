from typing import Optional
from pydantic import BaseModel

class CropBase(BaseModel):
    id: str
    name_en: str
    name_hi: str
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    category_hi: Optional[str] = None
    soil: Optional[str] = None
    soil_hi: Optional[str] = None
    soil_ph: Optional[str] = None
    climate: Optional[str] = None
    climate_hi: Optional[str] = None
    temperature: Optional[str] = None
    sowing_season: Optional[str] = None
    sowing_season_hi: Optional[str] = None
    irrigation: Optional[str] = None
    irrigation_hi: Optional[str] = None
    fertilizer: Optional[str] = None
    fertilizer_hi: Optional[str] = None
    harvesting: Optional[str] = None
    harvesting_hi: Optional[str] = None
    pests: Optional[str] = None
    pests_hi: Optional[str] = None
    diseases: Optional[str] = None
    diseases_hi: Optional[str] = None
    cultivation_tips: Optional[str] = None
    cultivation_tips_hi: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None

class CropResponse(CropBase):
    class Config:
        from_attributes = True
