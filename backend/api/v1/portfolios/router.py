from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import SessionLocal
from schemas.base_response import BaseResponse
from schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
)
from services.portfolio_service import (
    portfolio_service,
)
from decimal import Decimal
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException

from schemas.portfolio_transaction import (
    PortfolioTransactionCreate,
    PortfolioTransactionResponse,
)

from services.portfolio_transaction_service import (
    portfolio_transaction_service,
)
from services.portfolio_summary_service import (
    portfolio_summary_service,
)
from services.portfolio_snapshot_service import (
    portfolio_snapshot_service,
)
from services.portfolio_twr_service import (
    portfolio_twr_service,
)
from services.portfolio_risk_service import (
    portfolio_risk_service,
)
from services.portfolio_performance_service import (
    portfolio_performance_service,
)
from services.portfolio_xirr_service import (
    portfolio_xirr_service,
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
async def create_portfolio(
    payload: PortfolioCreate,
    db: Session = Depends(get_db),
):
    portfolio = portfolio_service.create(
        db=db,
        user_id=payload.user_id,
        name=payload.name,
        total_value=payload.total_value,
    )

    return BaseResponse(
        success=True,
        message="Portfolio created",
        data=PortfolioResponse.model_validate(
            portfolio
        ).model_dump(),
    )


@router.get(
    "/user/{user_id}",
    response_model=BaseResponse,
)
async def get_user_portfolios(
    user_id,
    db: Session = Depends(get_db),
):
    portfolios = portfolio_service.get_by_user(
        db=db,
        user_id=user_id,
    )

    return BaseResponse(
        success=True,
        message="Portfolios retrieved",
        data=[
            PortfolioResponse.model_validate(
                portfolio
            ).model_dump()
            for portfolio in portfolios
        ],
    )
    
@router.post(
    "/{portfolio_id}/transactions",
    response_model=BaseResponse,
)
async def create_transaction(
    portfolio_id: UUID,
    payload: PortfolioTransactionCreate,
    db: Session = Depends(get_db),
):
    if payload.portfolio_id != portfolio_id:
        raise HTTPException(
            status_code=400,
            detail="Portfolio ID in path and payload must match",
        )

    try:
        transaction = (
            portfolio_transaction_service
            .create_transaction(
                db=db,
                data=payload,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return BaseResponse(
        success=True,
        message="Portfolio transaction created",
        data=PortfolioTransactionResponse
        .model_validate(transaction)
        .model_dump(),
    )


@router.get(
    "/{portfolio_id}/transactions",
    response_model=BaseResponse,
)
async def get_portfolio_transactions(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    transactions = (
        portfolio_transaction_service
        .get_portfolio_transactions(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio transactions retrieved",
        data=[
            PortfolioTransactionResponse
            .model_validate(transaction)
            .model_dump()
            for transaction in transactions
        ],
    )


@router.get(
    "/{portfolio_id}/transactions/{symbol}",
    response_model=BaseResponse,
)
async def get_symbol_transactions(
    portfolio_id: UUID,
    symbol: str,
    db: Session = Depends(get_db),
):
    transactions = (
        portfolio_transaction_service
        .get_symbol_transactions(
            db=db,
            portfolio_id=portfolio_id,
            symbol=symbol,
        )
    )

    return BaseResponse(
        success=True,
        message="Symbol transactions retrieved",
        data=[
            PortfolioTransactionResponse
            .model_validate(transaction)
            .model_dump()
            for transaction in transactions
        ],
    )


@router.get(
    "/{portfolio_id}/transactions/date-range",
    response_model=BaseResponse,
)
async def get_transactions_by_date_range(
    portfolio_id: UUID,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
):
    try:
        transactions = (
            portfolio_transaction_service
            .get_transactions_by_date_range(
                db=db,
                portfolio_id=portfolio_id,
                start_date=start_date,
                end_date=end_date,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return BaseResponse(
        success=True,
        message="Portfolio transactions retrieved",
        data=[
            PortfolioTransactionResponse
            .model_validate(transaction)
            .model_dump()
            for transaction in transactions
        ],
    )
    
@router.get(
    "/{portfolio_id}/summary",
    response_model=BaseResponse,
)
async def get_portfolio_summary(
    portfolio_id: UUID,
    timeframe: str = "1d",
    db: Session = Depends(get_db),
):
    result = (
        portfolio_summary_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
            timeframe=timeframe,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio summary retrieved",
        data=result,
    )
    
@router.post(
    "/{portfolio_id}/snapshots",
    response_model=BaseResponse,
)
async def create_portfolio_snapshot(
    portfolio_id: UUID,
    snapshot_time: datetime,
    portfolio_value: Decimal,
    cash: Decimal,
    invested_value: Decimal,
    return_value: Decimal,
    risk_score: Decimal | None = None,
    db: Session = Depends(get_db),
):
    try:
        snapshot = (
            portfolio_snapshot_service.create(
                db=db,
                portfolio_id=portfolio_id,
                snapshot_time=snapshot_time,
                portfolio_value=portfolio_value,
                cash=cash,
                invested_value=invested_value,
                return_value=return_value,
                risk_score=risk_score,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return BaseResponse(
        success=True,
        message="Portfolio snapshot created",
        data={
            "id": str(snapshot.id),
            "portfolio_id": str(snapshot.portfolio_id),
            "snapshot_time": snapshot.snapshot_time,
            "portfolio_value": snapshot.portfolio_value,
            "cash": snapshot.cash,
            "invested_value": snapshot.invested_value,
            "return_value": snapshot.return_value,
            "risk_score": snapshot.risk_score,
        },
    )


@router.get(
    "/{portfolio_id}/snapshots",
    response_model=BaseResponse,
)
async def get_portfolio_snapshots(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    snapshots = (
        portfolio_snapshot_service.get_by_portfolio(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio snapshots retrieved",
        data=[
            {
                "id": str(snapshot.id),
                "portfolio_id": str(snapshot.portfolio_id),
                "snapshot_time": snapshot.snapshot_time,
                "portfolio_value": snapshot.portfolio_value,
                "cash": snapshot.cash,
                "invested_value": snapshot.invested_value,
                "return_value": snapshot.return_value,
                "risk_score": snapshot.risk_score,
            }
            for snapshot in snapshots
        ],
    )


@router.get(
    "/{portfolio_id}/snapshots/latest",
    response_model=BaseResponse,
)
async def get_latest_portfolio_snapshot(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    snapshot = (
        portfolio_snapshot_service.get_latest(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail="No portfolio snapshot found",
        )

    return BaseResponse(
        success=True,
        message="Latest portfolio snapshot retrieved",
        data={
            "id": str(snapshot.id),
            "portfolio_id": str(snapshot.portfolio_id),
            "snapshot_time": snapshot.snapshot_time,
            "portfolio_value": snapshot.portfolio_value,
            "cash": snapshot.cash,
            "invested_value": snapshot.invested_value,
            "return_value": snapshot.return_value,
            "risk_score": snapshot.risk_score,
        },
    )
    
@router.get(
    "/{portfolio_id}/twr",
    response_model=BaseResponse,
)
async def get_portfolio_twr(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    result = (
        portfolio_twr_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio TWR calculated",
        data=result,
    )
    
@router.get(
    "/{portfolio_id}/risk",
    response_model=BaseResponse,
)
async def get_portfolio_risk(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    result = (
        portfolio_risk_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio risk calculated",
        data=result,
    )
    
@router.get(
    "/{portfolio_id}/performance",
    response_model=BaseResponse,
)
async def get_portfolio_performance(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    result = (
        portfolio_performance_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio performance calculated",
        data=result,
    )
    
@router.get(
    "/{portfolio_id}/xirr",
    response_model=BaseResponse,
)
async def get_portfolio_xirr(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
):
    result = (
        portfolio_xirr_service.calculate(
            db=db,
            portfolio_id=portfolio_id,
        )
    )

    return BaseResponse(
        success=True,
        message="Portfolio XIRR calculated",
        data=result,
    )