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
from schemas.candlestick_analysis import (
    CandlestickAnalysisResponse,
)

from services.candlestick_analysis_service import (
    CandlestickAnalysisService,
)
from schemas.candlestick_pattern import (
    CandlestickPatternHistoryResponse,
)

from services.multi_timeframe_support_resistance_service import (
    MultiTimeframeSupportResistanceService,
)

from schemas.multi_timeframe_support_resistance import (
    MultiTimeframeSupportResistanceResponse,
)

from services.candlestick_pattern_service import (
    CandlestickPatternService,
)

from schemas.candlestick_explanation import (
    CandlestickExplanation,
)
from services.support_resistance_history_service import (
    SupportResistanceHistoryService,
)
from schemas.support_resistance import (
    SupportResistanceHistoryResponse,
)

from services.candlestick_explainability_service import (
    CandlestickExplainabilityService,
)

from services.multi_timeframe_pattern_service import (
    MultiTimeframePatternService,
)
from schemas.support_resistance import (
    SupportResistanceResponse,
)
from services.support_resistance_service import (
    SupportResistanceService,
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
async def get_technical_analysis(
    symbol: str,
    timeframe: str = "1d"
):
    return TechnicalAnalysisService.analyze(
        symbol=symbol,
        timeframe=timeframe
    )

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
async def get_indicators(
    symbol: str,
    timeframe: str = "1d"
):

    return TechnicalIndicatorService.get_latest(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/{symbol}/indicators/history",
    response_model=TechnicalIndicatorHistoryResponse
)
async def get_indicator_history(
    symbol: str,
    timeframe: str = "1d"
):

    return TechnicalIndicatorService.get_history(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/{symbol}/candlestick-analysis",
    response_model=CandlestickAnalysisResponse
)
async def get_candlestick_analysis(
    symbol: str,
    timeframe: str = "1d"
):

    return CandlestickAnalysisService.analyze(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/{symbol}/patterns/history",
    response_model=CandlestickPatternHistoryResponse
)
async def get_pattern_history(
    symbol: str,
    timeframe: str = "1d"
):

    return CandlestickPatternService.get_history(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/patterns/explain/{pattern}",
    response_model=CandlestickExplanation
)
async def explain_pattern(
    pattern: str
):

    return (
        CandlestickExplainabilityService
        .explain(pattern)
    )
    
@router.get(
    "/{symbol}/patterns",
    response_model=CandlestickAnalysisResponse
)
async def get_current_patterns(
    symbol: str,
    timeframe: str = "1d"
):

    return CandlestickAnalysisService.analyze(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/{symbol}/multi-timeframe-patterns"
)
def get_multi_timeframe_patterns(
    symbol: str,
):

    return (
        MultiTimeframePatternService.analyze(
            symbol
        )
    )
    
@router.get(
    "/{symbol}/support-resistance",
    response_model=SupportResistanceResponse
)
async def get_support_resistance(
    symbol: str,
    timeframe: str = "1d"
):

    return SupportResistanceService.analyze(
        symbol=symbol,
        timeframe=timeframe
    )
    
@router.get(
    "/{symbol}/support-resistance/history",
    response_model=SupportResistanceHistoryResponse,
)
async def get_support_resistance_history(
    symbol: str,
    timeframe: str = "1d",
):

    return (
        SupportResistanceHistoryService
        .get_history(
            symbol=symbol,
            timeframe=timeframe,
        )
    )
    
@router.get(
    "/{symbol}/multi-timeframe-support-resistance",
    response_model=
        MultiTimeframeSupportResistanceResponse,
)
async def get_multi_timeframe_support_resistance(
    symbol: str,
):

    return (
        MultiTimeframeSupportResistanceService
        .analyze(
            symbol=symbol
        )
    )