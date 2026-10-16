from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.session import get_db
from fastapi import APIRouter

from schemas.base_response import (
    BaseResponse,
)

from services.copilot_service import (
    CopilotService,
)

router = APIRouter()


@router.get(
    "/{symbol}",
    response_model=BaseResponse
)
async def get_copilot(
    symbol: str
):

    result = (
        CopilotService.analyze(
            symbol
        )
    )

    return BaseResponse(
        success=True,
        message="Copilot analysis generated",
        data=result.model_dump()
    )
    

@router.get(
    "/portfolio/{portfolio_id}",
    response_model=BaseResponse,
)
def get_portfolio_copilot(
    portfolio_id: UUID,
    benchmark: str = "NIFTY50",
    timeframe: str = "1d",
    lookback_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    result = CopilotService.analyze_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        benchmark=benchmark,
        timeframe=timeframe,
        lookback_days=lookback_days,
    )

    return BaseResponse(
        success=True,
        message="Portfolio Copilot analysis generated",
        data=result,
    )
