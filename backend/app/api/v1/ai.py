from fastapi import APIRouter
from backend.app.schemas.ai import AIQueryRequest, AIQueryResponse
from backend.app.services.ai_provider import get_ai_provider

router = APIRouter()

@router.post("/query", response_model=AIQueryResponse)
async def query_ai(request: AIQueryRequest):
    provider = get_ai_provider()
    context = {"crop": request.crop, "district": request.district}
    return await provider.answer_query(request.query, request.language, context)
