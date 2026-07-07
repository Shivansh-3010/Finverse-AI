from historical_news.enrichment.historical_finbert_enrichment import (
    HistoricalFinBERTEnrichment,
)

engine = HistoricalFinBERTEnrichment()

result = engine.enrich(
    input_csv="../datasets/historical_news_processed/historical_news_symbol_mapped.csv",
    output_csv="../datasets/historical_news_processed/historical_news_finbert.csv",
)

print(result)