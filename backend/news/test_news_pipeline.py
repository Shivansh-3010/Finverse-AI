from backend.news.news_pipeline import (
    NewsPipeline
)

pipeline = NewsPipeline()

headlines = [
    "Reliance Industries reports strong quarterly earnings growth",
    "Company announces routine management update",
    "SEBI launches investigation into accounting fraud allegations"
]

for headline in headlines:

    result = pipeline.analyze(
        headline
    )

    print("\n")
    print(result)