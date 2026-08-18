from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import SessionLocal
from schemas.base_response import BaseResponse
from schemas.holding import (
    HoldingCreate,
    HoldingResponse,
)
from services.holding_service import (
    holding_service,
)


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=BaseResponse,
)
async def create_holding(
    payload: HoldingCreate,
    db: Session = Depends(get_db),
):
    holding = holding_service.create(
        db=db,
        portfolio_id=payload.portfolio_id,
        symbol=payload.symbol,
        quantity=payload.quantity,
        avg_price=payload.avg_price,
        current_price=payload.current_price,
        market_value=payload.market_value,
    )

    return BaseResponse(
        success=True,
        message="Holding created",
        data=HoldingResponse.model_validate(
            holding
        ).model_dump(),
    )


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=BaseResponse,
)
async def get_portfolio_holdings(
    portfolio_id,
    db: Session = Depends(get_db),
):
    holdings = holding_service.get_by_portfolio(
        db=db,
        portfolio_id=portfolio_id,
    )

    return BaseResponse(
        success=True,
        message="Holdings retrieved",
        data=[
            HoldingResponse.model_validate(
                holding
            ).model_dump()
            for holding in holdings
        ],
    )