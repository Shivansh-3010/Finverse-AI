from fastapi import APIRouter

from schemas.base_response import BaseResponse

from services.risk_analysis_service import (
    RiskAnalysisService,
)
from services.position_sizing_service import (
    PositionSizingService,
)
from services.stop_loss_service import (
    StopLossService,
)
from services.risk_report_service import (
    RiskReportService,
)
from services.risk_metric_history_service import (
    RiskMetricHistoryService,
)

from schemas.risk_metric_history import (
    RiskMetricHistoryResponse,
)

router = APIRouter()


@router.get(
    "/{symbol}",
    response_model=BaseResponse
)
async def get_risk_analysis(
    symbol: str,
    timeframe: str = "1d"
):

    result = (
        RiskAnalysisService.analyze(
            symbol=symbol,
            timeframe=timeframe
        )
    )

    return BaseResponse(
        success=True,
        message="Risk analysis generated",
        data=result
    )
    
@router.get(
    "/{symbol}/position-size",
    response_model=BaseResponse
)
async def get_position_size(
    symbol: str,
    capital: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
):

    result = (
        PositionSizingService.calculate(
            capital=capital,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
        )
    )

    return BaseResponse(
        success=True,
        message=f"Position size for {symbol}",
        data=result
    )
    
@router.get(
    "/{symbol}/stop-loss",
    response_model=BaseResponse
)
async def get_stop_loss(
    symbol: str,
    entry_price: float,
    atr: float,
    risk_reward_ratio: float = 3.0,
):

    result = (
        StopLossService.calculate(
            entry_price=entry_price,
            atr=atr,
            risk_reward_ratio=risk_reward_ratio,
        )
    )

    return BaseResponse(
        success=True,
        message=f"Stop loss levels for {symbol}",
        data=result
    )
    
@router.get(
    "/{symbol}/report",
    response_model=BaseResponse
)
async def get_risk_report(
    symbol: str,
    capital: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
    atr: float,
    timeframe: str = "1d",
):

    result = (
        RiskReportService.generate(
            symbol=symbol,
            timeframe=timeframe,
            capital=capital,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
            atr=atr,
        )
    )

    return BaseResponse(
        success=True,
        message=f"Risk report for {symbol}",
        data=result
    )

@router.get(
    "/{symbol}/history",
    response_model=RiskMetricHistoryResponse
)
async def get_risk_history(
    symbol: str,
    timeframe: str = "1d"
):

    return (
        RiskMetricHistoryService.get_history(
            symbol=symbol,
            timeframe=timeframe
        )
    )