from ingestion.yahoo_ingestor import YahooIngestor
from validation.ohlcv_validator import OHLCVValidator
from transformation.ohlcv_transformer import OHLCVTransformer


ingestor = YahooIngestor()

df = ingestor.get_historical_data(
    symbol="RELIANCE.NS",
    period="1mo",
    interval="1d"
)

print("Validation Result:")
print(OHLCVValidator.validate(df))

transformed_df = OHLCVTransformer.transform(
    df,
    symbol="RELIANCE"
)

print("\nTransformed Data:")
print(transformed_df.head())