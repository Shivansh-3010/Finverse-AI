from fastapi import APIRouter
from schemas.technical_analysis import TechnicalAnalysisResponse
from services.technical_analysis_service import TechnicalAnalysisService
from schemas.indicator_explanation import IndicatorExplanation
from services.explainability_service import ExplainabilityService
from schemas.multi_timeframe_analysis import MultiTimeframeAnalysisResponse
from services.multi_timeframe_service import MultiTimeframeService
from schemas.copilot_analysis import CopilotAnalysisResponse
from services.copilot_service import CopilotService
from schemas.technical_indicator import (
    TechnicalIndicatorResponse,
    TechnicalIndicatorHistoryResponse,
)
from services.technical_indicator_service import (
    TechnicalIndicatorService,
)

from schemas.base_response import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def get_stocks():
    return BaseResponse(
        success=True,
        message="Stocks endpoint ready",
        data={}
    )

@router.get(
    "/{symbol}/technical",
    response_model=TechnicalAnalysisResponse
)
async def get_technical_analysis(symbol: str):
    return TechnicalAnalysisService.analyze(symbol)

@router.get(
    "/{symbol}/explanation",
    response_model=IndicatorExplanation
)
async def get_indicator_explanation(symbol: str):
    """
    Temporary Phase 7 Explainability endpoint.
    Later this will pull actual indicator values.
    """

    return ExplainabilityService.explain_rsi(28.0)

@router.get(
    "/{symbol}/multi-timeframe",
    response_model=MultiTimeframeAnalysisResponse
)
async def get_multi_timeframe_analysis(symbol: str):
    return MultiTimeframeService.analyze(symbol)

@router.get(
    "/{symbol}/analysis",
    response_model=CopilotAnalysisResponse
)
async def get_copilot_analysis(symbol: str):
    return CopilotService.analyze(symbol)

@router.get(
    "/{symbol}/indicators",
    response_model=TechnicalIndicatorResponse
)
async def get_indicators(symbol: str):

    return TechnicalIndicatorService.get_latest(
        symbol
    )
    
@router.get(
    "/{symbol}/indicators/history",
    response_model=TechnicalIndicatorHistoryResponse
)
async def get_indicator_history(symbol: str):

    return TechnicalIndicatorService.get_history(
        symbol
    )