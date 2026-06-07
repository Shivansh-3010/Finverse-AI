from yahoo_ingestor import YahooIngestor


ingestor = YahooIngestor()

df = ingestor.get_historical_data(
    symbol="RELIANCE.NS",
    period="1mo",
    interval="1d"
)

print(df.head())