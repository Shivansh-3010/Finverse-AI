from fastapi import APIRouter
import pandas as pd

from schemas.base_response import BaseResponse

from services.mlops_dashboard_service import (
    MLOpsDashboardService,
)

router = APIRouter()


def _sample_training_data():

    return pd.DataFrame({

        "rsi": [45, 50, 55],

        "macd": [0.2, 0.3, 0.4],

    })


def _sample_production_data():

    return pd.DataFrame({

        "rsi": [70, 72, 69],

        "macd": [0.2, 0.3, 0.4],

    })


def _sample_historical_predictions():

    return [

        1.0,
        1.1,
        0.9,

    ]


def _sample_recent_predictions():

    return [

        5.0,
        4.9,
        5.2,

    ]


@router.get(
    "/dashboard",
    response_model=BaseResponse,
)
async def dashboard():

    result = (
        MLOpsDashboardService.dashboard(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=_sample_training_data(),

            production_features=_sample_production_data(),

            historical_predictions=
                _sample_historical_predictions(),

            recent_predictions=
                _sample_recent_predictions(),
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
async def health():

    result = (
        MLOpsDashboardService.dashboard(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=_sample_training_data(),

            production_features=_sample_production_data(),

            historical_predictions=
                _sample_historical_predictions(),

            recent_predictions=
                _sample_recent_predictions(),
        )
    )

    return BaseResponse(

        success=True,

        message="Model health.",

        data=result["selected_model"],

    )


@router.get(
    "/alerts",
    response_model=BaseResponse,
)
async def alerts():

    result = (
        MLOpsDashboardService.dashboard(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=_sample_training_data(),

            production_features=_sample_production_data(),

            historical_predictions=
                _sample_historical_predictions(),

            recent_predictions=
                _sample_recent_predictions(),
        )
    )

    return BaseResponse(

        success=True,

        message="Active alerts.",

        data=result["alerts"],

    )


@router.get(
    "/models",
    response_model=BaseResponse,
)
async def models():

    result = (
        MLOpsDashboardService.dashboard(
            model_name="xgboost",
            symbol="RELIANCE",
            horizon="5d",

            training_features=_sample_training_data(),

            production_features=_sample_production_data(),

            historical_predictions=
                _sample_historical_predictions(),

            recent_predictions=
                _sample_recent_predictions(),
        )
    )

    return BaseResponse(

        success=True,

        message="Registered models.",

        data=result["dashboard"],

    )