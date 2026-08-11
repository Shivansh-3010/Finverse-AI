from fastapi import APIRouter

from schemas.base_response import (
    BaseResponse,
)

from services.mlops_dashboard_service import (
    MLOpsDashboardService,
)


router = APIRouter()


@router.get(
    "/dashboard",
    response_model=BaseResponse,
)
async def dashboard(
    model_name: str = "xgboost",
    symbol: str = "RELIANCE",
    timeframe: str = "1d",
    horizon: str = "5d",
):

    result = (
        MLOpsDashboardService.dashboard(
            model_name=model_name,
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )
    )

    return BaseResponse(

        success=True,

        message="MLOps dashboard generated.",

        data=result,

    )


@router.get(
    "/health",
    response_model=BaseResponse,
)
async def health(
    model_name: str = "xgboost",
    symbol: str = "RELIANCE",
    timeframe: str = "1d",
    horizon: str = "5d",
):

    result = (
        MLOpsDashboardService.dashboard(
            model_name=model_name,
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )
    )

    return BaseResponse(

        success=True,

        message="Model health.",

        data=result[
            "selected_model"
        ],

    )


@router.get(
    "/alerts",
    response_model=BaseResponse,
)
async def alerts(
    model_name: str = "xgboost",
    symbol: str = "RELIANCE",
    timeframe: str = "1d",
    horizon: str = "5d",
):

    result = (
        MLOpsDashboardService.dashboard(
            model_name=model_name,
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
        )
    )

    return BaseResponse(

        success=True,

        message="Active alerts.",

        data=result[
            "alerts"
        ],

    )


@router.get(
    "/models",
    response_model=BaseResponse,
)
async def models():

    result = (
        MLOpsDashboardService.dashboard()
    )

    return BaseResponse(

        success=True,

        message="Registered models.",

        data=result[
            "dashboard"
        ],

    )