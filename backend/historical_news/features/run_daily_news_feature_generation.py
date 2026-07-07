from historical_news.features.daily_news_feature_generator import (
    DailyNewsFeatureGenerator,
)

generator = (
    DailyNewsFeatureGenerator()
)

result = generator.generate(
    input_csv="../datasets/historical_news_processed/historical_news_events.csv",
    output_csv="../datasets/historical_news_processed/news_features_daily.csv",
)

print(result)