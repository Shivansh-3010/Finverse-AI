import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from ingestion.yahoo_ingestor import YahooIngestor
from validation.ohlcv_validator import OHLCVValidator
from transformation.ohlcv_transformer import OHLCVTransformer

from database.session import SessionLocal
from repositories.ohlcv_repository import OHLCVRepository
from services.market_data_service import MarketDataService


df = YahooIngestor().get_historical_data(
    symbol="RELIANCE.NS",
    period="1mo",
    interval="1d"
)

if not OHLCVValidator.validate(df):
    raise Exception("Validation failed")

transformed_df = OHLCVTransformer.transform(
    df,
    symbol="RELIANCE"
)

db = SessionLocal()

try:
    repository = OHLCVRepository(db)
    service = MarketDataService(repository)

    service.save_market_data(transformed_df)

    print("Data saved successfully.")
finally:
    db.close()