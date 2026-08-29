from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "KrishiMitra Backend",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "ai_fallback_provider": settings.AI_FALLBACK_PROVIDER
    }
