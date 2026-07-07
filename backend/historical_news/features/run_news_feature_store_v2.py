from historical_news.features.news_feature_store_v2 import (
    NewsFeatureStoreV2Generator,
)

generator = (
    NewsFeatureStoreV2Generator()
)

result = generator.generate(
    input_csv="../datasets/historical_news_processed/news_features_daily.csv",
    output_csv="../datasets/historical_news_processed/news_features_daily_v2.csv",
)

print(result)