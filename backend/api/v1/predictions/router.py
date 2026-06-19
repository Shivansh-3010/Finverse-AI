from fastapi import APIRouter

from schemas.base_response import BaseResponse

from services.prediction_service import (
    PredictionService,
)

router = APIRouter()


@router.get(
    "/{symbol}",
    response_model=BaseResponse
)
async def get_prediction(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    result = (
        PredictionService.generate(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )
    )

    return BaseResponse(
        success=True,
        message="Prediction generated",
        data=result
    )