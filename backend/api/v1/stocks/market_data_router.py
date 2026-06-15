from fastapi import APIRouter, HTTPException

from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from schemas.market_data import (
    MarketDataResponse,
)

router = APIRouter(
    prefix="/stocks",
    tags=["Market Data"]
)


@router.get(
    "/{symbol}",
    response_model=MarketDataResponse
)
def get_stock(
    symbol: str,
    timeframe: str = "1d"
):

    db = SessionLocal()

    try:

        repository = OHLCVRepository(
            db
        )

        records = (
            repository.get_latest_by_symbol_and_timeframe(
                symbol=symbol,
                timeframe=timeframe,
                limit=1
            )
        )

        if not records:

            raise HTTPException(
                status_code=404,
                detail="No market data found"
            )

        latest = records[0]

        return MarketDataResponse(
            symbol=latest.symbol,
            timeframe=latest.timeframe,
            open=latest.open,
            high=latest.high,
            low=latest.low,
            close=latest.close,
            volume=latest.volume,
            timestamp=latest.timestamp,
        )

    finally:
        db.close()