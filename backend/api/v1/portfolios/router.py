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