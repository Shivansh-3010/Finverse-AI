from fastapi import APIRouter

from database.session import (
    SessionLocal,
)

from schemas.base_response import (
    BaseResponse,
)

from services.prediction_service import (
    PredictionService,
)

from services.model_comparison_service import (
    ModelComparisonService,
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
    
@router.get(
    "/{symbol}/models",
    response_model=BaseResponse
)
async def compare_models(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    db = SessionLocal()

    try:

        result = (
            ModelComparisonService.compare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        return BaseResponse(
            success=True,
            message="Model comparison generated",
            data=result,
        )

    finally:
        db.close()
        
@router.get(
    "/{symbol}/horizon",
    response_model=BaseResponse
)
async def horizon_prediction(
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
        message=f"Horizon forecast generated ({horizon})",
        data=result,
    )
    
@router.get(
    "/{symbol}/report",
    response_model=BaseResponse
)
async def prediction_report(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    db = SessionLocal()

    try:

        result = (
            PredictionService.generate_report(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        return BaseResponse(
            success=True,
            message="Prediction report generated",
            data=result,
        )

    finally:
        db.close()