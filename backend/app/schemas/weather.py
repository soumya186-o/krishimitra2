from typing import List, Optional
from pydantic import BaseModel

class WeatherForecastDay(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    precipitation_prob: int
    condition: str
    condition_hi: str
    advisory: str
    advisory_hi: str

class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    current_temperature: float
    humidity: int
    wind_speed: float
    precipitation: float
    weather_condition: str
    weather_condition_hi: str
    agri_advisory: str
    agri_advisory_hi: str
    forecast: List[WeatherForecastDay]
    source: str
