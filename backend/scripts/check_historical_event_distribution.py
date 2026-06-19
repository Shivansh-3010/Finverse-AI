from collections import Counter

from database.session import SessionLocal
from models.news_article import NewsArticle

db = SessionLocal()

articles = (
    db.query(NewsArticle)
    .filter(
        NewsArticle.provider == "historical_dataset"
    )
    .all()
)

counter = Counter()

for article in articles:

    if not article.events:
        continue

    for event in article.events.split(","):
        counter[event.strip()] += 1

for event, count in counter.most_common():
    print(
        f"{event}: {count}"
    )

db.close()