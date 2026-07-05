import sys
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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

    symbols = [

        # Banking & Financials
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "KOTAKBANK",
        "AXISBANK",
        "INDUSINDBK",
        "BAJFINANCE",
        "BAJAJFINSV",
        "PFC",
        "RECLTD",

        # IT
        "TCS",
        "INFY",
        "HCLTECH",
        "WIPRO",
        "TECHM",
        "PERSISTENT",
        "COFORGE",

        # Energy & Oil
        "RELIANCE",
        "ONGC",
        "BPCL",
        "IOC",
        "GAIL",
        "OIL",

        # Auto
        "M&M",
        "MARUTI",
        "BAJAJ-AUTO",
        "HEROMOTOCO",
        "ASHOKLEY",

        # Defence
        "HAL",
        "BEL",
        "BDL",
        "GRSE",
        "MAZDOCK",

        # Railways
        "IRFC",
        "RVNL",
        "IRCON",
        "RAILTEL",
        "CONCOR",

        # Infrastructure & Capital Goods
        "LT",
        "SIEMENS",
        "ABB",
        "CUMMINSIND",
        "BHEL",

        # FMCG
        "ITC",
        "HINDUNILVR",
        "NESTLEIND",
        "BRITANNIA",
        "DABUR",

        # Pharma
        "SUNPHARMA",
        "DRREDDY",
        "CIPLA",
        "LUPIN",
        "AUROPHARMA",

        # Metals
        "TATASTEEL",
        "JSWSTEEL",
        "HINDALCO",
        "NMDC",

        # Green Energy / PSU Themes
        "IREDA",
        "NTPC",
        "POWERGRID",
        "NHPC",
        "SJVN",
        "SUZLON",
        
        # Others
        "SPICEJET",
        "NBCC",
        "PCJEWELLER",
        "RPOWER",
        "HUDCO",
        "IRB",
        "INDIANB",
        "INOXWIND",
        "TTML",
        "ASMTEC",
        "RITES",
        "IFCI",
        "WALCHANNAG",
        "IGL",
        "MANAPPURAM",
        "MOBIKWIK",
        "VENTIVE",
        "BLS",
        "IDEA",
        "DCXINDIA",
        "QUADFUTURE",
        "VIJAYA",
        "KAYNES",
        "LICI",
        "JIOFIN",
        "AEROFLEX",
        "ITDC",
        "TITAGARH",
        "MMTC",
        "CREDITACC",
        "MTARTECH",
    ]

    selected_symbols = random.sample(
        symbols,
        min(20, len(symbols))
    )

    print(
        f"Selected {len(selected_symbols)} symbols"
    )

    for symbol in selected_symbols:

        try:

            articles = (
                service.get_company_news_combined(
                    symbol
                )
            )

            print(
                f"{symbol}: {len(articles)}"
            )

            for article in articles:

                NewsPersistenceService.save_article(
                    symbol=article["symbol"],
                    article_data=article
                )

        except Exception as e:

            print(
                f"{symbol}: ERROR -> {e}"
            )


def start_scheduler():

    scheduler.add_job(
        collect_news,
        trigger="interval",
        minutes=60,
        id="news_collection",
        replace_existing=True,
    )

    scheduler.start()


def stop_scheduler():

    scheduler.shutdown()
    
if __name__ == "__main__":
    collect_news()