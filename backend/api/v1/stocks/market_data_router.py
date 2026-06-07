from fastapi import APIRouter
from schemas.market_data import MarketDataResponse


router = APIRouter(
    prefix="/stocks",
    tags=["Market Data"]
)


@router.get(
    "/{symbol}",
    response_model=MarketDataResponse
)
def get_stock(symbol: str):

    return {
        "symbol": symbol,
        "source": "market_data_service",
        "status": "ready"
    }