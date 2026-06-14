import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )

from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from services.news_collection_service import (
    NewsCollectionService,
)
from services.news_persistence_service import (
    NewsPersistenceService
)

scheduler = BackgroundScheduler()


def collect_news():

    service = NewsCollectionService()

    articles = (
        service.get_company_news_combined(
            "AAPL"
        )
    )

    print(
        f"Articles: {len(articles)}"
    )

    for article in articles:

        NewsPersistenceService.save_article(
            symbol=article["symbol"],
            article_data=article
        )


def start_scheduler():

    scheduler.add_job(
        collect_news,
        trigger="interval",
        minutes=15,
        id="news_collection",
        replace_existing=True,
    )

    scheduler.start()


def stop_scheduler():

    scheduler.shutdown()
    
if __name__ == "__main__":
    collect_news()