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

from services.prediction_dashboard_service import (
    PredictionDashboardService,
)

from services.prediction_evaluation_service import (
    PredictionEvaluationService,
)

from feature_store.prediction.prediction_features import (
    PredictionFeatureStore,
)

from repositories.prediction_repository import (
    PredictionRepository,
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
        
@router.get(
    "/{symbol}/dashboard",
    response_model=BaseResponse,
)
async def prediction_dashboard(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    result = (
        PredictionDashboardService.dashboard(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )
    )

    return BaseResponse(
        success=True,
        message="Prediction dashboard generated",
        data=result,
    )
    
@router.get(
    "/{symbol}/evaluation",
    response_model=BaseResponse,
)
async def prediction_evaluation(
    symbol: str,
    timeframe: str = "1d",
):

    db = SessionLocal()

    try:

        result = (
            PredictionEvaluationService.summary(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        return BaseResponse(
            success=True,
            message="Prediction evaluation generated",
            data=result,
        )

    finally:
        db.close()
        
@router.get(
    "/{symbol}/leaderboard",
    response_model=BaseResponse,
)
async def prediction_leaderboard(
    symbol: str,
    timeframe: str = "1d",
):

    db = SessionLocal()

    try:

        result = (
            PredictionEvaluationService.summary(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
            )

        )["leaderboard"]

        return BaseResponse(
            success=True,
            message="Prediction leaderboard generated",
            data=result,
        )

    finally:
        db.close()
        
@router.get(
    "/{symbol}/history",
    response_model=BaseResponse,
)
async def prediction_history(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    db = SessionLocal()

    try:

        repository = PredictionRepository(db)

        rows = repository.get_history(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )

        history = [
            {
                "timestamp": row.timestamp.isoformat(),
                "symbol": row.symbol,
                "timeframe": row.timeframe,
                "model_name": row.model_name,
                "prediction": row.prediction,
                "confidence": row.confidence,
                "horizon": row.horizon,
            }
            for row in rows
        ]

        return BaseResponse(
            success=True,
            message="Prediction history generated",
            data=history,
        )

    finally:
        db.close()
        
@router.get(
    "/{symbol}/feature-store",
    response_model=BaseResponse,
)
async def prediction_feature_store(
    symbol: str,
    timeframe: str = "1d",
    horizon: str = "1d",
):

    db = SessionLocal()

    try:

        result = (
            PredictionFeatureStore.latest(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        return BaseResponse(
            success=True,
            message="Prediction feature store generated",
            data=result,
        )

    finally:
        db.close()