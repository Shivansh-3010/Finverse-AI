from fastapi import APIRouter

from schemas.base_response import BaseResponse

from backend.agents.news_intelligence_agent.agent import (
    NewsIntelligenceAgent
)

router = APIRouter()

news_agent = NewsIntelligenceAgent()


@router.get(
    "/analyze/{headline}",
    response_model=BaseResponse
)
async def analyze_news(
    headline: str
):

    result = (
        news_agent.analyze_news(
            headline
        )
    )

    return BaseResponse(
        success=True,
        message="News analysis completed",
        data=result
    )