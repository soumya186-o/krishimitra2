from fastapi import APIRouter, Query
from backend.app.schemas.weather import WeatherResponse
from backend.app.services.weather_service import WeatherService

router = APIRouter()

# Well-known district coordinates for manual location selection fallback
DISTRICT_COORDS = {
    "delhi": (28.6139, 77.2090, "Delhi NCR"),
    "lucknow": (26.8467, 80.9462, "Lucknow, Uttar Pradesh"),
    "patna": (25.5941, 85.1376, "Patna, Bihar"),
    "bhopal": (23.2599, 77.4126, "Bhopal, Madhya Pradesh"),
    "jaipur": (26.9124, 75.7873, "Jaipur, Rajasthan"),
    "ludhiana": (30.9010, 75.8573, "Ludhiana, Punjab"),
    "karnal": (29.6857, 76.9905, "Karnal, Haryana"),
    "ahmedabad": (23.0225, 72.5714, "Ahmedabad, Gujarat"),
    "nagpur": (21.1458, 79.0882, "Nagpur, Maharashtra"),
    "bhubaneswar": (20.2961, 85.8245, "Bhubaneswar, Odisha"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad, Telangana"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru, Karnataka")
}

@router.get("", response_model=WeatherResponse)
async def get_weather(
    lat: float = Query(28.6139, description="Latitude"),
    lon: float = Query(77.2090, description="Longitude"),
    district: str = Query(None, description="Optional manual district selection")
):
    location_name = "Field Location"
    if district and district.lower() in DISTRICT_COORDS:
        lat, lon, location_name = DISTRICT_COORDS[district.lower()]
    elif district:
        location_name = district.title()

    return await WeatherService.get_weather(lat, lon, location_name)
