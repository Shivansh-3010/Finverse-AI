from historical_news.enrichment.historical_event_enrichment import (
    HistoricalEventEnrichment,
)


engine = HistoricalEventEnrichment()

result = engine.enrich(
    input_csv="../datasets/historical_news_processed/historical_news_finbert.csv",
    output_csv="../datasets/historical_news_processed/historical_news_events.csv",
)

print(result)