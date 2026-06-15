from fastapi import APIRouter

from schemas.base_response import BaseResponse

from services.recommendation_service import (
    RecommendationService,
)

router = APIRouter()


@router.get("/{symbol}",
            response_model=BaseResponse)
async def get_recommendation(
    symbol: str,
    timeframe: str = "1d"
):

    result = (
        RecommendationService.generate(
            symbol=symbol,
            timeframe=timeframe
        )
    )

    return BaseResponse(
        success=True,
        message="Recommendation generated",
        data=result
    )