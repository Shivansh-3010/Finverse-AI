from alpha_vantage_ingestor import AlphaVantageIngestor


ingestor = AlphaVantageIngestor()

print(
    "Configured:",
    ingestor.is_configured()
)